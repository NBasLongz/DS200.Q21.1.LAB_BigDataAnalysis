# Hadoop MapReduce Assignments - DS200.Q21.1 Lab01

This repository contains Hadoop MapReduce implementations for analyzing movie ratings data. The assignments cover four tasks: calculating average ratings per movie, average ratings by genre, ratings by gender, and ratings by age group.

## Prerequisites

- Java 11 or higher
- Apache Hadoop 3.x installed and configured
- Data files in the `data/` directory:
  - movies.txt: Movie information (ID, title, genres)
  - ratings_1.txt and `ratings_2.txt`: User ratings (user ID, movie ID, rating, timestamp)
  - users.txt: User information (ID, gender, age, occupation, zip code)

## Project Structure

```
DS200.Q21.1_Lab01/
├── data/                          # Input data files
├── hadoop/
│   ├── java/
│   │   └── lab01-mapreduce/
│   │       ├── pom.xml
│   │       └── src/main/java/ds200/lab01/
│   │           ├── MovieRatingAnalysis.java
│   │           ├── GenreRatingAnalysis.java
│   │           ├── GenderRatingAnalysis.java
│   │           └── AgeGroupRatingAnalysis.java
│   └── streaming/                 # Python streaming scripts (if needed)
├── output/                        # Output files from MapReduce jobs
├── scripts/
│   ├── run_all_hadoop_jobs.sh     # Script to compile and run all jobs
│   └── clean_all.sh               # Script to clean output and build files
└── README.md                      # This file
```

## Running the Assignments

### Option 1: Using the Automated Script

1. Navigate to the lab directory:
   ```
   cd /home/nbl2005/DS200.Q21.1_LAB/DS200.Q21.1_Lab01
   ```

2. Make the script executable:
   ```
   chmod +x scripts/run_all_hadoop_jobs.sh
   ```

3. Run all assignments:
   ```
   ./scripts/run_all_hadoop_jobs.sh
   ```

This script will:
- Compile all Java MapReduce classes
- Create JAR files
- Run each MapReduce job in sequence
- Save outputs to text files in the `output/` directory

### Option 2: Manual Execution

1. Compile the Java code:
   ```
   cd hadoop/java/lab01-mapreduce
   mvn clean compile
   mvn package
   ```

2. Run individual jobs (replace `<input_path>` with actual paths):
   ```
   # Task 1: Average ratings per movie
   hadoop jar target/lab01-mapreduce-1.0-SNAPSHOT.jar ds200.lab01.MovieRatingAnalysis <input_path> output/task1

   # Task 2: Average ratings by genre
   hadoop jar target/lab01-mapreduce-1.0-SNAPSHOT.jar ds200.lab01.GenreRatingAnalysis <input_path> output/task2

   # Task 3: Ratings by gender
   hadoop jar target/lab01-mapreduce-1.0-SNAPSHOT.jar ds200.lab01.GenderRatingAnalysis <input_path> output/task3

   # Task 4: Ratings by age group
   hadoop jar target/lab01-mapreduce-1.0-SNAPSHOT.jar ds200.lab01.AgeGroupRatingAnalysis <input_path> output/task4
   ```

## Output Files

After running the jobs, the following output files will be created in the `output/` directory:

- `task1_movie_ratings.txt`: Average rating and total ratings for each movie
- `task2_genre_ratings.txt`: Average rating and count for each genre
- `task3_gender_by_movie.txt`: Average ratings by gender for each movie
- `task4_age_groups_by_movie.txt`: Average ratings by age group for each movie



## Assignment Details

### Task 1: Movie Ratings Analysis
Calculates the average rating and total number of ratings for each movie.

### Task 2: Genre Ratings Analysis
Computes average ratings for movies grouped by genre.

### Task 3: Gender-Based Analysis
Analyzes ratings by user gender for each movie.

### Task 4: Age Group Analysis
Groups users by age ranges and calculates average ratings per movie for each age group.