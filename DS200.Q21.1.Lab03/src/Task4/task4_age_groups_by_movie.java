package Task4;

import model.RatingStats;
import util.Lab03Parse;
import util.OutputWriter;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.broadcast.Broadcast;
import scala.Tuple2;
import java.util.*;

public class task4_age_groups_by_movie {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("Task4").setMaster("local[*]");
        try (JavaSparkContext sc = new JavaSparkContext(conf)) {
            Map<Integer, String> movieMap = sc.textFile(args[0]).mapToPair(l -> new Tuple2<>(Integer.parseInt(l.split(",")[0]), l.split(",")[1])).collectAsMap();
            Map<Integer, String> userAgeMap = sc.textFile(args[1]).mapToPair(l -> {
                String[] p = l.split(",");
                return new Tuple2<>(Integer.parseInt(p[0]), Lab03Parse.ageGroup(Integer.parseInt(p[2])));
            }).collectAsMap();
            Broadcast<Map<Integer, String>> bUserAge = sc.broadcast(userAgeMap);

            List<Tuple2<String, RatingStats>> stats = new ArrayList<>(sc.textFile(args[2]).union(sc.textFile(args[3])).mapToPair(line -> {
                String[] p = line.split(",");
                return new Tuple2<>(p[1] + "_" + bUserAge.value().get(Integer.parseInt(p[0])), new RatingStats(Double.parseDouble(p[2]), 1));
            }).reduceByKey(RatingStats::merge).collect());

            stats.sort((a, b) -> {
                String[] pa = a._1.split("_"), pb = b._1.split("_");
                int c = movieMap.get(Integer.parseInt(pa[0])).compareTo(movieMap.get(Integer.parseInt(pb[0])));
                return c != 0 ? c : pa[1].compareTo(pb[1]);
            });

            List<String> output = new ArrayList<>();
            output.add("MovieID|Title|AgeGroup|AvgRating|Count");
            for (var s : stats) {
                String[] p = s._1.split("_");
                output.add(p[0] + "|" + movieMap.get(Integer.parseInt(p[0])) + "|" + p[1] + "|" + Lab03Parse.fmt(s._2.getAverage()) + "|" + s._2.count);
            }
            OutputWriter.write(args[4], output);
        }
    }
}