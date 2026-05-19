#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT/output}"

for file in "$OUT_DIR"/*.txt; do
  [ -e "$file" ] || continue
  clear || true
  echo "============================================================"
  echo "File: $(basename "$file")"
  echo "============================================================"
  sed -n '1,80p' "$file"
  echo
  read -r -p "Press Enter to continue..." _
done
