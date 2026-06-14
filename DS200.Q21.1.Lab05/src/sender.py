import argparse
import base64
import json
import logging
import socket
import time
import uuid
from datetime import datetime

try:
    import cv2
    import numpy as np
    _CV2 = True
except ImportError:
    _CV2 = False

from config import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FMT)
log = logging.getLogger("Sender")


def _encode_frame(frame) -> str:
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
    return base64.b64encode(buf).decode("ascii")


def _make_synthetic(frame_no: int):
    img = np.full((480, 640, 3), 40, np.uint8)
    cv2.putText(img, f"Synthetic #{frame_no}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (200, 200, 200), 2)
    rng = np.random.default_rng(frame_no)
    for _ in range(int(rng.integers(1, 5))):
        x, y = int(rng.integers(40, 500)), int(rng.integers(80, 300))
        cv2.rectangle(img, (x, y), (x + 55, y + 130), (0, 255, 0), 2)
    return img


class FrameSender:

    def __init__(self, source=None, fps: int = 2,
                 host: str = Config.HOST, port: int = Config.RECEIVER_PORT):
        self.source = source
        self.fps    = max(fps, 1)
        self.host   = host
        self.port   = port
        self._sock  = None
        self._cap   = None
        self._synthetic = (source is None) or (not _CV2)

    def _connect(self) -> bool:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.connect((self.host, self.port))
            log.info("Đã kết nối đến Receiver %s:%d", self.host, self.port)
            return True
        except ConnectionRefusedError:
            log.error("Receiver chưa khởi động tại %s:%d. "
                      "Hãy chạy receiver.py trước.", self.host, self.port)
            return False

    def _open_capture(self) -> None:
        if self._synthetic or not _CV2:
            self._synthetic = True
            return
        self._cap = cv2.VideoCapture(self.source)
        if not self._cap.isOpened():
            log.warning("Không mở được nguồn '%s'. Chuyển sang frame giả.", self.source)
            self._synthetic = True
            self._cap = None

    def _next_frame(self, frame_no: int):
        if self._synthetic:
            return _make_synthetic(frame_no)
        ok, frame = self._cap.read()
        if not ok:
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self._cap.read()
        return frame if ok else _make_synthetic(frame_no)

    def stream(self, total=None) -> None:
        if not self._connect():
            return

        self._open_capture()

        interval = 1.0 / self.fps
        sent     = 0

        log.info("Bắt đầu stream – %d fps, tổng %s frame",
                 self.fps, str(total) if total else "∞")

        try:
            while True:
                if total is not None and sent >= total:
                    break

                t0       = time.perf_counter()
                sent    += 1
                frame    = self._next_frame(sent)
                encoded  = _encode_frame(frame)

                msg = json.dumps({
                    "type": "frame",
                    "id":   str(uuid.uuid4()),
                    "no":   sent,
                    "ts":   datetime.now().isoformat(),
                    "data": encoded,
                }) + "\n"

                try:
                    self._sock.sendall(msg.encode())
                    log.info("  → Frame #%d đã gửi", sent)
                except (BrokenPipeError, OSError):
                    log.error("Mất kết nối đến Receiver.")
                    break

                elapsed = time.perf_counter() - t0
                wait    = interval - elapsed
                if wait > 0:
                    time.sleep(wait)

        except KeyboardInterrupt:
            log.info("Người dùng dừng Sender.")
        finally:
            self._close()
            log.info("Sender kết thúc – đã gửi %d frame.", sent)

    def _close(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
        if self._cap:
            self._cap.release()


def main():
    p = argparse.ArgumentParser(description="Gửi frames video đến Receiver")
    grp = p.add_mutually_exclusive_group()
    grp.add_argument("--video",     "-v", metavar="PATH",
                     help="Đường dẫn file video")
    grp.add_argument("--camera",    "-c", type=int, metavar="IDX",
                     help="Chỉ số camera (VD: 0)")
    grp.add_argument("--synthetic", "-s", action="store_true",
                     help="Dùng frame giả (không cần camera)")
    p.add_argument("--fps",    "-f", type=int, default=2,
                   help="Tốc độ gửi (frames/giây, mặc định: 2)")
    p.add_argument("--frames", "-n", type=int, default=None,
                   help="Số frame tối đa (mặc định: vô hạn)")
    p.add_argument("--host",   default=Config.HOST)
    p.add_argument("--port",   "-p", type=int, default=Config.RECEIVER_PORT)
    args = p.parse_args()

    if args.video:
        source = args.video
    elif args.camera is not None:
        source = args.camera
    else:
        source = None

    sender = FrameSender(source=source, fps=args.fps,
                         host=args.host, port=args.port)
    sender.stream(total=args.frames)


if __name__ == "__main__":
    main()
