import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class GenreRatingAnalysis {

    public static class GenreJoinMapper extends Mapper<Object, Text, Text, DoubleWritable> {
        
        // Map movieId to genres
        private Map<String, String> movieGenresMap = new HashMap<>();
        
        private Text genreKey = new Text();
        private DoubleWritable ratingValue = new DoubleWritable();

        @Override
        protected void setup(Context context) throws IOException, InterruptedException {
            URI[] cacheFiles = context.getCacheFiles();
            if (cacheFiles != null && cacheFiles.length > 0) {
                File moviesFile = new File(cacheFiles[0].getPath());
                BufferedReader br = new BufferedReader(new FileReader(moviesFile));
                String line;
                
                while ((line = br.readLine()) != null) {
                    String[] parts = line.split(",");
                    
                    if (parts.length >= 3) {
                        String movieId = parts[0].trim();
                        String genres = parts[parts.length - 1].trim(); 
                        movieGenresMap.put(movieId, genres);
                    }
                }
                br.close();
            }
        }

        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] parts = line.split(",");
            
            if (parts.length >= 3) {
                try {
                    String movieId = parts[1].trim();
                    double rating = Double.parseDouble(parts[2].trim());

                    String genresStr = movieGenresMap.get(movieId);

                    if (genresStr != null) {
                        String[] genres = genresStr.split("\\|");

                        ratingValue.set(rating);

                        for (String genre : genres) {
                            genreKey.set(genre.trim());
                            context.write(genreKey, ratingValue);
                        }
                    }
                } catch (NumberFormatException e) {
                }
            }
        }
    }

    public static class GenreReducer extends Reducer<Text, DoubleWritable, Text, Text> {
        private Text resultValue = new Text();

        @Override
        public void reduce(Text key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException {
            double sum = 0;
            int count = 0;

            for (DoubleWritable val : values) {
                sum += val.get();
                count++;
            }

            if (count > 0) {
                double average = sum / count;
                
                String formattedOutput = String.format("Avg: %.2f, Count: %d", average, count);
                resultValue.set(formattedOutput);
                context.write(key, resultValue);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 3) {
            System.err.println("Cách chạy: GenreRatingAnalysis <thư_mục_ratings> <thư_mục_output> <file_movies.txt>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "file:///"); 

        Job job = Job.getInstance(conf, "Genre Rating Analysis (with Join)");
        job.setJarByClass(GenreRatingAnalysis.class);

        job.setMapperClass(GenreJoinMapper.class);
        job.setReducerClass(GenreReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(DoubleWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        job.addCacheFile(new Path(args[2]).toUri());

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}