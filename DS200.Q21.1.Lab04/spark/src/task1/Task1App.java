package ds200.lab04.task1;

import ds200.lab04.common.DatasetLoader;
import ds200.lab04.common.ReportWriter;
import ds200.lab04.common.SparkFactory;
import ds200.lab04.common.TaskArgs;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.StructField;

import java.util.ArrayList;
import java.util.List;

public final class Task1App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task1_load_datasets.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 1");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);
            List<String> lines = new ArrayList<>();
            lines.add("TASK 1 - LOAD CSV FILES WITH INFERRED SCHEMA");
            lines.add("Delimiter: semicolon (;), header=true, inferSchema=true");
            lines.add("");

            appendDataset(lines, "Orders.csv", loader.orders());
            appendDataset(lines, "Customer_List.csv", loader.customers());
            appendDataset(lines, "Order_Items.csv", loader.orderItems());
            appendDataset(lines, "Products.csv", loader.products());
            appendDataset(lines, "Order_Reviews.csv", loader.reviews());

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }

    private static void appendDataset(List<String> lines, String name, Dataset<Row> df) {
        lines.add("============================================================");
        lines.add("Dataset: " + name);
        lines.add("Rows   : " + df.count());
        lines.add("Columns: " + df.columns().length);
        lines.add("Schema :");
        for (StructField field : df.schema().fields()) {
            lines.add("  - " + field.name() + " : " + field.dataType().simpleString());
        }
        lines.add("");
    }
}
