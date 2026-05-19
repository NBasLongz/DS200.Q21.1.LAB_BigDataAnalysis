package ds200.lab04.common;

public final class TaskArgs {
    public final String dataDir;
    public final String outputPath;

    private TaskArgs(String dataDir, String outputPath) {
        this.dataDir = dataDir;
        this.outputPath = outputPath;
    }

    public static TaskArgs parse(String[] args, String defaultOutputPath) {
        String dataDir = args.length >= 1 ? args[0] : "data";
        String outputPath = args.length >= 2 ? args[1] : defaultOutputPath;
        return new TaskArgs(dataDir, outputPath);
    }
}
