package ds200.lab04.task8;

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
import static org.apache.spark.sql.functions.desc;
import static org.apache.spark.sql.functions.expr;
import static org.apache.spark.sql.functions.max;
import static org.apache.spark.sql.functions.min;
import static org.apache.spark.sql.functions.round;
import static org.apache.spark.sql.functions.to_timestamp;
import static org.apache.spark.sql.functions.when;

public final class Task8App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task8_delivery_performance.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 8");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);

            Dataset<Row> orders = loader.orders()
                    .withColumn(
                            "Actual_Delivery_Time",
                            to_timestamp(col("Order_Delivered_Carrier_Date"), "yyyy-MM-dd HH:mm")
                    )
                    .select("Order_ID", "Order_Status", "Actual_Delivery_Time");

            Dataset<Row> items = loader.orderItems()
                    .withColumn(
                            "Expected_Delivery_Time",
                            to_timestamp(col("Shipping_Limit_Date"), "yyyy-MM-dd HH:mm")
                    )
                    .select("Order_ID", "Order_Item_ID", "Product_ID", "Seller_ID", "Expected_Delivery_Time");

            Dataset<Row> delivery = items
                    .join(orders, "Order_ID")
                    .filter(col("Actual_Delivery_Time").isNotNull()
                            .and(col("Expected_Delivery_Time").isNotNull()))
                    .withColumn(
                            "Delay_Days",
                            round(expr("(unix_timestamp(Actual_Delivery_Time) - unix_timestamp(Expected_Delivery_Time)) / 86400.0"), 2)
                    )
                    .withColumn(
                            "Delivery_Performance",
                            when(col("Delay_Days").lt(0), "Early")
                                    .when(col("Delay_Days").equalTo(0), "On_Time")
                                    .otherwise("Late")
                    );

            Dataset<Row> summary = delivery
                    .groupBy("Delivery_Performance")
                    .agg(
                            count("Order_Item_ID").alias("Item_Count"),
                            round(avg("Delay_Days"), 2).alias("Avg_Delay_Days"),
                            round(min("Delay_Days"), 2).alias("Min_Delay_Days"),
                            round(max("Delay_Days"), 2).alias("Max_Delay_Days")
                    )
                    .orderBy(desc("Item_Count"));

            Dataset<Row> worstLateItems = delivery
                    .select(
                            col("Order_ID"),
                            col("Order_Item_ID"),
                            col("Seller_ID"),
                            col("Order_Status"),
                            col("Expected_Delivery_Time"),
                            col("Actual_Delivery_Time"),
                            col("Delay_Days"),
                            col("Delivery_Performance")
                    )
                    .orderBy(desc("Delay_Days"));

            List<String> lines = new ArrayList<>();
            lines.add("TASK 8 - DELIVERY PERFORMANCE ANALYSIS");
            lines.add("Delay_Days = Order_Delivered_Carrier_Date - Shipping_Limit_Date.");
            lines.add("Negative value means the item was shipped before the expected shipping limit.");
            lines.add("Rows with NULL actual/expected delivery timestamps are excluded.");
            lines.add("Valid order-item rows used: " + delivery.count());
            lines.add("");
            lines.add("A. Delivery performance summary");
            lines.addAll(TableFormatter.toLines(summary, 20));
            lines.add("");
            lines.add("B. Top 50 latest order items by delay days");
            lines.addAll(TableFormatter.toLines(worstLateItems, 50));

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }
}
