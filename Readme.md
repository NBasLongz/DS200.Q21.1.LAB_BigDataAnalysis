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

This repository is the workspace for the course **DS200.Q21.1 — Big Data Analysis**. It contains five comprehensive lab assignments that cover major big data frameworks and technologies:

1. **Lab 01**: Hadoop MapReduce - Movie ratings analysis using MapReduce programming model
2. **Lab 02**: Apache Pig - Data processing using Pig Latin scripting language
3. **Lab 03**: Apache Spark RDD - Distributed data analysis using Apache Spark with Java RDD API
4. **Lab 04**: Apache Spark DataFrame - Distributed e-commerce data analysis using Spark DataFrame API
5. **Lab 05**: YOLO + PySpark - Real-time and batch person counting system using socket communication, PySpark, and OpenCV

All labs use the **MovieLens** dataset (except Lab 04 and Lab 05) for analyzing movie ratings, genres, user demographics, and temporal patterns.

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

### 📚 Lab 04: Apache Spark DataFrame Analysis
**Location**: `DS200.Q21.1.Lab04/`

**Objective**: Analyze e-commerce CSV datasets using Apache Spark DataFrame and Java Spark DataFrame API.

**Technologies**:
- Apache Spark 3.5.x
- Apache Maven 3.8+
- Java 11+
- Spark DataFrame API

**Tasks**:
1. Load semicolon-delimited CSV datasets with inferred schema
2. Count total orders, unique customers, unique sellers
3. Analyze orders by country
4. Analyze orders by purchase year/month
5. Analyze review score statistics
6. Analyze 2024 revenue by product category
7. Analyze delivery performance (task 8 in code)
8. Analyze customer segments (task 9 in code)

**Project Structure**:
```
DS200.Q21.1.Lab04/
├── README.md
├── data/                          # Input CSV data files
├── notebook/                      # Analysis notebooks
├── output/                        # Generated report outputs
├── screenshots/                   # Result screenshots
├── scripts/                       # Execution scripts
│   ├── run_all.sh
│   ├── run_one.sh
│   └── preview_outputs.sh
└── spark/                         # Spark application project
    ├── pom.xml
    ├── src/
    │   ├── common/
    │   ├── task1/
    │   ├── task2/
    │   ├── task3/
    │   ├── task4/
    │   ├── task5/
    │   ├── task6/
    │   ├── task8/
    │   └── task9/
    └── target/                    # Maven build outputs
```

**Running Lab 04**:
```bash
cd DS200.Q21.1.Lab04
chmod +x scripts/*.sh
./scripts/run_all.sh
```

---

### 📚 Lab 05: Real-time Person Counting System (YOLO + PySpark + OpenCV)
**Location**: `.` (Root directory of this workspace)

**Objective**: Build a distributed real-time person-counting system with YOLO detection and PySpark batch processing.

**Technologies**:
- Python 3.12
- PySpark 3.5.8
- Ultralytics YOLOv12
- OpenCV (cv2)
- TCP Sockets

**Tasks**:
1. Implement real-time camera/video frames streaming sender over TCP Socket.
2. Implement forwarder receiver.
3. Implement YOLO-based detector executing object detection and bounding boxes extraction.
4. Implement storage server saving results to JSON database.
5. Implement PySpark batch processor distributing person counting task over video files.
6. Export annotated video and visual output frames with drawn bounding boxes.

**Project Structure**:
```
DS200.Q21.1.Lab05/
├── src/
│   ├── config.py              # Centralized configuration
│   ├── sender.py              # Frame sender (video/camera)
│   ├── receiver.py            # Frame receiver and forwarder
│   ├── detector.py            # YOLO detector server
│   ├── storage.py             # Storage server saving JSON
│   ├── batch_processor.py     # PySpark batch processor
│   └── demo.py                # Main runner for real-time demo
├── output/
│   ├── detections.json        # Real-time detection output
│   └── results/               # Batch processing output
│       └── pedestrians/       # Results for pedestrians video
│           ├── annotated_pedestrians.avi
│           ├── annotated_frame_100.jpg
│           └── annotated_frame_200.jpg
```

**Result Visualization**:

Dưới đây là một số khung hình kết quả nhận diện được trích xuất (được vẽ bounding box màu xanh lá và hiển thị số lượng người đếm được):

<p align="center">
  <img src="output/results/pedestrians/annotated_frame_100.jpg" width="48%" alt="Frame 100" />
  <img src="output/results/pedestrians/annotated_frame_200.jpg" width="48%" alt="Frame 200" />
</p>

**Running Lab 05**:
```bash
# Chạy realtime demo
python3 src/demo.py --video data/video/pedestrians.mp4 --frames 150

# Chạy batch processor bằng PySpark
python3 src/batch_processor.py --no-sahi
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

└── DS200.Q21.1.Lab04/                  # Spark DataFrame Lab
    ├── data/                           # E-commerce CSV datasets
    ├── notebook/                       # Analysis notebooks
    ├── output/                         # Generated report outputs
    ├── screenshots/                    # Result screenshots
    ├── scripts/                        # Execution scripts
    └── spark/                          # Spark application source and Maven project
        ├── pom.xml
        ├── src/
        └── target/
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
