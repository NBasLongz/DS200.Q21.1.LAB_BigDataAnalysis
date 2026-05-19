package ds200.lab04.common;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

public final class DatasetLoader {
    private final SparkSession spark;
    private final String dataDir;

    public DatasetLoader(SparkSession spark, String dataDir) {
        this.spark = spark;
        this.dataDir = trimTrailingSlash(dataDir);
    }

    public Dataset<Row> orders() {
        return readCsv("Orders.csv");
    }

    public Dataset<Row> customers() {
        return readCsv("Customer_List.csv");
    }

    public Dataset<Row> orderItems() {
        return readCsv("Order_Items.csv");
    }

    public Dataset<Row> products() {
        return readCsv("Products.csv");
    }

    public Dataset<Row> reviews() {
        return readCsv("Order_Reviews.csv");
    }

    private Dataset<Row> readCsv(String fileName) {
        String path = dataDir + "/" + fileName;
        Dataset<Row> df = spark.read()
                .option("header", "true")
                .option("sep", ";")
                .option("inferSchema", "true")
                .option("encoding", "UTF-8")
                .option("quote", "\"")
                .option("escape", "\"")
                .option("multiLine", "true")
                .option("mode", "PERMISSIVE")
                .csv(path);

        for (String col : df.columns()) {
            String clean = col.replace("\uFEFF", "").trim();
            if (!clean.equals(col)) {
                df = df.withColumnRenamed(col, clean);
            }
        }
        return df;
    }

    private static String trimTrailingSlash(String value) {
        if (value == null || value.trim().isEmpty()) {
            return "data";
        }
        return value.replaceAll("/+$", "");
    }
}
