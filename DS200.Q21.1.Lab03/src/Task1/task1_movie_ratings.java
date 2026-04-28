package Task1;

import model.RatingStats;
import util.Lab03Parse;
import util.OutputWriter;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;
import java.util.*;

public class task1_movie_ratings {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("Task1").setMaster("local[*]");
        try (JavaSparkContext sc = new JavaSparkContext(conf)) {
            Map<Integer, String> movieMap = sc.textFile(args[0])
                    .mapToPair(line -> {
                        String[] p = line.split(",", 3);
                        return new Tuple2<>(Integer.parseInt(p[0]), p[1]);
                    }).collectAsMap();

            JavaRDD<String> ratings = sc.textFile(args[1]).union(sc.textFile(args[2]));
            int minRatings = Integer.parseInt(args[4]);

            // Bọc collect() vào new ArrayList để có thể sort
            List<Tuple2<Integer, RatingStats>> stats = new ArrayList<>(ratings.mapToPair(line -> {
                String[] p = line.split(",");
                return new Tuple2<>(Integer.parseInt(p[1]), new RatingStats(Double.parseDouble(p[2]), 1));
            }).reduceByKey(RatingStats::merge).collect());

            List<String> output = new ArrayList<>();
            output.add("MovieID|Title|AvgRating|Count"); 
            
            stats.sort(Comparator.comparing(t -> movieMap.getOrDefault(t._1, "")));
            Tuple2<Integer, RatingStats> topMovie = null;

            stats.sort(Comparator.comparing(t -> movieMap.getOrDefault(t._1, "")));
            for (var s : stats) {
                output.add(s._1 + "|" + movieMap.get(s._1) + "|" + Lab03Parse.fmt(s._2.getAverage()) + "|" + s._2.count);
                if (s._2.count >= minRatings) {
                    if (topMovie == null || s._2.getAverage() > topMovie._2.getAverage()) topMovie = s;
                    else if (s._2.getAverage() == topMovie._2.getAverage() && s._2.count > topMovie._2.count) topMovie = s;
                }
            }
            if (topMovie != null) output.add("TOP_MOVIE(minRatings=" + minRatings + "): " + movieMap.get(topMovie._1));
            OutputWriter.write(args[3], output);
        }
    }
}