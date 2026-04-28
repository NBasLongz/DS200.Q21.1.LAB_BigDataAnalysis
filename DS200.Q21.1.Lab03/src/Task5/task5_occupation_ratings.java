package Task5;

import model.RatingStats;
import util.Lab03Parse;
import util.OutputWriter;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.broadcast.Broadcast;
import scala.Tuple2;
import java.util.*;

public class task5_occupation_ratings {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("Task5").setMaster("local[*]");
        try (JavaSparkContext sc = new JavaSparkContext(conf)) {
            Map<Integer, Integer> userOccMap = sc.textFile(args[0]).mapToPair(l -> new Tuple2<>(Integer.parseInt(l.split(",")[0]), Integer.parseInt(l.split(",")[3]))).collectAsMap();
            Map<Integer, String> occMap = sc.textFile(args[1]).mapToPair(l -> new Tuple2<>(Integer.parseInt(l.split(",")[0]), l.split(",")[1])).collectAsMap();
            Broadcast<Map<Integer, Integer>> bUserOcc = sc.broadcast(userOccMap);
            Broadcast<Map<Integer, String>> bOccNames = sc.broadcast(occMap);

            List<Tuple2<String, RatingStats>> stats = new ArrayList<>(sc.textFile(args[2]).union(sc.textFile(args[3])).mapToPair(line -> {
                String[] p = line.split(",");
                String name = bOccNames.value().get(bUserOcc.value().get(Integer.parseInt(p[0])));
                return new Tuple2<>(name, new RatingStats(Double.parseDouble(p[2]), 1));
            }).reduceByKey(RatingStats::merge).collect());

            stats.sort(Comparator.comparing(Tuple2::_1));
            List<String> output = new ArrayList<>();
            output.add("Occupation|AvgRating|Count");
            for (var s : stats) output.add(s._1 + "|" + Lab03Parse.fmt(s._2.getAverage()) + "|" + s._2.count);
            OutputWriter.write(args[4], output);
        }
    }
}