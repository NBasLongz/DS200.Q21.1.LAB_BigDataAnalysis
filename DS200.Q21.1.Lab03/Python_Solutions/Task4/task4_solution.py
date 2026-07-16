from pyspark import SparkConf, SparkContext
conf = SparkConf().setAppName("Lab03_Task4").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
DATA_DIR = "../../Data/"

movie_map = sc.textFile(DATA_DIR + "movies.txt").map(lambda l: l.split(",")).map(lambda x: (x[0], x[1])).collectAsMap()
ratings_rdd = sc.textFile(DATA_DIR + "ratings_1.txt").union(sc.textFile(DATA_DIR + "ratings_2.txt")).map(lambda l: l.split(","))
users_rdd = sc.textFile(DATA_DIR + "users.txt").map(lambda l: l.split(","))

def get_age_group(age_str):
    try:
        age = int(age_str)
        if age >= 19 and age <= 35: return "19-35"
        elif age >= 36 and age <= 50: return "36-50"
        elif age >= 51: return "51+"
        return "Other"
    except: return "Unknown"

user_age = users_rdd.map(lambda x: (x[0], get_age_group(x[2])))
user_ratings = ratings_rdd.map(lambda x: (x[0], (x[1], float(x[2]))))
joined_age = user_age.join(user_ratings)
age_movie_rating = joined_age.map(lambda x: ((x[1][1][0], x[1][0]), (x[1][1][1], 1)))
age_movie_avg = age_movie_rating.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])).mapValues(lambda v: (v[0] / v[1], v[1])).sortByKey()

with open("task4_age_groups_by_movie_python.txt", "w", encoding="utf-8") as f:
    f.write("MovieID|Title|AgeGroup|AvgRating|Count\n")
    for (movie_id, age_group), (avg_score, count) in age_movie_avg.collect():
        f.write(f"{movie_id}|{movie_map.get(movie_id, 'Unknown')}|{age_group}|{avg_score:.4f}|{count}\n")
sc.stop()
