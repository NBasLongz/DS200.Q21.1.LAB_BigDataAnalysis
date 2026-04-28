#!/bin/bash

# Dừng script ngay lập tức nếu có lỗi
set -e

echo "1. ĐANG BUILD PROJECT BẰNG MAVEN..."
mvn clean package -DskipTests

# Cài đặt biến (Lưu ý: Viết hoa Data và Output theo tree)
JAR="target/lab03-rdd-1.0.0.jar"
DATA="Data"
OUT="Output"

echo "2. CHUẨN BỊ THƯ MỤC OUTPUT..."
mkdir -p "$OUT"
rm -rf "$OUT"/*

echo "3. CHẠY TASK 1: Average rating per movie..."
spark-submit --master local[*] --class Task1.task1_movie_ratings "$JAR" \
  "$DATA/movies.txt" "$DATA/ratings_1.txt" "$DATA/ratings_2.txt" \
  "$OUT/task1_movie_ratings.txt" "5"

echo "4. CHẠY TASK 2: Average rating by genre..."
spark-submit --master local[*] --class Task2.task2_genre_ratings "$JAR" \
  "$DATA/movies.txt" "$DATA/ratings_1.txt" "$DATA/ratings_2.txt" \
  "$OUT/task2_genre_ratings.txt"

echo "5. CHẠY TASK 3: Average rating by gender per movie..."
spark-submit --master local[*] --class Task3.task3_gender_by_movie "$JAR" \
  "$DATA/movies.txt" "$DATA/users.txt" "$DATA/ratings_1.txt" "$DATA/ratings_2.txt" \
  "$OUT/task3_gender_by_movie.txt"

echo "6. CHẠY TASK 4: Average rating by age group per movie..."
spark-submit --master local[*] --class Task4.task4_age_groups_by_movie "$JAR" \
  "$DATA/movies.txt" "$DATA/users.txt" "$DATA/ratings_1.txt" "$DATA/ratings_2.txt" \
  "$OUT/task4_age_groups_by_movie.txt"

echo "7. CHẠY TASK 5: Average rating by occupation..."
spark-submit --master local[*] --class Task5.task5_occupation_ratings "$JAR" \
  "$DATA/users.txt" "$DATA/occupation.txt" "$DATA/ratings_1.txt" "$DATA/ratings_2.txt" \
  "$OUT/task5_occupation_ratings.txt"

echo "8. CHẠY TASK 6: Average rating by year..."
spark-submit --master local[*] --class Task6.task6_yearly_ratings "$JAR" \
  "$DATA/ratings_1.txt" "$DATA/ratings_2.txt" \
  "$OUT/task6_yearly_ratings.txt"

echo " HOÀN THÀNH TẤT CẢ CÁC TASK!"