#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="$ROOT/spark"
DATA_DIR="${1:-$ROOT/data}"
OUT_DIR="${2:-$ROOT/output}"
JAR="$PROJECT/target/lab04-dataframe-1.0.0.jar"

mkdir -p "$OUT_DIR"

if ! command -v mvn >/dev/null 2>&1; then
  echo "ERROR: Maven is not installed or not on PATH." >&2
  exit 1
fi

if ! command -v spark-submit >/dev/null 2>&1; then
  echo "ERROR: spark-submit is not installed or not on PATH." >&2
  exit 1
fi

echo "[1/2] Building Maven project..."
(cd "$PROJECT" && mvn -q -DskipTests package)

echo "[2/2] Running Spark DataFrame tasks..."
declare -A TASKS=(
  [1]="ds200.lab04.task1.Task1App task1_load_datasets.txt"
  [2]="ds200.lab04.task2.Task2App task2_overall_stats.txt"
  [3]="ds200.lab04.task3.Task3App task3_orders_by_country.txt"
  [4]="ds200.lab04.task4.Task4App task4_orders_by_year_month.txt"
  [5]="ds200.lab04.task5.Task5App task5_review_stats.txt"
  [6]="ds200.lab04.task6.Task6App task6_revenue_2024_by_category.txt"
  [8]="ds200.lab04.task8.Task8App task8_delivery_performance.txt"
  [9]="ds200.lab04.task9.Task9App task9_customer_segments.txt"
)

for id in 1 2 3 4 5 6 8 9; do
  read -r CLASS FILE <<< "${TASKS[$id]}"
  echo "------------------------------------------------------------"
  echo "Running Task $id -> $OUT_DIR/$FILE"
  spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class "$CLASS" "$JAR" "$DATA_DIR" "$OUT_DIR/$FILE"
done

echo "Done. Reports are in: $OUT_DIR"
