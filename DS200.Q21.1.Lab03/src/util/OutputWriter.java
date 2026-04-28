package util;

import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class OutputWriter {
    public static void write(String path, List<String> lines) {
        try {
            Files.createDirectories(Paths.get(path).getParent());
            try (PrintWriter out = new PrintWriter(path)) {
                lines.forEach(out::println);
            }
        } catch (Exception e) { e.printStackTrace(); }
    }
}