#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/run_one.sh <task_id: 1|2|3|4|5|6|8|9> [data_dir] [output_dir]" >&2
  exit 1
fi

TASK_ID="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="$ROOT/spark"
DATA_DIR="${2:-$ROOT/data}"
OUT_DIR="${3:-$ROOT/output}"
JAR="$PROJECT/target/lab04-dataframe-1.0.0.jar"

mkdir -p "$OUT_DIR"
(cd "$PROJECT" && mvn -q -DskipTests package)

case "$TASK_ID" in
  1) CLASS="ds200.lab04.task1.Task1App"; FILE="task1_load_datasets.txt" ;;
  2) CLASS="ds200.lab04.task2.Task2App"; FILE="task2_overall_stats.txt" ;;
  3) CLASS="ds200.lab04.task3.Task3App"; FILE="task3_orders_by_country.txt" ;;
  4) CLASS="ds200.lab04.task4.Task4App"; FILE="task4_orders_by_year_month.txt" ;;
  5) CLASS="ds200.lab04.task5.Task5App"; FILE="task5_review_stats.txt" ;;
  6) CLASS="ds200.lab04.task6.Task6App"; FILE="task6_revenue_2024_by_category.txt" ;;
  8) CLASS="ds200.lab04.task8.Task8App"; FILE="task8_delivery_performance.txt" ;;
  9) CLASS="ds200.lab04.task9.Task9App"; FILE="task9_customer_segments.txt" ;;
  *) echo "Unknown task: $TASK_ID" >&2; exit 1 ;;
esac

spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class "$CLASS" "$JAR" "$DATA_DIR" "$OUT_DIR/$FILE"
