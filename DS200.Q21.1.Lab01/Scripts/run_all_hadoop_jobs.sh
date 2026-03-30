#!/bin/bash

# Script to run all 4 Hadoop MapReduce jobs sequentially
# Base directory
BASE_DIR="/home/nbl2005/DS200.Q21.1.LAB/DS200.Q21.1.Lab01"
DATA_DIR="/home/nbl2005/DS200.Q21.1_LAB/DS200.Q21.1_Lab01/data"

# Tạo thư mục classes chung
mkdir -p "$BASE_DIR/classes"

echo "Starting all Hadoop jobs..."

# Bai 1: MovieRatingAnalysis
echo "Running Bai 1: MovieRatingAnalysis"
cd "$BASE_DIR/BaiTap/BaiTap1"
rm -rf output classes
javac -cp $(hadoop classpath) -d classes MovieRatingAnalysis.java
jar cf MovieRatingAnalysis.jar -C classes .
hadoop jar MovieRatingAnalysis.jar MovieRatingAnalysis "$DATA_DIR" output "$DATA_DIR/movies.txt"
echo "Bai 1 completed. Output:"
cat output/part-r-00000
cat output/part-r-00000 > output/MovieRatingAnalysis.txt
echo "Results saved to output/MovieRatingAnalysis.txt"
echo ""

# Bai 2: GenreRatingAnalysis
echo "Running Bai 2: GenreRatingAnalysis"
cd "$BASE_DIR/BaiTap/BaiTap2"
rm -rf output classes
javac -cp $(hadoop classpath) -d classes GenreRatingAnalysis.java
jar cf GenreRatingAnalysis.jar -C classes .
hadoop jar GenreRatingAnalysis.jar GenreRatingAnalysis "$DATA_DIR" output "$DATA_DIR/movies.txt"
echo "Bai 2 completed. Output:"
cat output/part-r-00000
cat output/part-r-00000 > output/GenreRatingAnalysis.txt
echo "Results saved to output/GenreRatingAnalysis.txt"
echo ""

# Bai 3: GenderRatingAnalysis
echo "Running Bai 3: GenderRatingAnalysis"
cd "$BASE_DIR/BaiTap/BaiTap3"
rm -rf output classes
javac -cp $(hadoop classpath) -d classes GenderRatingAnalysis.java
jar cf GenderRatingAnalysis.jar -C classes .
hadoop jar GenderRatingAnalysis.jar GenderRatingAnalysis "$DATA_DIR" output "$DATA_DIR/users.txt" "$DATA_DIR/movies.txt"
echo "Bai 3 completed. Output:"
cat output/part-r-00000
cat output/part-r-00000 > output/GenderRatingAnalysis.txt
echo "Results saved to output/GenderRatingAnalysis.txt"
echo ""

# Bai 4: AgeGroupRatingAnalysis
echo "Running Bai 4: AgeGroupRatingAnalysis"
cd "$BASE_DIR/BaiTap/BaiTap4"
rm -rf output classes
javac -cp $(hadoop classpath) -d classes AgeGroupRatingAnalysis.java
jar cf AgeGroupRatingAnalysis.jar -C classes .
hadoop jar AgeGroupRatingAnalysis.jar AgeGroupRatingAnalysis "$DATA_DIR" output "$DATA_DIR/users.txt" "$DATA_DIR/movies.txt"
echo "Bai 4 completed. Output:"
cat output/part-r-00000
cat output/part-r-00000 > output/AgeGroupRatingAnalysis.txt
echo "Results saved to output/AgeGroupRatingAnalysis.txt"
echo ""

echo "All jobs completed!"