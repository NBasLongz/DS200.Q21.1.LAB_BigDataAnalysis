package ds200.lab04.common;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class TableFormatter {
    private TableFormatter() {}

    public static List<String> toLines(Dataset<Row> df, int maxRows) {
        String[] columns = df.columns();
        List<Row> rows = df.limit(maxRows).collectAsList();

        int[] widths = Arrays.stream(columns).mapToInt(String::length).toArray();
        List<List<String>> values = new ArrayList<>();

        for (Row row : rows) {
            List<String> current = new ArrayList<>();
            for (int i = 0; i < columns.length; i++) {
                String value = row.isNullAt(i) ? "NULL" : String.valueOf(row.get(i));
                current.add(value);
                widths[i] = Math.max(widths[i], Math.min(value.length(), 60));
            }
            values.add(current);
        }

        List<String> out = new ArrayList<>();
        out.add(formatRow(Arrays.asList(columns), widths));
        out.add(separator(widths));
        for (List<String> row : values) {
            out.add(formatRow(row, widths));
        }
        return out;
    }

    private static String formatRow(List<String> values, int[] widths) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < values.size(); i++) {
            if (i > 0) sb.append(" | ");
            sb.append(padRight(truncate(values.get(i), 60), widths[i]));
        }
        return sb.toString();
    }

    private static String separator(int[] widths) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < widths.length; i++) {
            if (i > 0) sb.append("-+-");
            sb.append("-".repeat(Math.max(1, widths[i])));
        }
        return sb.toString();
    }

    private static String padRight(String value, int width) {
        return String.format("%-" + width + "s", value);
    }

    private static String truncate(String value, int maxLen) {
        if (value == null) return "NULL";
        return value.length() <= maxLen ? value : value.substring(0, maxLen - 3) + "...";
    }
}
