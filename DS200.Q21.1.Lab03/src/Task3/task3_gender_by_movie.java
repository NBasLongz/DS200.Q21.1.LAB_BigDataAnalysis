package Task3;

import model.RatingStats;
import util.Lab03Parse;
import util.OutputWriter;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.broadcast.Broadcast;
import scala.Tuple2;
import java.util.*;

public class task3_gender_by_movie {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("Task3").setMaster("local[*]");
        try (JavaSparkContext sc = new JavaSparkContext(conf)) {
            Map<Integer, String> movieMap = sc.textFile(args[0]).mapToPair(l -> new Tuple2<>(Integer.parseInt(l.split(",")[0]), l.split(",")[1])).collectAsMap();
            Map<Integer, String> userGenderMap = sc.textFile(args[1]).mapToPair(l -> new Tuple2<>(Integer.parseInt(l.split(",")[0]), l.split(",")[1])).collectAsMap();
            Broadcast<Map<Integer, String>> bUserGender = sc.broadcast(userGenderMap);

            List<Tuple2<String, RatingStats>> stats = new ArrayList<>(sc.textFile(args[2]).union(sc.textFile(args[3])).mapToPair(line -> {
                String[] p = line.split(",");
                String gender = bUserGender.value().get(Integer.parseInt(p[0]));
                return new Tuple2<>(p[1] + "_" + gender, new RatingStats(Double.parseDouble(p[2]), 1));
            }).reduceByKey(RatingStats::merge).collect());

            Map<Integer, RatingStats> maleStats = new HashMap<>(), femaleStats = new HashMap<>();
            for (var s : stats) {
                String[] p = s._1.split("_");
                int mid = Integer.parseInt(p[0]);
                if (p[1].equals("M")) maleStats.put(mid, s._2); else femaleStats.put(mid, s._2);
            }

            List<Integer> sortedIds = new ArrayList<>(movieMap.keySet());
            sortedIds.sort(Comparator.comparing(movieMap::get));

            List<String> output = new ArrayList<>();
            output.add("MovieID|Title|MaleAvg|MaleCount|FemaleAvg|FemaleCount");
            for (int id : sortedIds) {
                RatingStats ms = maleStats.getOrDefault(id, new RatingStats(0, 0));
                RatingStats fs = femaleStats.getOrDefault(id, new RatingStats(0, 0));
                if (ms.count > 0 || fs.count > 0)
                    output.add(id + "|" + movieMap.get(id) + "|" + (ms.count == 0 ? "0.0000" : Lab03Parse.fmt(ms.getAverage())) + "|" + ms.count + "|" + (fs.count == 0 ? "0.0000" : Lab03Parse.fmt(fs.getAverage())) + "|" + fs.count);
            }
            OutputWriter.write(args[4], output);
        }
    }
}