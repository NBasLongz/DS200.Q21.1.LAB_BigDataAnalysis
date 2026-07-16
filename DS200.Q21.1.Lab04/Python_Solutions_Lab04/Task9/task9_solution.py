import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, countDistinct, avg, sum, min, max, round, to_timestamp, when, desc, expr, first, coalesce, lit

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

spark = SparkSession.builder.appName("Lab04_Task9").master("local[*]").getOrCreate()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
DATA_DIR = BASE_DIR + "/"

orders_df = load_csv(spark, DATA_DIR + "Orders.csv")
items_df = load_csv(spark, DATA_DIR + "Order_Items.csv")
customers_df = load_csv(spark, DATA_DIR + "Customer_List.csv")

order_values = items_df \
    .withColumn("Item_Revenue", coalesce(col("Price").cast("double"), lit(0.0)) + coalesce(col("Freight_Value").cast("double"), lit(0.0))) \
    .groupBy("Order_ID") \
    .agg(round(sum("Item_Revenue"), 2).alias("Order_Value"))

orders = orders_df \
    .withColumn("Purchase_Timestamp", to_timestamp(col("Order_Purchase_Timestamp"), "yyyy-MM-dd HH:mm")) \
    .select("Order_ID", "Customer_Trx_ID", "Order_Status", "Purchase_Timestamp")

customers = customers_df \
    .select("Customer_Trx_ID", "Subscriber_ID", "Customer_City", "Customer_Country")

customer_orders = orders.join(customers, "Customer_Trx_ID") \
    .join(order_values, "Order_ID", "left") \
    .withColumn("Order_Value", coalesce(col("Order_Value").cast("double"), lit(0.0))) \
    .filter(col("Purchase_Timestamp").isNotNull())

customer_features = customer_orders \
    .groupBy("Subscriber_ID") \
    .agg(
        countDistinct("Order_ID").alias("Order_Count"),
        round(avg("Order_Value"), 2).alias("Avg_Order_Value"),
        round(sum("Order_Value"), 2).alias("Total_Spent"),
        min("Purchase_Timestamp").alias("First_Purchase"),
        max("Purchase_Timestamp").alias("Last_Purchase"),
        first("Customer_Country").alias("Customer_Country"),
        first("Customer_City").alias("Customer_City")
    ) \
    .withColumn("Active_Days", expr("greatest(datediff(Last_Purchase, First_Purchase), 1)")) \
    .withColumn("Purchase_Frequency_Per_30_Days", round(col("Order_Count") * 30.0 / col("Active_Days"), 4)) \
    .withColumn("Customer_Segment", 
                when((col("Order_Count") >= 3) & (col("Avg_Order_Value") >= 200.0), "High_Value_Loyal")
                .when(col("Order_Count") >= 3, "Loyal")
                .when(col("Avg_Order_Value") >= 200.0, "Big_Spender")
                .otherwise("Occasional"))

segment_summary = customer_features \
    .groupBy("Customer_Segment") \
    .agg(
        count("Subscriber_ID").alias("Customer_Count"),
        round(avg("Order_Count"), 2).alias("Avg_Order_Count"),
        round(avg("Avg_Order_Value"), 2).alias("Avg_Order_Value"),
        round(avg("Purchase_Frequency_Per_30_Days"), 4).alias("Avg_Frequency_30_Days"),
        round(sum("Total_Spent"), 2).alias("Segment_Revenue")
    ) \
    .orderBy(desc("Segment_Revenue"))

top_customers = customer_features \
    .select("Subscriber_ID", "Customer_Country", "Customer_City", "Order_Count", "Avg_Order_Value", "Total_Spent", "Purchase_Frequency_Per_30_Days", "Customer_Segment") \
    .orderBy(desc("Total_Spent"), desc("Order_Count"))

lines = []
lines.append("TASK 9 - CUSTOMER SEGMENTATION")
lines.append("Features: Order_Count, Avg_Order_Value, Total_Spent, and Purchase_Frequency_Per_30_Days.")
lines.append("Segments: High_Value_Loyal, Loyal, Big_Spender, Occasional.")
lines.append(f"Total customers used: {customer_features.count()}")
lines.append("")
lines.append("A. Segment summary")
lines.extend(to_lines(segment_summary, 20))
lines.append("")
lines.append("B. Top 50 customers by total spending")
lines.extend(to_lines(top_customers, 50))

with open("task9_customer_segments.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
spark.stop()
