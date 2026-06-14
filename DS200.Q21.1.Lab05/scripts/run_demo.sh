#!/usr/bin/env bash
# run_demo.sh – Chạy demo tự động (khởi tất cả server + sender)
cd "$(dirname "$0")/../src" && python demo.py "$@"
