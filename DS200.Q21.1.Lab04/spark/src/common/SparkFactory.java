package ds200.lab04.common;

import org.apache.spark.sql.SparkSession;

public final class SparkFactory {
    private SparkFactory() {}

    public static SparkSession create(String appName) {
        return SparkSession.builder()
                .appName(appName)
                .master(System.getProperty("spark.master", "local[*]"))
                .config("spark.sql.session.timeZone", "UTC")
                .config("spark.sql.legacy.timeParserPolicy", "LEGACY")
                .getOrCreate();
    }
}
