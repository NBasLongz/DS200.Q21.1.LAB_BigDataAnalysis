<p align="center">
  <a href="https://www.uit.edu.vn/" title="University of Information Technology">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="University of Information Technology (UIT)" width="400">
  </a>
</p>

<h1 align="center"><b>DS200.Q21.1 - Big Data Analysis — LAB Workspace</b></h1>

---

## Student Information
- **Student ID**: 23520880
- **Full Name**: Nguyen Ba Long
- **Contact Email**: 23520880@gm.uit.edu.vn
- **Course**: DS200.Q21.1 - Big Data Analysis
- **University**: University of Information Technology (UIT)

---

## Purpose

This repository is the workspace for the course **DS200.Q21.1 — Big Data Analysis**. It contains three comprehensive lab assignments that cover major big data frameworks and technologies:

1. **Lab 01**: Hadoop MapReduce - Movie ratings analysis using MapReduce programming model
2. **Lab 02**: Apache Pig - Data processing using Pig Latin scripting language
3. **Lab 03**: Apache Spark RDD - Distributed data analysis using Apache Spark with Java RDD API

All labs use the **MovieLens** dataset for analyzing movie ratings, genres, user demographics, and temporal patterns.

---

## Lab Overview

### 📚 Lab 01: Hadoop MapReduce Analysis
**Location**: `DS200.Q21.1.Lab01/`

**Objective**: Analyze movie ratings using Hadoop MapReduce framework

**Technologies**:
- Java 11+
- Apache Hadoop 3.x
- MapReduce programming model

**Tasks**:
1. Calculate average ratings per movie
2. Average ratings by movie genre
3. Ratings analysis by user gender
4. Ratings analysis by user age group

**Project Structure**:
```
DS200.Q21.1.Lab01/
├── Data/                 # Input data (movies.txt, ratings_*.txt, users.txt)
├── Notebook/             # Jupyter notebooks for analysis
├── Scripts/              # Shell scripts for running MapReduce jobs
├── BaiTap/               # Assignment instructions
├── ScreenShot_Result/    # Result screenshots
└── Readme.md             # Lab documentation
```

**Key Files**:
- `Data/movies.txt` - Movie information (ID, title, genres)
- `Data/ratings_*.txt` - User ratings (userID, movieID, rating, timestamp)
- `Data/users.txt` - User demographics (ID, gender, age, occupation)

---

### 📚 Lab 02: Apache Pig Analysis
**Location**: `DS200.Q21.1.Lab02/`

**Objective**: Process and analyze MovieLens data using Apache Pig scripting

**Technologies**:
- Apache Pig 0.17.0
- Pig Latin scripting language
- HDFS data processing

**Tasks**:
1. Data transformation and aggregation using Pig scripts
2. Group by analysis (genre, gender, age groups)
3. Average rating calculations
4. Data filtering and sorting operations

**Project Structure**:
```
DS200.Q21.1.Lab02/
├── Data/                      # Input dataset
├── Notebook/                  # Analysis notebooks
├── Source_Pig/                # Pig Latin scripts (*.pig files)
├── Output/                    # Output results
├── Result/                    # Final analysis results
├── Screenshot_result_InfUser/ # Result screenshots
└── pig-0.17.0/                # Pig framework installation
```

---

### 📚 Lab 03: Apache Spark RDD Analysis
**Location**: `DS200.Q21.1.Lab03/`

**Objective**: Perform distributed data analysis using Apache Spark RDD with Java

**Technologies**:
- Apache Spark 3.5.0 (with Scala 2.12)
- Apache Maven 3.8.7 (build tool)
- Java 11+
- Spark RDD API

**Tasks**:
1. **Task 1**: Movie average ratings with minimum rating threshold
2. **Task 2**: Average ratings by movie genre
3. **Task 3**: Gender-based rating analysis by movie
4. **Task 4**: Age group-based rating analysis
5. **Task 5**: Occupation-based rating analysis
6. **Task 6**: Yearly rating trends analysis

**Project Structure**:
```
DS200.Q21.1.Lab03/
├── Data/                      # Input MovieLens dataset
├── Notebook/                  # Jupyter notebooks
├── Output/                    # Generated results
├── src/
│   ├── Task1..Task6/          # 6 analysis tasks
│   ├── model/                 # Data model (RatingStats.java)
│   └── util/                  # Utilities (Lab03Parse, OutputWriter)
├── scripts/                   # Shell scripts
│   └── run_all.sh             # Master script to run all tasks
├── target/                    # Maven build output (JAR files)
├── pom.xml                    # Maven configuration
├── screenshots/               # Result screenshots
└── Readme.md                  # Lab documentation
```

**Key Components**:

**Java Classes**:
- `task1_movie_ratings` - Movie ratings with filtering
- `task2_genre_ratings` - Genre-based analysis
- `task3_gender_by_movie` - Gender demographics analysis
- `task4_age_groups_by_movie` - Age group analysis
- `task5_occupation_ratings` - Occupation-based analysis
- `task6_yearly_ratings` - Temporal rating trends
- `RatingStats` - Data model for aggregation
- `Lab03Parse` - Utility functions (formatting, parsing)
- `OutputWriter` - File I/O operations

