from pyspark import SparkConf, SparkContext
conf = SparkConf().setAppName("Lab03_Task2").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
DATA_DIR = "../../Data/"

movies_rdd = sc.textFile(DATA_DIR + "movies.txt").map(lambda l: l.split(","))
ratings_rdd = sc.textFile(DATA_DIR + "ratings_1.txt").union(sc.textFile(DATA_DIR + "ratings_2.txt")).map(lambda l: l.split(","))

movie_genres = movies_rdd.map(lambda x: (x[0], x[2].split("|")))
ratings_only = ratings_rdd.map(lambda x: (x[1], float(x[2])))
joined_genres = movie_genres.join(ratings_only)
flat_genres = joined_genres.flatMap(lambda x: [(genre, (x[1][1], 1)) for genre in x[1][0]])
genre_avg = flat_genres.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])).mapValues(lambda v: (v[0] / v[1], v[1])).sortByKey()

with open("task2_genre_ratings_python.txt", "w", encoding="utf-8") as f:
    f.write("Genre|AvgRating|Count\n")
    for genre, (avg_score, count) in genre_avg.collect():
        f.write(f"{genre}|{avg_score:.4f}|{count}\n")
sc.stop()
