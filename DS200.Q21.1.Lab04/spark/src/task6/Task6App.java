package ds200.lab04.task6;

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
import static org.apache.spark.sql.functions.count;
import static org.apache.spark.sql.functions.countDistinct;
import static org.apache.spark.sql.functions.desc;
import static org.apache.spark.sql.functions.expr;
import static org.apache.spark.sql.functions.round;
import static org.apache.spark.sql.functions.sum;
import static org.apache.spark.sql.functions.to_timestamp;
import static org.apache.spark.sql.functions.year;

public final class Task6App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task6_revenue_2024_by_category.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 6");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);
            Dataset<Row> orders2024 = loader.orders()
                    .withColumn("Purchase_Timestamp", to_timestamp(col("Order_Purchase_Timestamp"), "yyyy-MM-dd HH:mm"))
                    .filter(col("Purchase_Timestamp").isNotNull())
                    .withColumn("Order_Year", year(col("Purchase_Timestamp")))
                    .filter(col("Order_Year").equalTo(2024));

            Dataset<Row> joined = orders2024
                    .join(loader.orderItems(), "Order_ID")
                    .join(loader.products(), "Product_ID")
                    .withColumn("Revenue", expr("coalesce(cast(Price as double), 0.0) + coalesce(cast(Freight_Value as double), 0.0)"))
                    .withColumn("Product_Category_Name", expr("coalesce(Product_Category_Name, 'Unknown')"));

            Dataset<Row> result = joined
                    .groupBy(col("Product_Category_Name"))
                    .agg(
                            round(sum("Revenue"), 2).alias("Total_Revenue_2024"),
                            countDistinct("Order_ID").alias("Order_Count"),
                            count("Order_Item_ID").alias("Sold_Item_Count")
                    )
                    .orderBy(desc("Total_Revenue_2024"), desc("Sold_Item_Count"));

            List<String> lines = new ArrayList<>();
            lines.add("TASK 6 - 2024 REVENUE BY PRODUCT CATEGORY");
            lines.add("Revenue = Price + Freight_Value. Only orders with purchase year = 2024 are included.");
            lines.add("Total categories: " + result.count());
            lines.add("");
            lines.addAll(TableFormatter.toLines(result, 100));

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }
}
