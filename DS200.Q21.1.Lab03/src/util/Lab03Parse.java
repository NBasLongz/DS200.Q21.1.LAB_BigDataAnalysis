package util;

import java.io.Serializable;
import java.time.Instant;
import java.time.ZoneId;

public class Lab03Parse implements Serializable {
    public static String fmt(double d) {
        return String.format("%.4f", d);
    }

    public static String ageGroup(int age) {
        if (age <= 18) return "0-18";
        if (age <= 35) return "19-35";
        if (age <= 50) return "36-50";
        return "51+";
    }

    public static int yearFromTimestamp(long ts) {
        return Instant.ofEpochSecond(ts).atZone(ZoneId.of("UTC")).getYear();
    }
}