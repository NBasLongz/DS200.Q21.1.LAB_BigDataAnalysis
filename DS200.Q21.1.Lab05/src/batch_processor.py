import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from config import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FMT)
log = logging.getLogger("BatchProcessor")

try:
    import cv2
    import numpy as np
    _CV2 = True
except ImportError:
    _CV2 = False
    log.error("OpenCV là bắt buộc. Cài bằng: pip install opencv-python")
    sys.exit(1)

try:
    from ultralytics import YOLO as _YOLO
    _YOLO_OK = True
except ImportError:
    _YOLO_OK = False
    log.warning("Ultralytics không có – sẽ bỏ qua detection thực tế.")

try:
    from sahi import AutoDetectionModel
    from sahi.predict import get_sliced_prediction
    _SAHI_OK = True
except ImportError:
    _SAHI_OK = False

try:
    from pyspark import SparkContext, SparkConf
    _SPARK_OK = True
except ImportError:
    _SPARK_OK = False
    log.warning("PySpark không có – xử lý tuần tự.")


def process_single_video(args_tuple: tuple) -> dict:
    video_path, model_path, use_sahi, confidence, output_dir = args_tuple

    import cv2, json, os, time
    import numpy as np
    from pathlib import Path
    from datetime import datetime

    video_name = Path(video_path).stem
    model      = None
    sahi_model = None

    try:
        from ultralytics import YOLO
        model = YOLO(model_path)
    except Exception:
        pass

    if use_sahi and model is not None:
        try:
            from sahi import AutoDetectionModel
            sahi_model = AutoDetectionModel.from_pretrained(
                model_type="yolov8", model_path=model_path,
                confidence_threshold=confidence, device="cpu",
            )
        except Exception:
            sahi_model = None

    def _detect_frame(frame):
        if sahi_model:
            try:
                from sahi.predict import get_sliced_prediction
                res = get_sliced_prediction(
                    frame, sahi_model,
                    slice_height=256, slice_width=256,
                    overlap_height_ratio=0.2, overlap_width_ratio=0.2,
                    postprocess_type="NMS", postprocess_match_threshold=0.5,
                    verbose=0,
                )
                boxes = []
                for p in res.object_prediction_list:
                    if p.category.id == 0:
                        b = p.bbox
                        boxes.append({"x": int(b.minx), "y": int(b.miny),
                                      "w": int(b.maxx-b.minx), "h": int(b.maxy-b.miny),
                                      "conf": round(p.score.value, 3)})
                return boxes, "SAHI"
            except Exception:
                pass

        if model:
            results = model(frame, verbose=False)
            boxes = []
            for r in results:
                for box in r.boxes:
                    if int(box.cls[0]) == 0 and float(box.conf[0]) >= confidence:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        boxes.append({"x": int(x1), "y": int(y1),
                                      "w": int(x2-x1), "h": int(y2-y1),
                                      "conf": round(float(box.conf[0]), 3)})
            return boxes, "YOLO"

        return [], "none"

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": f"Không mở được: {video_path}"}

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps          = cap.get(cv2.CAP_PROP_FPS) or 30
    width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out_dir = os.path.join(output_dir, video_name)
    os.makedirs(out_dir, exist_ok=True)
    video_out_path = os.path.join(out_dir, f"annotated_{video_name}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out_video = cv2.VideoWriter(video_out_path, fourcc, fps, (width, height))

    frame_results = []
    total_persons = 0
    frame_no      = 0
    t_start       = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_no += 1
        boxes, method = _detect_frame(frame)
        count = len(boxes)
        total_persons += count

        for b in boxes:
            x, y, w, h = b["x"], b["y"], b["w"], b["h"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"P {b['conf']}", (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        cv2.putText(frame, f"Count: {count}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        out_video.write(frame)

        frame_results.append({
            "frame_no":       frame_no,
            "ts":             round(frame_no / fps, 3),
            "person_count":   count,
            "boxes":          boxes,
            "method":         method,
        })
        if frame_no % 100 == 0:
            print(f"  [{video_name}] {frame_no}/{total_frames} frames")

    cap.release()
    out_video.release()
    proc_s = time.time() - t_start

    with open(os.path.join(out_dir, "frame_detections.json"), "w") as f:
        json.dump(frame_results, f, indent=2)

    avg  = round(total_persons / frame_no, 2) if frame_no else 0
    mmax = max((r["person_count"] for r in frame_results), default=0)

    summary = {
        "video_name":  video_name,
        "video_path":  video_path,
        "video_info":  {"total_frames": total_frames, "fps": fps,
                        "resolution": f"{width}x{height}",
                        "duration_s": round(total_frames/fps, 2)},
        "detection":   {"total_persons": total_persons,
                        "frames_processed": frame_no,
                        "avg_persons_frame": avg,
                        "max_persons_frame": mmax,
                        "method": frame_results[0]["method"] if frame_results else "none"},
        "processing":  {"time_s": round(proc_s, 2),
                        "fps_proc": round(frame_no/proc_s, 2) if proc_s else 0,
                        "finished_at": datetime.now().isoformat()},
    }

    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    with open(os.path.join(out_dir, "report.txt"), "w", encoding="utf-8") as f:
        f.write(f"Báo cáo: {video_name}\n{'='*50}\n")
        f.write(f"Độ phân giải : {width}x{height}\n")
        f.write(f"FPS          : {fps}\n")
        f.write(f"Tổng frames  : {total_frames}\n")
        f.write(f"Thời lượng   : {round(total_frames/fps,2)}s\n\n")
        f.write(f"Phương pháp  : {summary['detection']['method']}\n")
        f.write(f"Tổng người   : {total_persons}\n")
        f.write(f"TB người/frame: {avg}\n")
        f.write(f"Max người/frame: {mmax}\n\n")
        f.write(f"Thời xử lý  : {round(proc_s,2)}s\n")
        f.write(f"Tốc độ      : {summary['processing']['fps_proc']} fps\n")

    return summary


def process_videos(video_paths: list, model_path: str,
                   output_dir: str, use_sahi: bool = True,
                   confidence: float = Config.CONFIDENCE,
                   use_spark: bool = True) -> list:
    args_list = [(vp, model_path, use_sahi, confidence, output_dir)
                 for vp in video_paths]

    if _SPARK_OK and use_spark and len(video_paths) > 1:
        import threading
        log.info("Khởi động PySpark – phân phối %d video ra các worker…",
                 len(video_paths))
        spark_results = []
        spark_error   = [None]

        def _run_spark():
            try:
                import sys, os
                os.environ["PYSPARK_PYTHON"] = sys.executable
                os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
                conf = (SparkConf()
                        .setAppName(Config.SPARK_APP)
                        .setMaster(Config.SPARK_MASTER))
                sc = SparkContext(conf=conf)
                sc.setLogLevel("ERROR")
                try:
                    rdd = sc.parallelize(args_list, len(video_paths))
                    spark_results.extend(rdd.map(process_single_video).collect())
                finally:
                    sc.stop()
            except Exception as exc:
                spark_error[0] = exc

        t = threading.Thread(target=_run_spark, daemon=True)
        t.start()
        t.join(timeout=180)

        if t.is_alive():
            log.warning("PySpark khởi động quá 180s – chuyển sang tuần tự.")
        elif spark_error[0]:
            log.warning("Spark lỗi (%s) – chuyển sang tuần tự.", spark_error[0])
        else:
            log.info("PySpark hoàn thành.")
            return spark_results

    log.info("Xử lý tuần tự %d video…", len(video_paths))
    return [process_single_video(a) for a in args_list]


def main():
    p = argparse.ArgumentParser(
        description="Batch processor: xử lý nhiều video bằng PySpark")
    p.add_argument("--videos-dir", "-v",
                   default=os.path.join(Config.OUTPUT_DIR, "..", "data", "video"),
                   help="Thư mục chứa video")
    p.add_argument("--output-dir", "-o",
                   default=os.path.join(Config.OUTPUT_DIR, "results"),
                   help="Thư mục lưu kết quả")
    p.add_argument("--model",      "-m", default=Config.MODEL_PATH)
    p.add_argument("--no-sahi",    action="store_true")
    p.add_argument("--no-spark",   action="store_true", help="Tắt PySpark, xử lý tuần tự")
    p.add_argument("--confidence", "-c", type=float, default=Config.CONFIDENCE)
    args = p.parse_args()

    videos_dir = os.path.abspath(args.videos_dir)
    output_dir = os.path.abspath(args.output_dir)

    exts = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
    video_paths = sorted([
        os.path.join(videos_dir, f)
        for f in os.listdir(videos_dir)
        if Path(f).suffix.lower() in exts
    ]) if os.path.isdir(videos_dir) else []

    if not video_paths:
        log.error("Không tìm thấy video trong: %s", videos_dir)
        sys.exit(1)

    log.info("Tìm thấy %d video:", len(video_paths))
    for vp in video_paths:
        log.info("  • %s", os.path.basename(vp))

    os.makedirs(output_dir, exist_ok=True)

    use_sahi  = not args.no_sahi
    use_spark = not args.no_spark
    log.info("Chế độ: %s | Confidence: %.2f | Spark: %s",
             "SAHI+YOLO" if use_sahi else "YOLO", args.confidence,
             "có" if (_SPARK_OK and use_spark) else "không")

    t0      = datetime.now()
    results = process_videos(video_paths, args.model,
                             output_dir, use_sahi, args.confidence, use_spark)
    total_s = (datetime.now() - t0).total_seconds()

    overall = {
        "info": {
            "total_videos":   len(video_paths),
            "total_time_s":   round(total_s, 2),
            "method":         "SAHI+YOLO" if use_sahi else "YOLO",
            "spark":          _SPARK_OK,
            "finished_at":    datetime.now().isoformat(),
        },
        "videos": results,
    }
    summary_file = os.path.join(output_dir, "overall_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(overall, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print("  KẾT QUẢ XỬ LÝ HÀNG LOẠT")
    print(f"{'='*60}")
    print(f"  Số video    : {len(video_paths)}")
    print(f"  Tổng thời gian: {total_s:.2f}s")
    for r in results:
        if "error" not in r:
            d = r.get("detection", {})
            print(f"  • {r['video_name']}: "
                  f"{d.get('total_persons',0)} người, "
                  f"TB {d.get('avg_persons_frame',0)}/frame")
    print(f"  Kết quả: {output_dir}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
