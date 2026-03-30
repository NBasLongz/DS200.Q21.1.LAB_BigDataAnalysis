<p align="center">
  <a href="https://www.uit.edu.vn/" title="University of Information Technology">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="University of Information Technology (UIT)" width="400">
  </a>
</p>

<h1 align="center"><b>DS200.Q21.1 - Big Data Analysis — LAB workspace</b></h1>

<p align="center">
  <img src="https://img.shields.io/badge/Repository-NBasLongz%2FDS200.Q21.1.LAB_BigDataAnalysis-blue?style=for-the-badge" alt="repo" />
  <img src="https://img.shields.io/badge/Jupyter%20Notebook-96%25-brightgreen?style=for-the-badge&logo=jupyter" alt="Notebooks" />
  <img src="https://img.shields.io/badge/Java-3.6%25-orange?style=for-the-badge&logo=openjdk" alt="Java" />
  <img src="https://img.shields.io/badge/Shell-0.4%25-lightgrey?style=for-the-badge&logo=gnu-bash" alt="Shell" />
</p>

---

## Thông tin sinh viên (Vui lòng cung cấp để cập nhật)


| Mã SV     | Họ và tên       | GitHub                                  | Email                      |
|:---------:|------------------|-----------------------------------------|----------------------------|
| 23520880   | Nguyen Ba Long | [NBasLongz](https://github.com/NBasLongz) | 23520880@uit.edu.vn         |

---

## Mục đích

Repo này là workspace cho môn DS200.Q21.1 — Big Data Analysis. Theo nội dung hiện có trong repo, phần lớn nội dung là Jupyter Notebook (phân tích & xử lý dữ liệu), kèm theo một số mã Java MapReduce và vài script shell hỗ trợ. Mục tiêu: lưu trữ các bài lab, notebook phân tích, mã MapReduce (nếu cần) và tài liệu hướng dẫn.

---

## Nội dung chính của repo

- notebooks/           ← Jupyter notebooks cho các bài lab (phần lớn nội dung)
- data/                ← dữ liệu mẫu (CSV, TXT, ...)
- hadoop/java/         ← (tùy chọn) mã Java MapReduce (nếu có)
- scripts/             ← script shell để chạy/builde hoặc tiền xử lý
- output/              ← kết quả chạy, báo cáo, logs
- slides/              ← tài liệu bài giảng (nếu có)
- screenshots/         ← ảnh chụp màn hình nộp bài

---

## Cấu trúc thư mục (ví dụ tham khảo)

```text
DS200.Q21.1.LAB_BigDataAnalysis/
├── README.md
├── requirements.txt           ← (tùy chọn) dependencies cho notebooks
├── data/
├── notebooks/
│   ├── lab01_analysis.ipynb
│   └── lab02_...ipynb
├── hadoop/
│   ├── java/
│   └── streaming/
├── scripts/
├── output/
└── screenshots/
