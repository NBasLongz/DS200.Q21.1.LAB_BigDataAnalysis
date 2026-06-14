#!/usr/bin/env bash
# run_receiver.sh
cd "$(dirname "$0")/../src" && python receiver.py "$@"
