```markdown
# DS200 - LAB 03: PHÂN TÍCH DỮ LIỆU MOVIELENS VỚI APACHE SPARK RDD

## 1. Giới thiệu Dự án
Dự án áp dụng các kỹ thuật xử lý dữ liệu lớn (Big Data) **Apache Spark RDD (Resilient Distributed Datasets)** với ngôn ngữ lập trình **Java**.  

Tập dữ liệu sử dụng là **MovieLens**, bao gồm:
- Thông tin phim  
- Thông tin người dùng  
- Dữ liệu đánh giá (ratings)  

Mục tiêu: xây dựng các báo cáo thống kê quan trọng từ dữ liệu.

- **Môn học**: DS200 - Xử lý Dữ liệu lớn  
- **Đơn vị**: Khoa Khoa học Máy tính - Trường Đại học Công nghệ Thông tin (UIT)  

---

## 2. Công nghệ sử dụng

Dự án chạy trên môi trường giả lập cluster (local):

- **Hệ điều hành**: Ubuntu 22.04 LTS (WSL2)  
- **Java**: OpenJDK 11  
- **Build Tool**: Apache Maven 3.8.7  

### Big Data Frameworks
- Apache Spark 3.5.8 (without-hadoop)  
- Apache Hadoop 3.3.6 (Classpath + HDFS NameNode)  

---

## 3. Cấu trúc thư mục

```

DS200.Q21.1.Lab03/
├── Data/                   # Dữ liệu đầu vào (*.txt)

├── src/                    # Source code

│   ├── Task1..Task6/       # 6 bài toán phân tích

│   ├── model/              # Các class (RatingStats,...)

│   └── util/               # Công cụ hỗ trợ (Format, IO, Parse)

├── scripts/

│   └── run_all.sh          # Script chạy toàn bộ

├── Output/                 # Kết quả (6 file .txt)

├── target/                 # File .jar sau khi build

├── pom.xml                 # Maven config

└── README.md               # Tài liệu

````

---

## 4. Cấu hình & Cài đặt

### Biến môi trường

Thêm vào `~/.bashrc`:

```bash
export SPARK_HOME=~/spark
export PATH=$PATH:$SPARK_HOME/bin
export SPARK_DIST_CLASSPATH=$(hadoop classpath)
````

### Khởi động Hadoop

```bash
start-all.sh
```

---

## 5. Hướng dẫn thực thi

### Cấp quyền script (nếu cần)

```bash
chmod +x scripts/run_all.sh
```

### Chạy toàn bộ Lab

```bash
./scripts/run_all.sh
```

### Quy trình script

1. **Build** → Maven đóng gói `.jar`
2. **Clean** → Xóa dữ liệu cũ trong `Output/`
3. **Run** → Chạy 6 task bằng `spark-submit (local[*])`

---

## 6. Chi tiết các Task

| Task | Bài toán                    | Output File                   | Header                                         |
| ---- | --------------------------- | ----------------------------- | ---------------------------------------------- |
| 1    | Rating trung bình theo phim | task1_movie_ratings.txt       | MovieID | Title | AvgRating | Count            |
| 2    | Rating theo thể loại        | task2_genre_ratings.txt       | Genre | AvgRating | Count                      |
| 3    | So sánh theo giới tính      | task3_gender_by_movie.txt     | MovieID | Title | MaleAvg | ... | FemaleCount  |
| 4    | Phân tích theo độ tuổi      | task4_age_groups_by_movie.txt | MovieID | Title | AgeGroup | AvgRating | Count |
| 5    | Rating theo nghề nghiệp     | task5_occupation_ratings.txt  | Occupation | AvgRating | Count                 |
| 6    | Thống kê theo năm           | task6_yearly_ratings.txt      | Year | AvgRating | Count                       |

---


## 7. Thông tin Tác giả

* **Họ tên**: Nguyễn Bá Long
* **MSSV**: 23520880
* **Lớp**: DS200.Q21.1
* **Trường**: Đại học Công nghệ Thông tin - ĐHQG TP.HCM
* **GitHub**: NBasLongz

