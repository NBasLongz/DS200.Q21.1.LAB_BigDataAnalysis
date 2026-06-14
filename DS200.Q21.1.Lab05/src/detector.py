import argparse
import base64
import json
import logging
import socket
import threading
import time
import uuid
from datetime import datetime

from config import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FMT)
log = logging.getLogger("Detector")

try:
    import cv2
    import numpy as np
    _CV2 = True
except ImportError:
    _CV2 = False
    log.warning("OpenCV không khả dụng – dùng mock detection.")

try:
    from ultralytics import YOLO as _YOLO
    _YOLO_OK = True
except ImportError:
    _YOLO_OK = False
    log.warning("Ultralytics YOLO không khả dụng – dùng mock detection.")

try:
    from sahi import AutoDetectionModel
    from sahi.predict import get_sliced_prediction
    _SAHI_OK = True
except ImportError:
    _SAHI_OK = False

try:
    from pyspark import SparkContext, SparkConf
    from pyspark.streaming import StreamingContext
    _SPARK_OK = True
except ImportError:
    _SPARK_OK = False


class PersonDetector:

    def __init__(self, model_path: str = Config.MODEL_PATH,
                 confidence: float = Config.CONFIDENCE,
                 use_sahi: bool = True):
        self.model_path = model_path
        self.confidence = confidence
        self.use_sahi   = use_sahi and _SAHI_OK
        self._model     = None
        self._sahi_mdl  = None
        self._load()

    def _load(self) -> None:
        if not _YOLO_OK:
            log.warning("YOLO không có – sẽ dùng mock detection.")
            return
        try:
            self._model = _YOLO(self.model_path)
            log.info("YOLO model: %s", self.model_path)
        except Exception as exc:
            log.warning("Không tải được YOLO model (%s). Dùng mock.", exc)
            self._model = None
            return

        if self.use_sahi:
            try:
                self._sahi_mdl = AutoDetectionModel.from_pretrained(
                    model_type="yolov8",
                    model_path=self.model_path,
                    confidence_threshold=self.confidence,
                    device="cpu",
                )
                log.info("SAHI sliced inference: BẬT")
            except Exception as exc:
                log.warning("Không khởi tạo được SAHI (%s). Dùng YOLO thuần.", exc)
                self._sahi_mdl = None

    def run(self, b64_data: str) -> dict:
        if not _CV2:
            return self._mock()

        try:
            raw    = base64.b64decode(b64_data)
            arr    = np.frombuffer(raw, np.uint8)
            image  = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        except Exception as exc:
            log.error("Giải mã ảnh thất bại: %s", exc)
            return self._mock()

        if image is None:
            return self._mock()

        if self._sahi_mdl:
            return self._detect_sahi(image)
        if self._model:
            return self._detect_yolo(image)
        return self._mock()

    def _detect_yolo(self, image) -> dict:
        results = self._model(image, verbose=False)
        boxes   = []
        for r in results:
            for box in r.boxes:
                cls  = int(box.cls[0])
                conf = float(box.conf[0])
                if cls == Config.PERSON_CLS and conf >= self.confidence:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    boxes.append({
                        "x": int(x1), "y": int(y1),
                        "w": int(x2 - x1), "h": int(y2 - y1),
                        "conf": round(conf, 3),
                    })
        return {"person_count": len(boxes), "boxes": boxes, "method": "YOLO"}

    def _detect_sahi(self, image) -> dict:
        try:
            result = get_sliced_prediction(
                image, self._sahi_mdl,
                slice_height=256, slice_width=256,
                overlap_height_ratio=0.2, overlap_width_ratio=0.2,
                postprocess_type="NMS", postprocess_match_threshold=0.5,
                verbose=0,
            )
            boxes = []
            for pred in result.object_prediction_list:
                if pred.category.id == Config.PERSON_CLS:
                    bb   = pred.bbox
                    conf = pred.score.value
                    boxes.append({
                        "x": int(bb.minx), "y": int(bb.miny),
                        "w": int(bb.maxx - bb.minx),
                        "h": int(bb.maxy - bb.miny),
                        "conf": round(conf, 3),
                    })
            return {"person_count": len(boxes), "boxes": boxes, "method": "SAHI"}
        except Exception as exc:
            log.error("SAHI lỗi (%s). Chuyển sang YOLO thuần.", exc)
            return self._detect_yolo(image)

    @staticmethod
    def _mock() -> dict:
        import random
        n = random.randint(0, 4)
        boxes = [{"x": random.randint(50, 400), "y": random.randint(50, 300),
                  "w": 55, "h": 130,
                  "conf": round(random.uniform(0.60, 0.95), 3)}
                 for _ in range(n)]
        return {"person_count": n, "boxes": boxes, "method": "mock"}


