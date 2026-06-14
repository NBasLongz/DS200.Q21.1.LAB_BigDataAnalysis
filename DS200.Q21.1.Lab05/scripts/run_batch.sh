#!/usr/bin/env bash
# run_batch.sh – Xử lý hàng loạt video bằng PySpark
cd "$(dirname "$0")/../src" && python batch_processor.py "$@"
