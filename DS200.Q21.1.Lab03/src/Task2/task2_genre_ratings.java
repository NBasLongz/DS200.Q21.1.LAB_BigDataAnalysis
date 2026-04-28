package Task2;

import model.RatingStats;
import util.Lab03Parse;
import util.OutputWriter;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.broadcast.Broadcast;
import scala.Tuple2;
import java.util.*;

public class task2_genre_ratings {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("Task2").setMaster("local[*]");
        try (JavaSparkContext sc = new JavaSparkContext(conf)) {
            Map<Integer, List<String>> genreMap = sc.textFile(args[0]).mapToPair(line -> {
                String[] p = line.split(",", 3);
                List<String> genres = p.length > 2 ? Arrays.asList(p[2].split("\\|")) : new ArrayList<>();
                return new Tuple2<>(Integer.parseInt(p[0]), genres);
            }).collectAsMap();
            Broadcast<Map<Integer, List<String>>> bGenreMap = sc.broadcast(genreMap);

            JavaRDD<String> ratings = sc.textFile(args[1]).union(sc.textFile(args[2]));

            List<Tuple2<String, RatingStats>> stats = new ArrayList<>(ratings.flatMapToPair(line -> {
                String[] p = line.split(",");
                int mid = Integer.parseInt(p[1]);
                double r = Double.parseDouble(p[2]);
                List<String> genres = bGenreMap.value().getOrDefault(mid, new ArrayList<>());
                List<Tuple2<String, RatingStats>> res = new ArrayList<>();
                for (String g : genres) res.add(new Tuple2<>(g, new RatingStats(r, 1)));
                return res.iterator();
            }).reduceByKey(RatingStats::merge).collect());

            stats.sort(Comparator.comparing(Tuple2::_1));
            List<String> output = new ArrayList<>();
            output.add("Genre|AvgRating|Count");
            for (var s : stats) output.add(s._1 + "|" + Lab03Parse.fmt(s._2.getAverage()) + "|" + s._2.count);
            OutputWriter.write(args[3], output);
        }
    }
}