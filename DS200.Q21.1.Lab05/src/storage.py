import argparse
import json
import logging
import os
import socket
import threading
from datetime import datetime

from config import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FMT)
log = logging.getLogger("Storage")


class StorageServer:

    def __init__(self,
                 host: str = Config.HOST,
                 port: int = Config.STORAGE_PORT,
                 out_file: str = Config.RESULTS_FILE):
        self.host     = host
        self.port     = port
        self.out_file = out_file
        self._server  = None
        self._running = False
        self._results = []
        self._lock    = threading.Lock()
        self._total   = 0
        self._persons = 0

        self._init_storage()

    def _init_storage(self) -> None:
        os.makedirs(os.path.dirname(self.out_file) or ".", exist_ok=True)

        if os.path.exists(self.out_file):
            try:
                with open(self.out_file, encoding="utf-8") as f:
                    self._results = json.load(f)
                self._total   = len(self._results)
                self._persons = sum(r.get("person_count", 0)
                                    for r in self._results)
                log.info("Đã tải %d kết quả cũ từ %s",
                         self._total, self.out_file)
            except Exception:
                self._results = []

    def _store(self, result: dict) -> None:
        result["saved_at"] = datetime.now().isoformat()
        with self._lock:
            self._results.append(result)
            self._total   += 1
            self._persons += result.get("person_count", 0)
            self._persist()

        self._print_result(result)

    def _persist(self) -> None:
        try:
            tmp = self.out_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._results, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.out_file)
        except Exception as exc:
            log.error("Ghi file thất bại: %s", exc)

    def _print_result(self, r: dict) -> None:
        print(f"  Frame #{r.get('frame_no', '?')} | "
              f"ID: {str(r.get('frame_id', ''))[:8]}…")
        print(f"  Thời gian  : {r.get('ts', '')}")
        print(f"  Số người   : {r.get('person_count', 0)}")
        print(f"  Phương pháp: {r.get('method', '?')}")
        print(f"  Thời xử lý : {r.get('ms', 0):.1f} ms")
        if r.get("boxes"):
            print("  Bounding boxes:")
            for i, b in enumerate(r["boxes"], 1):
                print(f"    [{i}] x={b['x']}, y={b['y']}, "
                      f"w={b['w']}, h={b['h']}, conf={b['conf']:.3f}")
        print(f"  ── Tổng tích luỹ: {self._total} frame, "
              f"{self._persons} lượt người ──")

    def _handle_detector(self, conn: socket.socket, addr) -> None:
        log.info("Detector kết nối từ %s", addr)
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
                        log.warning("JSON không hợp lệ – bỏ qua.")
                        continue

                    if msg.get("type") == "result":
                        self._store(msg)
                    else:
                        log.debug("Bỏ qua message type=%s", msg.get("type"))
        except Exception as exc:
            log.error("Lỗi xử lý detector %s: %s", addr, exc)
        finally:
            conn.close()
            log.info("Detector %s ngắt kết nối.", addr)

    def start(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(5)
        self._running = True

        _sep = "=" * 60
        log.info(_sep)
        log.info("  STORAGE  đang lắng nghe %s:%d", self.host, self.port)
        log.info("  Kết quả sẽ ghi vào: %s", self.out_file)
        log.info(_sep)

        try:
            while self._running:
                conn, addr = self._server.accept()
                t = threading.Thread(target=self._handle_detector,
                                     args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            log.info("Đang tắt Storage…")
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
            self._persist()

        avg = self._persons / self._total if self._total else 0
        log.info("Storage dừng. Tổng: %d frame | %d người | "
                 "TB %.2f người/frame",
                 self._total, self._persons, avg)
        log.info("File kết quả: %s", self.out_file)

    def statistics(self) -> dict:
        with self._lock:
            total = self._total
            persons = self._persons
        return {
            "total_frames":       total,
            "total_persons":      persons,
            "avg_persons_frame":  round(persons / total, 2) if total else 0,
        }


def main():
    p = argparse.ArgumentParser(description="Storage – lưu kết quả nhận diện")
    p.add_argument("--host", default=Config.HOST)
    p.add_argument("--port", "-p", type=int, default=Config.STORAGE_PORT)
    p.add_argument("--out",  "-o", default=Config.RESULTS_FILE,
                   help="File JSON lưu kết quả")
    args = p.parse_args()

    server = StorageServer(host=args.host, port=args.port, out_file=args.out)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
