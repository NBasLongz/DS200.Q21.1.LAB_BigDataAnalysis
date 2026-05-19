package ds200.lab04.task4;

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

import static org.apache.spark.sql.functions.asc;
import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.countDistinct;
import static org.apache.spark.sql.functions.desc;
import static org.apache.spark.sql.functions.month;
import static org.apache.spark.sql.functions.to_timestamp;
import static org.apache.spark.sql.functions.year;

public final class Task4App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task4_orders_by_year_month.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 4");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);
            Dataset<Row> ordersWithTime = loader.orders()
                    .withColumn("Purchase_Timestamp", to_timestamp(col("Order_Purchase_Timestamp"), "yyyy-MM-dd HH:mm"))
                    .filter(col("Purchase_Timestamp").isNotNull())
                    .withColumn("Order_Year", year(col("Purchase_Timestamp")))
                    .withColumn("Order_Month", month(col("Purchase_Timestamp")));

            Dataset<Row> result = ordersWithTime
                    .groupBy(col("Order_Year"), col("Order_Month"))
                    .agg(countDistinct("Order_ID").alias("Total_Orders"))
                    .orderBy(asc("Order_Year"), desc("Order_Month"));

            List<String> lines = new ArrayList<>();
            lines.add("TASK 4 - NUMBER OF ORDERS BY YEAR AND MONTH");
            lines.add("Display order: year ascending, month descending.");
            lines.add("");
            lines.addAll(TableFormatter.toLines(result, 100));

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }
}
