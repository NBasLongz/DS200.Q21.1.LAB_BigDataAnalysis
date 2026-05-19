# DS200 Lab04 - Fecom E-commerce Analytics with Spark DataFrame

This project solves Lab04 using **Java + Apache Spark DataFrame**. It implements the tasks available in the current codebase: 1-6, 8, and 9.

## Implemented tasks

| Task | Requirement | Output file |
|---:|---|---|
| 1 | Read all CSV files with inferred schema | `output/task1_load_datasets.txt` |
| 2 | Count total orders, unique customers, unique sellers | `output/task2_overall_stats.txt` |
| 3 | Analyze number of orders by country, sorted descending | `output/task3_orders_by_country.txt` |
| 4 | Analyze orders by purchase year/month, year asc and month desc | `output/task4_orders_by_year_month.txt` |
| 5 | Average review score and review count by score level, handling NULL/outliers | `output/task5_review_stats.txt` |
| 6 | 2024 revenue by product category | `output/task6_revenue_2024_by_category.txt` |
| 8 | Delivery performance analysis | `output/task8_delivery_performance.txt` |
| 9 | Customer segmentation analysis | `output/task9_customer_segments.txt` |

## Folder structure

```text
DS200.Q21.1.Lab04/
├── README.md
├── data/
│   ├── README.md
│   ├── Orders.csv
│   ├── Customer_List.csv
│   ├── Order_Items.csv
│   ├── Products.csv
│   └── Order_Reviews.csv
├── notebook/
├── output/
├── screenshots/
├── scripts/
│   ├── run_all.sh
│   ├── run_one.sh
│   └── preview_outputs.sh
└── spark/
    ├── pom.xml
    ├── src/
    │   ├── common/
    │   │   ├── DatasetLoader.java
    │   │   ├── ReportWriter.java
    │   │   ├── SparkFactory.java
    │   │   ├── TableFormatter.java
    │   │   └── TaskArgs.java
    │   ├── task1/Task1App.java
    │   ├── task2/Task2App.java
    │   ├── task3/Task3App.java
    │   ├── task4/Task4App.java
    │   ├── task5/Task5App.java
    │   ├── task6/Task6App.java
    │   ├── task8/Task8App.java
    │   └── task9/Task9App.java
    └── target/
```

## Prerequisites

Recommended environment:

- Ubuntu / WSL2
- Java 11
- Apache Maven 3.6+
- Apache Spark 3.5.x with `spark-submit` on PATH

Check environment:

```bash
java -version
mvn -version
spark-submit --version
```

## Prepare data

Copy the five CSV files into the `data/` folder:

```bash
cp /path/to/Orders.csv data/
cp /path/to/Customer_List.csv data/
cp /path/to/Order_Items.csv data/
cp /path/to/Products.csv data/
cp /path/to/Order_Reviews.csv data/
```

## Run all tasks

From the root folder:

```bash
chmod +x scripts/*.sh
./scripts/run_all.sh
```

The script builds the Maven project and writes all reports to `output/`.

## Run one task

```bash
./scripts/run_one.sh 3
./scripts/run_one.sh 6
./scripts/run_one.sh 9
```

You can also pass a custom data directory and output directory:

```bash
./scripts/run_one.sh 5 /path/to/data /path/to/output
```

## Manual commands

```bash
cd spark
mvn -q -DskipTests package
cd ..

JAR=spark/target/lab04-dataframe-1.0.0.jar
DATA=data
OUT=output

spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task1.Task1App  $JAR $DATA $OUT/task1_load_datasets.txt
spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task2.Task2App  $JAR $DATA $OUT/task2_overall_stats.txt
spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task3.Task3App  $JAR $DATA $OUT/task3_orders_by_country.txt
spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task4.Task4App  $JAR $DATA $OUT/task4_orders_by_year_month.txt
spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task5.Task5App  $JAR $DATA $OUT/task5_review_stats.txt
spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task6.Task6App  $JAR $DATA $OUT/task6_revenue_2024_by_category.txt
spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task8.Task8App  $JAR $DATA $OUT/task8_delivery_performance.txt
spark-submit --master local[*] --conf spark.hadoop.fs.defaultFS=file:/// --class ds200.lab04.task9.Task9App  $JAR $DATA $OUT/task9_customer_segments.txt
```

## Notes on data cleaning

- The loader removes UTF-8 BOM from header names, so `Order_ID` is recognized correctly even if the CSV begins with BOM.
- Task 5 casts `Review_Score` to integer and keeps only scores from 1 to 5.
- Revenue is calculated as `Price + Freight_Value` with NULL values treated as 0.

## Screenshot suggestion

Run:

```bash
./scripts/preview_outputs.sh
```

Then take screenshots of each task output for submission.

