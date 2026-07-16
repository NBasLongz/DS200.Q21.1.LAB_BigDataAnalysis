from pyspark import SparkConf, SparkContext
conf = SparkConf().setAppName("Lab03_Task3").setMaster("local[*]")
sc = SparkContext.getOrCreate(conf)
DATA_DIR = "../../Data/"

movie_map = sc.textFile(DATA_DIR + "movies.txt").map(lambda l: l.split(",")).map(lambda x: (x[0], x[1])).collectAsMap()
ratings_rdd = sc.textFile(DATA_DIR + "ratings_1.txt").union(sc.textFile(DATA_DIR + "ratings_2.txt")).map(lambda l: l.split(","))
users_rdd = sc.textFile(DATA_DIR + "users.txt").map(lambda l: l.split(","))

user_gender = users_rdd.map(lambda x: (x[0], x[1]))
user_ratings = ratings_rdd.map(lambda x: (x[0], (x[1], float(x[2]))))
joined_gender = user_gender.join(user_ratings)

def get_gender_stats(records):
    male_scores = [r[1] for r in records if r[0] == 'M']
    female_scores = [r[1] for r in records if r[0] == 'F']
    m_avg = sum(male_scores) / len(male_scores) if male_scores else 0.0
    f_avg = sum(female_scores) / len(female_scores) if female_scores else 0.0
    return (m_avg, len(male_scores), f_avg, len(female_scores))

gender_grouped = joined_gender.map(lambda x: (x[1][1][0], (x[1][0], x[1][1][1]))).groupByKey().mapValues(list)
gender_stats = gender_grouped.mapValues(get_gender_stats).sortByKey()

with open("task3_gender_by_movie_python.txt", "w", encoding="utf-8") as f:
    f.write("MovieID|Title|MaleAvg|MaleCount|FemaleAvg|FemaleCount\n")
    for movie_id, (m_avg, m_count, f_avg, f_count) in gender_stats.collect():
        f.write(f"{movie_id}|{movie_map.get(movie_id, 'Unknown')}|{m_avg:.4f}|{m_count}|{f_avg:.4f}|{f_count}\n")
sc.stop()