**Running Lab 03**:
```bash
cd DS200.Q21.1.Lab03
mvn clean package -DskipTests    # Build the project
cd scripts
bash run_all.sh                  # Execute all tasks
# Results will be in ../output/
```

---

## Common Dataset (MovieLens)

All three labs use the same movie ratings dataset:

| File | Content | Format |
|------|---------|--------|
| `movies.txt` | Movie information | ID, Title, Genres |
| `ratings_1.txt` | Ratings subset 1 | UserID, MovieID, Rating, Timestamp |
| `ratings_2.txt` | Ratings subset 2 | UserID, MovieID, Rating, Timestamp |
| `users.txt` | User demographics | UserID, Gender, Age, Occupation, ZipCode |
| `occupation.txt` | Occupation mapping | OccupationID, OccupationName |

---

## Directory Structure (Complete)

```
DS200.Q21.1.LAB/
├── README.md                           # Main documentation (this file)
├── Readme.md                           # Alternative naming
├── Slides_Refer/                       # Reference materials and slides
│
├── DS200.Q21.1.Lab01/                  # Hadoop MapReduce Lab
│   ├── Data/                           # Input dataset
│   ├── Scripts/                        # Execution scripts
│   ├── Notebook/                       # Analysis notebooks
│   ├── BaiTap/                         # Assignment files
│   ├── ScreenShot_Result/              # Result screenshots
│   └── Readme.md
│
├── DS200.Q21.1.Lab02/                  # Apache Pig Lab
│   ├── Data/                           # Input data
│   ├── Notebook/                       # Analysis notebooks
│   ├── Source_Pig/                     # Pig scripts (*.pig)
│   ├── Output/                         # Intermediate outputs
│   ├── Result/                         # Final results
│   ├── Screenshot_result_InfUser/      # Screenshots
│   └── pig-0.17.0/                     # Pig installation
│
└── DS200.Q21.1.Lab03/                  # Apache Spark Lab
    ├── Data/                           # MovieLens dataset
    ├── Notebook/                       # Jupyter notebooks
    ├── Output/                         # Task outputs
    ├── src/                            # Java source code
    │   ├── Task1..Task6/               # Task implementations
    │   ├── model/                      # Data models
    │   └── util/                       # Utilities
    ├── scripts/                        # Shell scripts
    ├── target/                         # Maven build directory
    ├── pom.xml                         # Maven configuration
    ├── screenshots/                    # Result images
    └── Readme.md                       # Lab documentation
```

---

## Prerequisites & Environment Setup

### System Requirements
- **OS**: Linux (Ubuntu 22.04 LTS or similar)
- **Java**: OpenJDK 11 or higher
- **Memory**: 8GB+ recommended for Spark jobs
- **Disk Space**: 5GB+ for data and installations

### Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| Java | 11+ | Programming language |
| Maven | 3.8.7+ | Java project build tool |
| Apache Hadoop | 3.3.6+ | Distributed file system (Labs 1 & 2) |
| Apache Spark | 3.5.0+ | Distributed computing (Lab 3) |
| Apache Pig | 0.17.0+ | Data processing scripting (Lab 2) |
| Jupyter | Latest | Notebook environment |

---

## How to Use This Repository

### For Lab 01 (MapReduce):
```bash
cd DS200.Q21.1.Lab01
# Follow instructions in Readme.md
# Run Hadoop MapReduce jobs using provided scripts
```

### For Lab 02 (Pig):
```bash
cd DS200.Q21.1.Lab02
# Follow Pig script execution guidelines
# Check Source_Pig/ for Pig Latin scripts
```

### For Lab 03 (Spark RDD):
```bash
cd DS200.Q21.1.Lab03
mvn clean package -DskipTests
cd scripts
bash run_all.sh
# Check output/ for results
```

---

## Expected Outputs

Each lab generates analysis results showing:
- Average ratings by different dimensions (genre, gender, age, occupation, year)
- Top/bottom rated items
- Statistical summaries
- Trend analysis

Results are saved in text format with pipe-delimited values (`|`).

---

## Notes & Tips

1. **Data Format**: All input data files use pipe (`|`) or comma (`,`) delimiters
2. **Output Format**: Results are generated as pipe-delimited text files
3. **Timestamps**: Rating timestamps are in Unix epoch format (Lab 01 and 03)
4. **Memory Management**: For large datasets, adjust Spark executor memory in scripts
5. **Error Handling**: Check logs in `output/` or console for troubleshooting

---

## References & Resources

- [Apache Hadoop Documentation](https://hadoop.apache.org/docs/stable/)
- [Apache Spark RDD Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Apache Pig Documentation](https://pig.apache.org/docs/r0.17.0/)
- [MovieLens Dataset](https://grouplens.org/datasets/movielens/)
- [UIT Big Data Course](https://www.uit.edu.vn/)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2024 | 1.0 | Initial lab assignments setup |
| 2026-04 | 1.1 | Updated documentation for all 3 labs |

---

**Last Updated**: April 28, 2026  
**Status**:  All labs completed and documented  
**Maintainer**: Nguyen Ba Long (23520880)
