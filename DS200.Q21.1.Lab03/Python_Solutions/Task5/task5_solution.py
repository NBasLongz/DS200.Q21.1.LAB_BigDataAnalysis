from pyspark import SparkConf, SparkContext
conf = SparkConf().setAppName("Lab03_Task5").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
DATA_DIR = "../../Data/"

occupation_rdd = sc.textFile(DATA_DIR + "occupation.txt").map(lambda l: l.split(","))
users_rdd = sc.textFile(DATA_DIR + "users.txt").map(lambda l: l.split(","))
ratings_rdd = sc.textFile(DATA_DIR + "ratings_1.txt").union(sc.textFile(DATA_DIR + "ratings_2.txt")).map(lambda l: l.split(","))

occ_map = occupation_rdd.map(lambda x: (x[0], x[1])).collectAsMap()
user_occ = users_rdd.map(lambda x: (x[0], x[3]))
joined_occ = user_occ.join(ratings_rdd.map(lambda x: (x[0], float(x[2]))))
occ_ratings = joined_occ.map(lambda x: (occ_map.get(x[1][0], 'Unknown'), (x[1][1], 1)))
occ_totals = occ_ratings.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
occ_avg = occ_totals.mapValues(lambda v: (v[0] / v[1], v[1])).sortByKey()

with open("task5_occupation_ratings_python.txt", "w", encoding="utf-8") as f:
    f.write("Occupation|AvgRating|Count\n")
    for occ_name, (avg_score, total_reviews) in occ_avg.collect():
        f.write(f"{occ_name}|{avg_score:.4f}|{total_reviews}\n")
sc.stop()
