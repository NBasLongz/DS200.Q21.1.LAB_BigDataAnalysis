import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, countDistinct, count, round, desc, to_timestamp, year, coalesce, lit

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

spark = SparkSession.builder.appName("Lab04_Task6").master("local[*]").getOrCreate()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
DATA_DIR = BASE_DIR + "/"

orders_df = load_csv(spark, DATA_DIR + "Orders.csv")
items_df = load_csv(spark, DATA_DIR + "Order_Items.csv")
products_df = load_csv(spark, DATA_DIR + "Products.csv")

orders_2024 = orders_df \
    .withColumn("Purchase_Timestamp", to_timestamp(col("Order_Purchase_Timestamp"), "yyyy-MM-dd HH:mm")) \
    .filter(col("Purchase_Timestamp").isNotNull()) \
    .withColumn("Order_Year", year(col("Purchase_Timestamp"))) \
    .filter(col("Order_Year") == 2024)

joined = orders_2024 \
    .join(items_df, "Order_ID") \
    .join(products_df, "Product_ID") \
    .withColumn("Revenue", coalesce(col("Price").cast("double"), lit(0.0)) + coalesce(col("Freight_Value").cast("double"), lit(0.0))) \
    .withColumn("Product_Category_Name", coalesce(col("Product_Category_Name"), lit("Unknown")))

result = joined \
    .groupBy("Product_Category_Name") \
    .agg(
        round(sum("Revenue"), 2).alias("Total_Revenue_2024"),
        countDistinct("Order_ID").alias("Order_Count"),
        count("Order_Item_ID").alias("Sold_Item_Count")
    ) \
    .orderBy(desc("Total_Revenue_2024"), desc("Sold_Item_Count"))

lines = []
lines.append("TASK 6 - 2024 REVENUE BY PRODUCT CATEGORY")
lines.append("Revenue = Price + Freight_Value. Only orders with purchase year = 2024 are included.")
lines.append(f"Total categories: {result.count()}")
lines.append("")
lines.extend(to_lines(result, 100))

with open("task6_revenue_2024_by_category.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
spark.stop()
