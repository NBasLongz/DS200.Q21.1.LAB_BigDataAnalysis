package ds200.lab04.task3;

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

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.countDistinct;
import static org.apache.spark.sql.functions.desc;

public final class Task3App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task3_orders_by_country.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 3");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);
            Dataset<Row> result = loader.orders()
                    .join(loader.customers(), "Customer_Trx_ID")
                    .groupBy(col("Customer_Country"), col("Customer_Country_Code"))
                    .agg(countDistinct("Order_ID").alias("Total_Orders"))
                    .orderBy(desc("Total_Orders"), col("Customer_Country"));

            List<String> lines = new ArrayList<>();
            lines.add("TASK 3 - NUMBER OF ORDERS BY COUNTRY");
            lines.add("Sorted by Total_Orders descending.");
            lines.add("Total countries: " + result.count());
            lines.add("");
            lines.addAll(TableFormatter.toLines(result, 100));

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }
}
