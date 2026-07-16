import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, round, asc

def load_csv(spark, path):
    df = spark.read.option("header", "true") \
                   .option("sep", ";") \
                   .option("inferSchema", "true") \
                   .option("encoding", "UTF-8") \
                   .option("quote", '"') \
                   .option("escape", '"') \
                   .option("multiLine", "true") \
                   .option("mode", "PERMISSIVE") \
                   .csv(path)
    for col_name in df.columns:
        clean_name = col_name.replace("\uFEFF", "").strip()
        if clean_name != col_name:
            df = df.withColumnRenamed(col_name, clean_name)
    return df

def to_lines(df, max_rows):
    import datetime
    import builtins
    columns = df.columns
    rows = df.limit(max_rows).collect()
    
    widths = [len(col) for col in columns]
    values = []
    
    for row in rows:
        current = []
        for i in range(len(columns)):
            val = row[i]
            if val is None:
                val_str = "NULL"
            elif isinstance(val, datetime.datetime):
                val_str = val.strftime("%Y-%m-%d %H:%M:%S.0")
            else:
                val_str = str(val)
            current.append(val_str)
            widths[i] = builtins.max(widths[i], builtins.min(len(val_str), 60))
        values.append(current)
        
    def truncate(s, max_len=60):
        if s == "NULL":
            return "NULL"
        if len(s) <= max_len:
            return s
        return s[:max_len - 3] + "..."
        
    def pad_right(s, w):
        return f"{truncate(s):<{w}}"
        
    out = []
    header_parts = [pad_right(col, widths[i]) for i, col in enumerate(columns)]
    out.append(" | ".join(header_parts))
    
    sep_parts = ["-" * builtins.max(1, w) for w in widths]
    out.append("-+-".join(sep_parts))
    
    for row in values:
        row_parts = [pad_right(val, widths[i]) for i, val in enumerate(row)]
        out.append(" | ".join(row_parts))
        
    return out

spark = SparkSession.builder.appName("Lab04_Task5").master("local[*]").getOrCreate()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
DATA_DIR = BASE_DIR + "/"

reviews_df = load_csv(spark, DATA_DIR + "Order_Reviews.csv")

clean_reviews = reviews_df \
    .withColumn("Review_Score_Clean", col("Review_Score").cast("int")) \
    .filter(col("Review_Score_Clean").isNotNull() & col("Review_Score_Clean").between(1, 5))

total_rows = reviews_df.count()
valid_rows = clean_reviews.count()
invalid_or_null_rows = total_rows - valid_rows

overall = clean_reviews.agg(
    round(avg("Review_Score_Clean"), 4).alias("Average_Review_Score"),
    count("Review_Score_Clean").alias("Valid_Review_Count")
).first()

avg_score = overall["Average_Review_Score"]
avg_score_str = f"{avg_score:.4f}"

score_levels = spark.range(1, 6) \
    .withColumn("Review_Score", col("id").cast("int")) \
    .drop("id")

distribution_counts = clean_reviews \
    .groupBy(col("Review_Score_Clean").alias("Review_Score")) \
    .agg(count("Review_Score_Clean").alias("Review_Count"))

distribution = score_levels \
    .join(distribution_counts, "Review_Score", "left") \
    .na.fill(0, ["Review_Count"]) \
    .orderBy(asc("Review_Score"))

lines = []
lines.append("TASK 5 - REVIEW SCORE STATISTICS")
lines.append("Cleaning rule: cast Review_Score to integer, keep values from 1 to 5 only.")
lines.append(f"Original review rows     : {total_rows}")
lines.append(f"Valid review rows        : {valid_rows}")
lines.append(f"Invalid or NULL rows     : {invalid_or_null_rows}")
lines.append(f"Average review score     : {avg_score_str}")
lines.append("")
lines.append("Distribution by score:")
lines.extend(to_lines(distribution, 10))

with open("task5_review_stats.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
spark.stop()
