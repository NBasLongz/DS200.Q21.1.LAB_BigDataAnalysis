import argparse
import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime

_SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SRC)
from config import Config


def _banner():
    print()
    print("=" * 65)
    print("   HỆ THỐNG ĐẾM NGƯỜI THỜI GIAN THỰC – DS200.Q21.1 Lab 05")
    print("=" * 65)
    print(f"   Ngày   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Ports  : Storage={Config.STORAGE_PORT}  "
          f"Detector={Config.DETECTOR_PORT}  "
          f"Receiver={Config.RECEIVER_PORT}")
    print("=" * 65)
    print()
    print("  Kiến trúc:")
    print()
    print("  ┌─────────┐  TCP:6100  ┌──────────┐  TCP:6200  ┌──────────┐")
    print("  │  Sender │──────────►│ Receiver │──────────►│ Detector │")
    print("  └─────────┘           └──────────┘           └────┬─────┘")
    print("                                                     │ TCP:6300")
    print("                                                     ▼")
    print("                                               ┌──────────┐")
    print("                                               │ Storage  │")
    print("                                               └────┬─────┘")
    print("                                                    │")
    print("                                                    ▼")
    print("                                          output/detections.json")
    print()


_log_handles = []


def _start(script: str, extra_args: list = None, delay: float = 2.0):
    path = os.path.join(_SRC, script)
    if not os.path.exists(path):
        print(f"  ✗ Không tìm thấy: {path}")
        return None

    cmd = [sys.executable, path] + (extra_args or [])
    log_path = os.path.join(Config.OUTPUT_DIR, f"{script.replace('.py', '')}.log")
    log_file = open(log_path, "w", encoding="utf-8")
    _log_handles.append(log_file)
    proc = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=_SRC,
    )
    time.sleep(delay)

    if proc.poll() is None:
        print(f"  ✔ {script} đã khởi động (PID {proc.pid})")
        return proc
    else:
        log_file.flush()
        with open(log_path, "r", encoding="utf-8") as f:
            out = f.read(300)
        print(f"  ✗ {script} khởi động thất bại:")
        print(out)
        return None


def _wait_port(host: str, port: int, timeout: float = 60.0, interval: float = 1.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(interval)
    return False


def _stop_all(procs: list):
    print("\n  Đang tắt các server…")
    for name, proc in procs:
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=4)
                print(f"  ✔ {name} đã tắt")
            except subprocess.TimeoutExpired:
                proc.kill()
                print(f"  ✔ {name} đã kill")


def _show_results(results_file: str):
    print("  KẾT QUẢ")

    if not os.path.exists(results_file):
        print(f"  ✗ Chưa có file kết quả ({results_file})")
        return

    try:
        with open(results_file, encoding="utf-8") as f:
            results = json.load(f)
    except Exception as exc:
        print(f"  ✗ Đọc file lỗi: {exc}")
        return

    if not results:
        print("  (Không có kết quả nào)")
        return

    print(f"  Tổng frame đã xử lý: {len(results)}")
    print(f"\n  5 frame cuối:")
    for r in results[-5:]:
        print(f"    Frame #{r.get('frame_no','?'):>4}  "
              f"| {r.get('person_count',0):>2} người "
              f"| {r.get('method','?'):<5} "
              f"| {r.get('ms',0):.1f} ms")

    total_p = sum(r.get("person_count", 0) for r in results)
    avg     = total_p / len(results) if results else 0
    print(f"\n  Tổng người phát hiện : {total_p}")
    print(f"  Trung bình / frame   : {avg:.2f}")
    print(f"\n  File kết quả         : {results_file}")


