#!/usr/bin/env bash
# run_all.sh – Khởi động toàn bộ hệ thống (4 terminal riêng biệt)
# Yêu cầu: gnome-terminal (Ubuntu) hoặc osascript (macOS)
# Nếu không có GUI terminal, dùng tmux hoặc chạy thủ công từng lệnh.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/../src"

echo "========================================================"
echo "  Khởi động hệ thống đếm người – DS200 Lab05"
echo "========================================================"
echo "  SRC: $SRC_DIR"
echo ""

# Hàm tiện ích
_run_in_term() {
    local TITLE="$1"
    local CMD="$2"
    if command -v gnome-terminal &>/dev/null; then
        gnome-terminal --title="$TITLE" -- bash -c "$CMD; read -p 'Nhấn Enter để đóng...'"
    elif command -v xterm &>/dev/null; then
        xterm -title "$TITLE" -e bash -c "$CMD; read -p 'Press Enter...'" &
    elif command -v osascript &>/dev/null; then
        osascript -e "tell application \"Terminal\" to do script \"$CMD\""
    else
        echo "  [WARN] Không tìm thấy GUI terminal. Chạy thủ công:"
        echo "    $CMD"
    fi
}

echo "  [1/4] Storage server  (port 6300)..."
_run_in_term "Storage" "cd '$SRC_DIR' && python storage.py"
sleep 2

echo "  [2/4] Detector server (port 6200)..."
_run_in_term "Detector" "cd '$SRC_DIR' && python detector.py"
sleep 3

echo "  [3/4] Receiver server (port 6100)..."
_run_in_term "Receiver" "cd '$SRC_DIR' && python receiver.py"
sleep 2

echo ""
echo "  Tất cả server đã khởi động."
echo "  Chạy sender:"
echo "    cd $SRC_DIR"
echo "    python sender.py --video ../data/video/people.mp4 --fps 5"
echo "    python sender.py --synthetic --frames 30"
echo ""
echo "  Hoặc chạy demo tự động:"
echo "    python demo.py --frames 30"
echo "========================================================"
