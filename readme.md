# Humanity OS

## Giới thiệu
Humanity OS là một hệ thống quản lý doanh nghiệp, cung cấp các tính năng như quản lý công ty, KPI, đánh giá nhân sự và quản lý dự án.

## Cấu trúc thư mục
```
├── companies/        # Quản lý công ty
├── custom_admin/     # Giao diện admin tùy chỉnh
├── evaluations/      # Hệ thống đánh giá nhân viên
├── humanity_os/      # Cấu hình chính của Django
├── kpis/             # Quản lý KPI
├── projects/         # Quản lý dự án
├── users/            # Quản lý người dùng
├── static/           # Tệp tĩnh
├── templates/        # Giao diện HTML
├── .gitignore        # Danh sách file bị bỏ qua khi commit
├── manage.py         # File quản lý Django
├── requirements.txt  # Danh sách các package Python
├── .venv/            # Môi trường ảo (virtual environment)
└── .vscode/          # Cấu hình VS Code
```

## Cài đặt
### 1. Tạo và kích hoạt môi trường ảo
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 2. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3. Chạy dự án
```bash
python manage.py migrate
python manage.py runserver
```

## Thông tin liên hệ
- **Tác giả:** loochuynhh
- **Email:** lochuynhhsb@gmail.com
- **License:** MIT

