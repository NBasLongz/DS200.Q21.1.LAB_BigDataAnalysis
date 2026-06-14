import argparse
import json
import logging
import socket
import threading
from datetime import datetime

from config import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FMT)
log = logging.getLogger("Receiver")


class FrameReceiver:

    def __init__(self,
                 host: str = Config.HOST,
                 port: int = Config.RECEIVER_PORT):
        self.host       = host
        self.port       = port
        self._server    = None
        self._detector  = None
        self._lock      = threading.Lock()
        self._running   = False
        self._total_rx  = 0

    def _connect_detector(self) -> bool:
        with self._lock:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((Config.HOST, Config.DETECTOR_PORT))
                self._detector = s
                log.info("Đã kết nối đến Detector %s:%d",
                         Config.HOST, Config.DETECTOR_PORT)
                return True
            except ConnectionRefusedError:
                log.warning("Detector chưa sẵn sàng (port %d). "
                            "Frame sẽ bị bỏ qua.", Config.DETECTOR_PORT)
                self._detector = None
                return False

    def _forward(self, raw_json: str) -> None:
        with self._lock:
            if self._detector is None:
                return
            try:
                self._detector.sendall((raw_json + "\n").encode())
            except (BrokenPipeError, OSError):
                log.warning("Mất kết nối Detector. Đang thử kết nối lại…")
                try:
                    self._detector.close()
                except Exception:
                    pass
                self._detector = None

        if self._detector is None:
            self._connect_detector()

    def _handle_sender(self, conn: socket.socket, addr) -> None:
        log.info("Sender kết nối từ %s", addr)
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
                    if not line:
                        continue
                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError:
                        log.warning("JSON không hợp lệ từ %s – bỏ qua.", addr)
                        continue

                    if msg.get("type") == "frame":
                        self._total_rx += 1
                        log.info("← Frame #%s từ %s (tổng: %d)",
                                 msg.get("no", "?"), addr, self._total_rx)
                        self._forward(line)

        except Exception as exc:
            log.error("Lỗi xử lý sender %s: %s", addr, exc)
        finally:
            conn.close()
            log.info("Sender %s ngắt kết nối.", addr)

    def start(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(Config.MAX_CONNECTIONS if hasattr(Config, "MAX_CONNECTIONS") else 5)
        self._running = True

        log.info("  RECEIVER  đang lắng nghe %s:%d", self.host, self.port)

        self._connect_detector()

        try:
            while self._running:
                conn, addr = self._server.accept()
                t = threading.Thread(target=self._handle_sender,
                                     args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            log.info("Đang tắt Receiver…")
        finally:
            self.stop()

    def stop(self) -> None:
        self._running = False
        if self._server:
            try:
                self._server.close()
            except Exception:
                pass
        with self._lock:
            if self._detector:
                try:
                    self._detector.close()
                except Exception:
                    pass
        log.info("Receiver dừng. Tổng frame đã nhận: %d", self._total_rx)


def main():
    p = argparse.ArgumentParser(description="Receiver – nhận frame từ Sender")
    p.add_argument("--host", default=Config.HOST)
    p.add_argument("--port", "-p", type=int, default=Config.RECEIVER_PORT)
    args = p.parse_args()

    server = FrameReceiver(host=args.host, port=args.port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
