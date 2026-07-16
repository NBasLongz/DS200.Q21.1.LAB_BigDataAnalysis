import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, min, max, round, to_timestamp, when, desc, expr

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

spark = SparkSession.builder.appName("Lab04_Task8").master("local[*]").getOrCreate()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
DATA_DIR = BASE_DIR + "/"

orders_df = load_csv(spark, DATA_DIR + "Orders.csv")
items_df = load_csv(spark, DATA_DIR + "Order_Items.csv")

orders = orders_df \
    .withColumn("Actual_Delivery_Time", to_timestamp(col("Order_Delivered_Carrier_Date"), "yyyy-MM-dd HH:mm")) \
    .select("Order_ID", "Order_Status", "Actual_Delivery_Time")

items = items_df \
    .withColumn("Expected_Delivery_Time", to_timestamp(col("Shipping_Limit_Date"), "yyyy-MM-dd HH:mm")) \
    .select("Order_ID", "Order_Item_ID", "Product_ID", "Seller_ID", "Expected_Delivery_Time")

delivery = items.join(orders, "Order_ID") \
    .filter(col("Actual_Delivery_Time").isNotNull() & col("Expected_Delivery_Time").isNotNull()) \
    .withColumn("Delay_Days", round((col("Actual_Delivery_Time").cast("long") - col("Expected_Delivery_Time").cast("long")) / 86400.0, 2)) \
    .withColumn("Delivery_Performance", 
                when(col("Delay_Days") < 0, "Early")
                .when(col("Delay_Days") == 0, "On_Time")
                .otherwise("Late"))

summary = delivery \
    .groupBy("Delivery_Performance") \
    .agg(
        count("Order_Item_ID").alias("Item_Count"),
        round(avg("Delay_Days"), 2).alias("Avg_Delay_Days"),
        round(min("Delay_Days"), 2).alias("Min_Delay_Days"),
        round(max("Delay_Days"), 2).alias("Max_Delay_Days")
    ) \
    .orderBy(desc("Item_Count"))

worst_late_items = delivery \
    .select("Order_ID", "Order_Item_ID", "Seller_ID", "Order_Status", "Expected_Delivery_Time", "Actual_Delivery_Time", "Delay_Days", "Delivery_Performance") \
    .orderBy(desc("Delay_Days"))

lines = []
lines.append("TASK 8 - DELIVERY PERFORMANCE ANALYSIS")
lines.append("Delay_Days = Order_Delivered_Carrier_Date - Shipping_Limit_Date.")
lines.append("Negative value means the item was shipped before the expected shipping limit.")
lines.append("Rows with NULL actual/expected delivery timestamps are excluded.")
lines.append(f"Valid order-item rows used: {delivery.count()}")
lines.append("")
lines.append("A. Delivery performance summary")
lines.extend(to_lines(summary, 20))
lines.append("")
lines.append("B. Top 50 latest order items by delay days")
lines.extend(to_lines(worst_late_items, 50))

with open("task8_delivery_performance.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
spark.stop()
