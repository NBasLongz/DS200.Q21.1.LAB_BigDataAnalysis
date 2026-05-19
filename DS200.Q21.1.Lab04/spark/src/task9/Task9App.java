package ds200.lab04.task9;

import ds200.lab04.common.DatasetLoader;
import ds200.lab04.common.ReportWriter;
import ds200.lab04.common.SparkFactory;
import ds200.lab04.common.TableFormatter;
import ds200.lab04.common.TaskArgs;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import java.util.ArrayList;
import java.util.List;

import static org.apache.spark.sql.functions.avg;
import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.count;
import static org.apache.spark.sql.functions.countDistinct;
import static org.apache.spark.sql.functions.desc;
import static org.apache.spark.sql.functions.expr;
import static org.apache.spark.sql.functions.first;
import static org.apache.spark.sql.functions.max;
import static org.apache.spark.sql.functions.min;
import static org.apache.spark.sql.functions.round;
import static org.apache.spark.sql.functions.sum;
import static org.apache.spark.sql.functions.to_timestamp;
import static org.apache.spark.sql.functions.when;

public final class Task9App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task9_customer_segments.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 9");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);

            Dataset<Row> orderValues = loader.orderItems()
                    .withColumn("Item_Revenue", expr("coalesce(cast(Price as double), 0.0) + coalesce(cast(Freight_Value as double), 0.0)"))
                    .groupBy("Order_ID")
                    .agg(round(sum("Item_Revenue"), 2).alias("Order_Value"));

            Dataset<Row> orders = loader.orders()
                    .withColumn("Purchase_Timestamp", to_timestamp(col("Order_Purchase_Timestamp"), "yyyy-MM-dd HH:mm"))
                    .select("Order_ID", "Customer_Trx_ID", "Order_Status", "Purchase_Timestamp");

            Dataset<Row> customers = loader.customers()
                    .select("Customer_Trx_ID", "Subscriber_ID", "Customer_City", "Customer_Country");

            Dataset<Row> customerOrders = orders
                    .join(customers, "Customer_Trx_ID")
                    .join(orderValues, "Order_ID", "left")
                    .withColumn("Order_Value", expr("coalesce(cast(Order_Value as double), 0.0)"))
                    .filter(col("Purchase_Timestamp").isNotNull());

            Dataset<Row> customerFeatures = customerOrders
                    .groupBy("Subscriber_ID")
                    .agg(
                            countDistinct("Order_ID").alias("Order_Count"),
                            round(avg("Order_Value"), 2).alias("Avg_Order_Value"),
                            round(sum("Order_Value"), 2).alias("Total_Spent"),
                            min("Purchase_Timestamp").alias("First_Purchase"),
                            max("Purchase_Timestamp").alias("Last_Purchase"),
                            first("Customer_Country").alias("Customer_Country"),
                            first("Customer_City").alias("Customer_City")
                    )
                    .withColumn("Active_Days", expr("greatest(datediff(Last_Purchase, First_Purchase), 1)"))
                    .withColumn("Purchase_Frequency_Per_30_Days", round(expr("Order_Count * 30.0 / Active_Days"), 4))
                    .withColumn(
                            "Customer_Segment",
                            when(col("Order_Count").geq(3).and(col("Avg_Order_Value").geq(200.0)), "High_Value_Loyal")
                                    .when(col("Order_Count").geq(3), "Loyal")
                                    .when(col("Avg_Order_Value").geq(200.0), "Big_Spender")
                                    .otherwise("Occasional")
                    );

            Dataset<Row> segmentSummary = customerFeatures
                    .groupBy("Customer_Segment")
                    .agg(
                            count("Subscriber_ID").alias("Customer_Count"),
                            round(avg("Order_Count"), 2).alias("Avg_Order_Count"),
                            round(avg("Avg_Order_Value"), 2).alias("Avg_Order_Value"),
                            round(avg("Purchase_Frequency_Per_30_Days"), 4).alias("Avg_Frequency_30_Days"),
                            round(sum("Total_Spent"), 2).alias("Segment_Revenue")
                    )
                    .orderBy(desc("Segment_Revenue"));

            Dataset<Row> topCustomers = customerFeatures
                    .select(
                            col("Subscriber_ID"),
                            col("Customer_Country"),
                            col("Customer_City"),
                            col("Order_Count"),
                            col("Avg_Order_Value"),
                            col("Total_Spent"),
                            col("Purchase_Frequency_Per_30_Days"),
                            col("Customer_Segment")
                    )
                    .orderBy(desc("Total_Spent"), desc("Order_Count"));

            List<String> lines = new ArrayList<>();
            lines.add("TASK 9 - CUSTOMER SEGMENTATION");
            lines.add("Features: Order_Count, Avg_Order_Value, Total_Spent, and Purchase_Frequency_Per_30_Days.");
            lines.add("Segments: High_Value_Loyal, Loyal, Big_Spender, Occasional.");
            lines.add("Total customers used: " + customerFeatures.count());
            lines.add("");
            lines.add("A. Segment summary");
            lines.addAll(TableFormatter.toLines(segmentSummary, 20));
            lines.add("");
            lines.add("B. Top 50 customers by total spending");
            lines.addAll(TableFormatter.toLines(topCustomers, 50));

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }
}
