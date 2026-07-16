from pyspark import SparkConf, SparkContext
conf = SparkConf().setAppName("Lab03_Task1").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
DATA_DIR = "../../Data/"

movie_map = sc.textFile(DATA_DIR + "movies.txt").map(lambda l: l.split(",")).map(lambda x: (x[0], x[1])).collectAsMap()
ratings_rdd = sc.textFile(DATA_DIR + "ratings_1.txt").union(sc.textFile(DATA_DIR + "ratings_2.txt")).map(lambda l: l.split(","))

movie_ratings = ratings_rdd.map(lambda x: (x[1], (float(x[2]), 1)))
movie_totals = movie_ratings.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
movie_avg = movie_totals.mapValues(lambda v: (v[0] / v[1], v[1])).filter(lambda x: x[1][1] >= 5)

with open("task1_movie_ratings_python.txt", "w", encoding="utf-8") as f:
    f.write("MovieID|Title|AvgRating|Count\n")
    for movie_id, (avg_score, total_reviews) in movie_avg.sortByKey().collect():
        f.write(f"{movie_id}|{movie_map.get(movie_id, 'Unknown')}|{avg_score:.4f}|{total_reviews}\n")
    
    movie_avg_50 = movie_totals.mapValues(lambda v: (v[0] / v[1], v[1])).filter(lambda x: x[1][1] >= 5)
    if not movie_avg_50.isEmpty():
        top_movie = movie_avg_50.sortBy(lambda x: x[1][0], ascending=False).first()
        f.write(f"TOP_MOVIE(minRatings=5): {movie_map.get(top_movie[0], 'Unknown')}\n")
sc.stop()