def run_test():
    print("Kiểm tra môi trường…\n")
    checks = [
        ("config",        "Cấu hình"),
        ("sender",        "Sender"),
        ("receiver",      "Receiver"),
        ("detector",      "Detector"),
        ("storage",       "Storage"),
        ("batch_processor", "Batch Processor"),
    ]
    for mod, name in checks:
        try:
            __import__(mod)
            print(f"  ✔ {name}")
        except ImportError as exc:
            print(f"  ✗ {name}: {exc}")

    print("\n  Thư viện tuỳ chọn:")
    opts = [
        ("cv2",          "OpenCV"),
        ("numpy",        "NumPy"),
        ("ultralytics",  "YOLO (Ultralytics)"),
        ("sahi",         "SAHI"),
        ("mediapipe",    "MediaPipe"),
        ("pyspark",      "PySpark"),
    ]
    for mod, name in opts:
        try:
            __import__(mod)
            print(f"  ✔ {name}")
        except ImportError:
            print(f"  ⚠ {name} – không có (tuỳ chọn)")

    print(f"\n  Cấu hình:")
    print(f"    Receiver  port: {Config.RECEIVER_PORT}")
    print(f"    Detector  port: {Config.DETECTOR_PORT}")
    print(f"    Storage   port: {Config.STORAGE_PORT}")
    print(f"    Model     path: {Config.MODEL_PATH}")
    print(f"    Confidence    : {Config.CONFIDENCE}")


def run_demo(num_frames: int = 20, video_path: str = None):
    _banner()
    procs = []

    try:
        print("[1/3] Khởi động Storage server…")
        s = _start("storage.py", delay=1.5)
        if not s:
            print("Không thể tiếp tục.")
            return False
        procs.append(("storage.py", s))
        if not _wait_port(Config.HOST, Config.STORAGE_PORT, timeout=15):
            print("  ✗ Storage không lắng nghe sau 15s.")
            _stop_all(procs)
            return False
        print(f"  ✔ Storage sẵn sàng tại cổng {Config.STORAGE_PORT}")

        print("[2/3] Khởi động Detector server…")
        d = _start("detector.py", extra_args=["--no-sahi"], delay=1.5)
        if not d:
            print("Không thể tiếp tục.")
            _stop_all(procs)
            return False
        procs.append(("detector.py", d))
        print("  ⏳ Đang chờ Detector load YOLO model (tối đa 120s)…")
        if not _wait_port(Config.HOST, Config.DETECTOR_PORT, timeout=120):
            print("  ✗ Detector không lắng nghe sau 120s.")
            _stop_all(procs)
            return False
        print(f"  ✔ Detector sẵn sàng tại cổng {Config.DETECTOR_PORT}")

        print("[3/3] Khởi động Receiver server…")
        r = _start("receiver.py", delay=1.5)
        if not r:
            print("Không thể tiếp tục.")
            _stop_all(procs)
            return False
        procs.append(("receiver.py", r))
        if not _wait_port(Config.HOST, Config.RECEIVER_PORT, timeout=15):
            print("  ✗ Receiver không lắng nghe sau 15s.")
            _stop_all(procs)
            return False
        print(f"  ✔ Receiver sẵn sàng tại cổng {Config.RECEIVER_PORT}")

        print("\nTất cả server đã sẵn sàng. Bắt đầu gửi frames…\n")
        print("-" * 65)

        sender_args = ["--frames", str(num_frames), "--fps", "2"]
        if video_path:
            sender_args += ["--video", video_path]
        else:
            sender_args.append("--synthetic")

        sender_proc = subprocess.Popen(
            [sys.executable, os.path.join(_SRC, "sender.py")] + sender_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=_SRC,
            text=True,
        )
        for line in sender_proc.stdout:
            print(f"  [Sender] {line.rstrip()}")
        sender_proc.wait()

        print("\n  Đang chờ pipeline hoàn tất…")
        time.sleep(3)

        _show_results(Config.RESULTS_FILE)
        return True

    except KeyboardInterrupt:
        print("\n\n  Demo bị ngắt bởi người dùng.")
        return False

    finally:
        _stop_all(procs)
        for fh in _log_handles:
            try:
                fh.close()
            except Exception:
                pass
        print(f"\n{'='*65}")
        print("  Demo kết thúc.")
        print(f"{'='*65}\n")


def main():
    p = argparse.ArgumentParser(description="Demo – chạy toàn bộ hệ thống")
    p.add_argument("--frames", "-n", type=int, default=20,
                   help="Số frame gửi (mặc định: 20)")
    p.add_argument("--video",  "-v", help="Đường dẫn file video (tuỳ chọn)")
    p.add_argument("--test",   "-t", action="store_true",
                   help="Chỉ kiểm tra dependencies, không chạy demo")
    args = p.parse_args()

    if args.test:
        run_test()
        return

    video = os.path.abspath(args.video) if args.video else None
    ok    = run_demo(num_frames=args.frames, video_path=video)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
