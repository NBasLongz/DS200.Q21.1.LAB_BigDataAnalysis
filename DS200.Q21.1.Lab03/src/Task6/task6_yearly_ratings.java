package Task6;

import model.RatingStats;
import util.Lab03Parse;
import util.OutputWriter;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;
import java.util.*;

public class task6_yearly_ratings {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("Task6").setMaster("local[*]");
        try (JavaSparkContext sc = new JavaSparkContext(conf)) {
            List<Tuple2<Integer, RatingStats>> stats = new ArrayList<>(sc.textFile(args[0]).union(sc.textFile(args[1])).mapToPair(line -> {
                String[] p = line.split(",");
                return new Tuple2<>(Lab03Parse.yearFromTimestamp(Long.parseLong(p[3])), new RatingStats(Double.parseDouble(p[2]), 1));
            }).reduceByKey(RatingStats::merge).collect());

            stats.sort(Comparator.comparing(Tuple2::_1));
            
            List<String> output = new ArrayList<>();
            output.add("Year|AvgRating|Count");
            for (var s : stats) output.add(s._1 + "|" + Lab03Parse.fmt(s._2.getAverage()) + "|" + s._2.count);
            OutputWriter.write(args[2], output);
        }
    }
}