from pyspark import SparkConf, SparkContext
import datetime
conf = SparkConf().setAppName("Lab03_Task6").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
DATA_DIR = "../../Data/"

ratings_rdd = sc.textFile(DATA_DIR + "ratings_1.txt").union(sc.textFile(DATA_DIR + "ratings_2.txt")).map(lambda l: l.split(","))

def timestamp_to_year(ts_str):
    try: return str(datetime.datetime.fromtimestamp(int(ts_str)).year)
    except: return "Unknown"

time_ratings = ratings_rdd.map(lambda x: (timestamp_to_year(x[3]), (float(x[2]), 1)))
time_totals = time_ratings.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
time_avg = time_totals.mapValues(lambda v: (v[0] / v[1], v[1])).sortByKey()

with open("task6_yearly_ratings_python.txt", "w", encoding="utf-8") as f:
    f.write("Year|AvgRating|Count\n")
    for year, (avg_score, total_reviews) in time_avg.collect():
        f.write(f"{year}|{avg_score:.4f}|{total_reviews}\n")
sc.stop()
