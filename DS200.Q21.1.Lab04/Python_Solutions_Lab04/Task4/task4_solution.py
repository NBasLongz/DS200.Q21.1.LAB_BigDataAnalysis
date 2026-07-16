import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct, asc, desc, to_timestamp, year, month

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

spark = SparkSession.builder.appName("Lab04_Task4").master("local[*]").getOrCreate()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
DATA_DIR = BASE_DIR + "/"

orders_df = load_csv(spark, DATA_DIR + "Orders.csv")

orders_with_time = orders_df \
    .withColumn("Purchase_Timestamp", to_timestamp(col("Order_Purchase_Timestamp"), "yyyy-MM-dd HH:mm")) \
    .filter(col("Purchase_Timestamp").isNotNull()) \
    .withColumn("Order_Year", year(col("Purchase_Timestamp"))) \
    .withColumn("Order_Month", month(col("Purchase_Timestamp")))

result = orders_with_time \
    .groupBy("Order_Year", "Order_Month") \
    .agg(countDistinct("Order_ID").alias("Total_Orders")) \
    .orderBy(asc("Order_Year"), desc("Order_Month"))

lines = []
lines.append("TASK 4 - NUMBER OF ORDERS BY YEAR AND MONTH")
lines.append("Display order: year ascending, month descending.")
lines.append("")
lines.extend(to_lines(result, 100))

with open("task4_orders_by_year_month.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
spark.stop()
