#!/usr/bin/env bash
# run_detector.sh
cd "$(dirname "$0")/../src" && python detector.py "$@"
