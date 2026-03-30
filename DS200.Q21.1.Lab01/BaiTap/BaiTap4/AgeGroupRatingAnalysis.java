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

public class AgeGroupRatingAnalysis {

    public static class AgeGroupMapper extends Mapper<Object, Text, Text, Text> {
        
        private Map<String, String> userAgeGroupMap = new HashMap<>();
        private Map<String, String> movieTitleMap = new HashMap<>();
        
        private Text titleKey = new Text();
        private Text ageRatingValue = new Text();

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
                        
                        if (fileName.contains("user") && parts.length >= 3) {
                            String userId = parts[0].trim();
                            
                            try {
                                int age = Integer.parseInt(parts[2].trim());
                                String ageGroup = "";
                                
                                if (age <= 18) {
                                    ageGroup = "0-18";
                                } else if (age <= 35) {
                                    ageGroup = "18-35";
                                } else if (age <= 50) {
                                    ageGroup = "35-50";
                                } else {
                                    ageGroup = "50+";
                                }
                                
                                userAgeGroupMap.put(userId, ageGroup);
                            } catch (NumberFormatException e) {
                            }
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

                    String ageGroup = userAgeGroupMap.get(userId);
                    String title = movieTitleMap.get(movieId);

                    if (title != null && ageGroup != null) {
                        titleKey.set(title);
                        ageRatingValue.set(ageGroup + ":" + rating);
                        context.write(titleKey, ageRatingValue);
                    }
                } catch (Exception e) {
                }
            }
        }
    }

    public static class AgeGroupReducer extends Reducer<Text, Text, Text, Text> {
        private Text resultValue = new Text();

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            double sum18 = 0, sum35 = 0, sum50 = 0, sumOver50 = 0;
            int count18 = 0, count35 = 0, count50 = 0, countOver50 = 0;

            for (Text val : values) {
                String[] parts = val.toString().split(":");
                if (parts.length == 2) {
                    String ageGroup = parts[0];
                    try {
                        double rating = Double.parseDouble(parts[1]);

                        switch (ageGroup) {
                            case "0-18":
                                sum18 += rating;
                                count18++;
                                break;
                            case "18-35":
                                sum35 += rating;
                                count35++;
                                break;
                            case "35-50":
                                sum50 += rating;
                                count50++;
                                break;
                            case "50+":
                                sumOver50 += rating;
                                countOver50++;
                                break;
                        }
                    } catch (NumberFormatException e) {
                    }
                }
            }

            String val18 = count18 > 0 ? String.format("%.2f", sum18 / count18) : "NA";
            String val35 = count35 > 0 ? String.format("%.2f", sum35 / count35) : "NA";
            String val50 = count50 > 0 ? String.format("%.2f", sum50 / count50) : "NA";
            String valOver50 = countOver50 > 0 ? String.format("%.2f", sumOver50 / countOver50) : "NA";
            
            String formattedOutput = String.format("0-18: %s 18-35: %s 35-50: %s 50+: %s", 
                                                   val18, val35, val50, valOver50);
            resultValue.set(formattedOutput);
            
            if (count18 > 0 || count35 > 0 || count50 > 0 || countOver50 > 0) {
                context.write(key, resultValue);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 4) {
            System.err.println("Cách chạy: AgeGroupRatingAnalysis <input_ratings> <output_dir> <users_file> <movies_file>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "file:///"); 

        Job job = Job.getInstance(conf, "Age Group Rating Analysis");
        job.setJarByClass(AgeGroupRatingAnalysis.class);

        job.setMapperClass(AgeGroupMapper.class);
        job.setReducerClass(AgeGroupReducer.class);

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