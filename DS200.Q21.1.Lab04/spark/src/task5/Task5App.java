package ds200.lab04.task5;

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
import static org.apache.spark.sql.functions.avg;
import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.count;
import static org.apache.spark.sql.functions.round;

public final class Task5App {
    public static void main(String[] args) throws Exception {
        TaskArgs parsed = TaskArgs.parse(args, "output/task5_review_stats.txt");
        SparkSession spark = SparkFactory.create("DS200 Lab04 Task 5");

        try {
            DatasetLoader loader = new DatasetLoader(spark, parsed.dataDir);
            Dataset<Row> reviews = loader.reviews();
            Dataset<Row> cleanReviews = reviews
                    .withColumn("Review_Score_Clean", col("Review_Score").cast("int"))
                    .filter(col("Review_Score_Clean").isNotNull()
                            .and(col("Review_Score_Clean").between(1, 5)));

            long totalRows = reviews.count();
            long validRows = cleanReviews.count();
            long invalidOrNullRows = totalRows - validRows;

            Row overall = cleanReviews.agg(
                    round(avg("Review_Score_Clean"), 4).alias("Average_Review_Score"),
                    count("Review_Score_Clean").alias("Valid_Review_Count")
            ).first();

            Dataset<Row> scoreLevels = spark.range(1, 6)
                    .withColumn("Review_Score", col("id").cast("int"))
                    .drop("id");

            Dataset<Row> distributionCounts = cleanReviews
                    .groupBy(col("Review_Score_Clean").alias("Review_Score"))
                    .agg(count("Review_Score_Clean").alias("Review_Count"));

            Dataset<Row> distribution = scoreLevels
                    .join(distributionCounts, new String[]{"Review_Score"}, "left")
                    .na().fill(0, new String[]{"Review_Count"})
                    .orderBy(asc("Review_Score"));

            List<String> lines = new ArrayList<>();
            lines.add("TASK 5 - REVIEW SCORE STATISTICS");
            lines.add("Cleaning rule: cast Review_Score to integer, keep values from 1 to 5 only.");
            lines.add("Original review rows     : " + totalRows);
            lines.add("Valid review rows        : " + validRows);
            lines.add("Invalid or NULL rows     : " + invalidOrNullRows);
            lines.add("Average review score     : " + overall.get(0));
            lines.add("");
            lines.add("Distribution by score:");
            lines.addAll(TableFormatter.toLines(distribution, 10));

            ReportWriter.write(parsed.outputPath, lines);
            lines.forEach(System.out::println);
        } finally {
            spark.stop();
        }
    }
}
