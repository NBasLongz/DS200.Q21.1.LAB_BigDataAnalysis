# DS200.Q21.1 – Lab 05: Hệ thống đếm người thời gian thực

### Thông tin sinh viên:
* **Họ và tên:** Nguyễn Bá Long
* **Mã số sinh viên:** 23520880
* **Liên kết Github:** https://github.com/NBasLongz/DS200.Q21.1.LAB_BigDataAnalysis

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/PySpark-3.5.8-E25A1C?style=for-the-badge&logo=apachespark" />
  <img src="https://img.shields.io/badge/YOLOv12-Ultralytics-00FFFF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv" />
</p>

## Mô tả hệ thống

Hệ thống phân tán đếm số lượng người hiện diện trong camera, bao gồm:
1. **Sender (Camera)**: Đọc video/webcam và liên tục gửi các khung hình (frames) mã hóa Base64 sang Receiver qua TCP Socket (cổng `6100`).
2. **Receiver**: Nhận các khung hình từ Sender và chuyển tiếp (forward) chúng sang Detector qua TCP Socket (cổng `6200`).
3. **Detector (YOLO)**: Nhận khung hình, thực thi nhận diện đối tượng bằng YOLOv12n (được cấu hình tối ưu chạy trên môi trường ảo venv), vẽ các khung bounding box, và gửi kết quả dạng JSON sang Storage qua TCP Socket (cổng `6300`).
4. **Storage**: Lắng nghe kết quả từ Detector và lưu trữ toạ độ bounding box có cấu trúc vào file JSON `output/detections.json`.
5. **Batch Processor (PySpark)**: Sử dụng PySpark RDD (phân tán song song trên các worker) để xử lý hàng loạt video cùng lúc, xuất ra file JSON kết quả, báo cáo tổng hợp và render trực tiếp video đầu ra đã vẽ bounding box (`.avi` / `.mp4`).

## Kiến trúc truyền thông tin
```
┌─────────┐  TCP:6100  ┌──────────┐  TCP:6200  ┌──────────┐
│  Sender │──────────►│ Receiver │──────────►│ Detector │
└─────────┘           └──────────┘           └────┬─────┘
                                                  │ TCP:6300
                                                  ▼
                                             ┌─────────┐
                                             │ Storage │
                                             └─────────┘
```

## Kết quả nhận diện trực quan

Dưới đây là một số khung hình trích xuất từ video kết quả nhận diện (vẽ bounding box màu xanh lá và hiển thị số lượng người):

<p align="center">
  <img src="output/results/pedestrians/annotated_frame_100.jpg" width="48%" alt="Frame 100" />
  <img src="output/results/pedestrians/annotated_frame_200.jpg" width="48%" alt="Frame 200" />
</p>

## Hướng dẫn chạy hệ thống

### 1. Chạy demo thời gian thực (realtime)
Khởi chạy demo tự động kích hoạt tất cả các server và chạy nhận diện:
```bash
python3 src/demo.py --video data/video/pedestrians.mp4 --frames 150
```

### 2. Chạy batch processor bằng PySpark
Chạy xử lý song song video phân phối qua PySpark:
```bash
python3 src/batch_processor.py --no-sahi
```
Kết quả video đầu ra và hình ảnh được lưu trữ tại `output/results/pedestrians/`.