class DetectorServer:

    def __init__(self, host: str = Config.HOST,
                 port: int = Config.DETECTOR_PORT,
                 use_sahi: bool = True,
                 use_spark: bool = False):
        self.host       = host
        self.port       = port
        self.detector   = PersonDetector(use_sahi=use_sahi)
        self._server    = None
        self._storage   = None
        self._lock      = threading.Lock()
        self._running   = False
        self._processed = 0
        self._use_spark = use_spark and _SPARK_OK
        self._sc  = None
        self._ssc = None
        if self._use_spark:
            self._init_spark()

    def _init_spark(self) -> None:
        try:
            import sys, os
            os.environ["PYSPARK_PYTHON"] = sys.executable
            os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
            conf = (SparkConf()
                    .setAppName(Config.SPARK_APP)
                    .setMaster(Config.SPARK_MASTER))
            self._sc  = SparkContext(conf=conf)
            self._sc.setLogLevel("ERROR")
            self._ssc = StreamingContext(self._sc, Config.SPARK_BATCH_S)
            log.info("PySpark StreamingContext khởi tạo thành công.")
        except Exception as exc:
            log.warning("Không khởi tạo được Spark (%s). Dùng threading.", exc)
            self._use_spark = False

    def _connect_storage(self) -> bool:
        with self._lock:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((Config.HOST, Config.STORAGE_PORT))
                self._storage = s
                log.info("Đã kết nối đến Storage %s:%d",
                         Config.HOST, Config.STORAGE_PORT)
                return True
            except ConnectionRefusedError:
                log.warning("Storage chưa sẵn sàng. Kết quả sẽ bị bỏ qua.")
                self._storage = None
                return False

    def _send_result(self, result_json: str) -> None:
        with self._lock:
            if self._storage is None:
                return
            try:
                self._storage.sendall((result_json + "\n").encode())
            except (BrokenPipeError, OSError):
                log.warning("Mất kết nối Storage. Đang thử lại…")
                try:
                    self._storage.close()
                except Exception:
                    pass
                self._storage = None

        if self._storage is None:
            self._connect_storage()

    def _process_frame(self, raw_json: str) -> None:
        try:
            msg = json.loads(raw_json)
        except json.JSONDecodeError:
            log.warning("JSON không hợp lệ – bỏ qua.")
            return

        frame_id = msg.get("id", str(uuid.uuid4()))
        frame_no = msg.get("no", 0)
        b64_data = msg.get("data", "")

        log.info("Đang xử lý frame #%d …", frame_no)
        t0 = time.perf_counter()

        detection = self.detector.run(b64_data)

        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
        self._processed += 1

        count  = detection["person_count"]
        method = detection["method"]
        log.info("  ✔ %d người [%s] trong %.1f ms", count, method, elapsed_ms)

        result = {
            "type":         "result",
            "frame_id":     frame_id,
            "frame_no":     frame_no,
            "ts":           datetime.now().isoformat(),
            "person_count": count,
            "boxes":        detection["boxes"],
            "method":       method,
            "ms":           elapsed_ms,
        }
        self._send_result(json.dumps(result))

    def _handle_receiver(self, conn: socket.socket, addr) -> None:
        log.info("Receiver kết nối từ %s", addr)
        buf = ""
        try:
            while self._running:
                chunk = conn.recv(Config.RECV_BYTES)
                if not chunk:
                    break
                buf += chunk.decode("utf-8", errors="replace")

                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if line:
                        self._process_frame(line)
        except Exception as exc:
            log.error("Lỗi xử lý receiver %s: %s", addr, exc)
        finally:
            conn.close()
            log.info("Receiver %s ngắt kết nối.", addr)

    def start(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(5)
        self._running = True

        _method = "SAHI + YOLO" if self.detector._sahi_mdl else \
                  ("YOLO" if self.detector._model else "mock")
        _sep = "=" * 60
        log.info(_sep)
        log.info("  DETECTOR  đang lắng nghe %s:%d", self.host, self.port)
        log.info("  Phương pháp: %s | Spark: %s",
                 _method, "BẬT" if self._use_spark else "TẮT")
        log.info(_sep)

        self._connect_storage()

        try:
            while self._running:
                conn, addr = self._server.accept()
                t = threading.Thread(target=self._handle_receiver,
                                     args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            log.info("Đang tắt Detector…")
        finally:
            self.stop()

    def stop(self) -> None:
        self._running = False
        if self._ssc:
            try:
                self._ssc.stop(stopSparkContext=True, stopGraceFully=True)
            except Exception:
                pass
        if self._server:
            try:
                self._server.close()
            except Exception:
                pass
        with self._lock:
            if self._storage:
                try:
                    self._storage.close()
                except Exception:
                    pass
        log.info("Detector dừng. Tổng frame đã xử lý: %d", self._processed)


def main():
    p = argparse.ArgumentParser(description="Detector – nhận diện người bằng YOLO")
    p.add_argument("--host",     default=Config.HOST)
    p.add_argument("--port",     "-p", type=int, default=Config.DETECTOR_PORT)
    p.add_argument("--spark",    action="store_true",
                   help="Bật PySpark Streaming")
    p.add_argument("--no-sahi",  action="store_true",
                   help="Tắt SAHI (chỉ dùng YOLO thuần, nhanh hơn)")
    args = p.parse_args()

    server = DetectorServer(
        host=args.host, port=args.port,
        use_sahi=not args.no_sahi,
        use_spark=args.spark,
    )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
