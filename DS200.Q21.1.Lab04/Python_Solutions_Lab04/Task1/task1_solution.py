import os
from pyspark.sql import SparkSession

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

spark = SparkSession.builder.appName("Lab04_Task1").master("local[*]").getOrCreate()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
DATA_DIR = BASE_DIR + "/"

orders_df = load_csv(spark, DATA_DIR + "Orders.csv")
customers_df = load_csv(spark, DATA_DIR + "Customer_List.csv")
items_df = load_csv(spark, DATA_DIR + "Order_Items.csv")
products_df = load_csv(spark, DATA_DIR + "Products.csv")
reviews_df = load_csv(spark, DATA_DIR + "Order_Reviews.csv")

def append_dataset(lines, name, df):
    lines.append(" ")
    lines.append(f"Dataset: {name}")
    lines.append(f"Rows   : {df.count()}")
    lines.append(f"Columns: {len(df.columns)}")
    lines.append("Schema :")
    for field in df.schema.fields:
        lines.append(f"  - {field.name} : {field.dataType.simpleString()}")
    lines.append("")

lines = []
lines.append("TASK 1 - LOAD CSV FILES WITH INFERRED SCHEMA")
lines.append("Delimiter: semicolon (;), header=true, inferSchema=true")
lines.append("")

append_dataset(lines, "Orders.csv", orders_df)
append_dataset(lines, "Customer_List.csv", customers_df)
append_dataset(lines, "Order_Items.csv", items_df)
append_dataset(lines, "Products.csv", products_df)
append_dataset(lines, "Order_Reviews.csv", reviews_df)

with open("task1_load_datasets.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
spark.stop()
