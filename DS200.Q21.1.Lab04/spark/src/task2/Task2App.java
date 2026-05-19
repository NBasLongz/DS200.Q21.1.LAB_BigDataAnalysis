package ds200.lab04.task2;

import ds200.lab04.common.DatasetLoader;
import ds200.lab04.common.ReportWriter;
import ds200.lab04.common.SparkFactory;
import ds200.lab04.common.TaskArgs;
import org.apache.spark.sql.SparkSession;

import java.util.ArrayList;
import java.util.List;

import static org.apache.spark.sql.functions.countDistinct;

public final class Task2App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task2_overall_stats.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 2");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);

            long totalOrderRows = loader.orders().count();
            long distinctOrders = loader.orders().select("Order_ID").distinct().count();

            long customerRows = loader.customers().count();
            long distinctCustomerTrxIds = loader.customers()
                    .agg(countDistinct("Customer_Trx_ID").alias("Distinct_Customer_Trx_ID"))
                    .first().getLong(0);
            long distinctSubscriberIds = loader.customers()
                    .agg(countDistinct("Subscriber_ID").alias("Distinct_Subscriber_ID"))
                    .first().getLong(0);

            long totalSellers = loader.orderItems()
                    .agg(countDistinct("Seller_ID").alias("Unique_Sellers"))
                    .first().getLong(0);

            List<String> lines = new ArrayList<>();
            lines.add("TASK 2 - OVERALL STATISTICS");
            lines.add("Total orders                  : " + distinctOrders);
            lines.add("Total customers               : " + customerRows);
            lines.add("Total unique sellers          : " + totalSellers);
            lines.add("");
            lines.add("Data-quality checks:");
            lines.add("Order table rows              : " + totalOrderRows);
            lines.add("Distinct Customer_Trx_ID      : " + distinctCustomerTrxIds);
            lines.add("Distinct Subscriber_ID        : " + distinctSubscriberIds);

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }
}
