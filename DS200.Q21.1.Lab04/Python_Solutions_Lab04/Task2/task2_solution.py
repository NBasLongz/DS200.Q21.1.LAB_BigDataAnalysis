import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct

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

spark = SparkSession.builder.appName("Lab04_Task2").master("local[*]").getOrCreate()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
DATA_DIR = BASE_DIR + "/"

orders_df = load_csv(spark, DATA_DIR + "Orders.csv")
customers_df = load_csv(spark, DATA_DIR + "Customer_List.csv")
items_df = load_csv(spark, DATA_DIR + "Order_Items.csv")

total_order_rows = orders_df.count()
distinct_orders = orders_df.select("Order_ID").distinct().count()

customer_rows = customers_df.count()
distinct_customer_trx_ids = customers_df.agg(countDistinct("Customer_Trx_ID")).first()[0]
distinct_subscriber_ids = customers_df.agg(countDistinct("Subscriber_ID")).first()[0]

total_sellers = items_df.agg(countDistinct("Seller_ID")).first()[0]

lines = []
lines.append("TASK 2 - OVERALL STATISTICS")
lines.append(f"Total orders                  : {distinct_orders}")
lines.append(f"Total customers               : {customer_rows}")
lines.append(f"Total unique sellers          : {total_sellers}")
lines.append("")
lines.append("Data-quality checks:")
lines.append(f"Order table rows              : {total_order_rows}")
lines.append(f"Distinct Customer_Trx_ID      : {distinct_customer_trx_ids}")
lines.append(f"Distinct Subscriber_ID        : {distinct_subscriber_ids}")

with open("task2_overall_stats.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
spark.stop()
