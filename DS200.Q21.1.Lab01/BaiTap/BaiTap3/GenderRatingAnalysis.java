import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class GenderRatingAnalysis {

    public static class GenderMapper extends Mapper<Object, Text, Text, Text> {
        
        private Map<String, String> userGenderMap = new HashMap<>();
        private Map<String, String> movieTitleMap = new HashMap<>();
        
        private Text titleKey = new Text();
        private Text genderRatingValue = new Text();

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            URI[] cacheFiles = context.getCacheFiles();
            if (cacheFiles != null) {
                for (URI uri : cacheFiles) {
                    Path path = new Path(uri.getPath());
                    String fileName = path.getName();
                    BufferedReader br = new BufferedReader(new FileReader(new File(path.toString())));
                    String line;
                    
                    while ((line = br.readLine()) != null) {
                        String[] parts = line.split(",");
                        
                        if (fileName.contains("user") && parts.length >= 2) {
                            String userId = parts[0].trim();
                            String gender = parts[1].trim().toUpperCase();
                            userGenderMap.put(userId, gender);
                        } else if (fileName.contains("movie") && parts.length >= 2) {
                            String movieId = parts[0].trim();
                            String title = parts[1].trim();
                            movieTitleMap.put(movieId, title);
                        }
                    }
                    br.close();
                }
            }
        }

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] parts = line.split(",");
            
            if (parts.length >= 3) {
                try {
                    String userId = parts[0].trim();
                    String movieId = parts[1].trim();
                    String rating = parts[2].trim();

                    String gender = userGenderMap.get(userId);
                    String title = movieTitleMap.get(movieId);

                    if (title != null && gender != null) {
                        titleKey.set(title);
                        genderRatingValue.set(gender + ":" + rating);
                        context.write(titleKey, genderRatingValue);
                    }
                } catch (Exception e) {
                }
            }
        }
    }

    public static class GenderReducer extends Reducer<Text, Text, Text, Text> {
        private Text resultValue = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            double sumMale = 0, sumFemale = 0;
            int countMale = 0, countFemale = 0;

            for (Text val : values) {
                String[] parts = val.toString().split(":");
                if (parts.length == 2) {
                    String gender = parts[0];
                    try {
                        double rating = Double.parseDouble(parts[1]);

                        if (gender.equals("M")) {
                            sumMale += rating;
                            countMale++;
                        } else if (gender.equals("F")) {
                            sumFemale += rating;
                            countFemale++;
                        }
                    } catch (NumberFormatException e) {
                    }
                }
            }

            if (countMale > 0 || countFemale > 0) {
                double avgMale = countMale > 0 ? sumMale / countMale : 0.0;
                double avgFemale = countFemale > 0 ? sumFemale / countFemale : 0.0;
                
                String formattedOutput = String.format("Male: %.2f, Female: %.2f", avgMale, avgFemale);
                resultValue.set(formattedOutput);
                context.write(key, resultValue);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 4) {
            System.err.println("Cách chạy: GenderRatingAnalysis <input_ratings> <output_dir> <users_file> <movies_file>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "file:///"); 

        Job job = Job.getInstance(conf, "Gender Rating Analysis");
        job.setJarByClass(GenderRatingAnalysis.class);

        job.setMapperClass(GenderMapper.class);
        job.setReducerClass(GenderReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        job.addCacheFile(new Path(args[2]).toUri());
        job.addCacheFile(new Path(args[3]).toUri());

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}