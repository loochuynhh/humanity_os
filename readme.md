# Humanity OS

Humanity OS là một hệ thống quản lý doanh nghiệp tích hợp, được xây dựng trên Django, hỗ trợ quản lý dự án, theo dõi công việc, đánh giá hiệu suất (KPI), và điểm danh nhân sự. Ứng dụng cung cấp giao diện thân thiện cho cả người dùng và quản trị viên, với các tính năng như lịch dự án, báo cáo PDF, và trò chuyện AI.

## Tính năng chính

- **Quản lý dự án**: Tạo, theo dõi dự án và công việc với tiến độ, trạng thái, và thời gian thực tế.
- **Theo dõi thời gian**: Ghi nhận thời gian làm việc cho từng công việc, hỗ trợ gia hạn deadline.
- **Đánh giá hiệu suất**: Quản lý KPI định lượng và định tính, tạo form đánh giá đồng nghiệp/phản hồi.
- **Điểm danh nhân sự**: Check-in/check-out với vị trí và ảnh, lưu lịch sử điểm danh.
- **Bảng điều khiển**: Hiển thị thống kê dự án, task, KPI, và hoạt động người dùng.
- **Báo cáo**: Xuất báo cáo PDF về hiệu suất dự án, KPI, và hoạt động cá nhân.
- **AI hỗ trợ**: Đề xuất người dùng phù hợp cho công việc và trò chuyện AI để hỗ trợ nhân sự.
- **Giao diện admin tùy chỉnh**: Quản lý người dùng, dự án, và KPI với thống kê chi tiết.

## Cấu trúc dự án

```
humanity_os/
├── manage.py              # Quản lý Django
├── docker-compose.yml     # Cấu hình Docker
├── Dockerfile             # Cấu hình container
├── requirements.txt       # Danh sách thư viện Python
├── humanity_os/           # Cấu hình Django chính
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── users/                 # Quản lý người dùng, điểm danh, hồ sơ
├── projects/              # Quản lý dự án, công việc, lịch
├── evaluations/           # Đánh giá, phản hồi, form
├── kpis/                  # Quản lý KPI, báo cáo hiệu suất
├── custom_admin/          # Giao diện admin tùy chỉnh
├── templates/             # Template HTML
└── static/                # File tĩnh (CSS, JS, hình ảnh)
```

## Yêu cầu hệ thống

- Python 3.9+
- PostgreSQL (hoặc cơ sở dữ liệu tương thích với Django)
- Docker (khuyến nghị để triển khai)
- Các thư viện Python liệt kê trong `requirements.txt`

## Cài đặt

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd humanity_os
   ```

2. **Tạo và cấu hình file môi trường**:
   - Tạo file `.env` và cập nhật các biến môi trường (ví dụ: `DATABASE_URL`, `SECRET_KEY`).

3. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Chạy migration**:
   ```bash
   python manage.py migrate
   ```

5. **Khởi động server phát triển**:
   ```bash
   python manage.py runserver
   ```

6. **(Tùy chọn) Triển khai với Docker**:
   ```bash
   docker-compose up --build
   ```

## Sử dụng

- **Truy cập ứng dụng**: Mở trình duyệt tại `http://localhost:8000`.
- **Admin dashboard**: Đăng nhập với tài khoản admin tại `/admin/` hoặc `/admin/dashboard/`.
- **Tài liệu API**: Các endpoint như `/api/suggest-user-for-task/` hỗ trợ tích hợp bên ngoài.

## Đóng góp

1. Fork repository và tạo branch mới:
   ```bash
   git checkout -b feature/<tên-tính-năng>
   ```
2. Commit thay đổi và push lên fork của bạn.
3. Tạo Pull Request mô tả chi tiết thay đổi.

## Giấy phép

[MIT License](LICENSE)

## Liên hệ

Vui lòng liên hệ qua email: lochuynhhsb@gmail.com hoặc mở issue trên repository để báo lỗi hoặc đề xuất cải tiến.