<p align="center">
  <a href="https://www.uit.edu.vn/" title="University of Information Technology">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="University of Information Technology (UIT)" width="400">
  </a>
</p>

<h1 align="center"><b>DS200.Q21.1 - Big Data Analysis — LAB workspace</b></h1>


---

## Thông tin sinh viên  
- Mã sinh viên: 23520880
- Họ và tên : Nguyen Ba Long
- Email liên hệ: 23520880@gm.uit.edu.vn



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
