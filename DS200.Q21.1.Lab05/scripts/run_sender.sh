#!/usr/bin/env bash
# run_sender.sh
cd "$(dirname "$0")/../src" && python sender.py "$@"
