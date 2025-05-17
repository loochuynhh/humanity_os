# Hướng dẫn Migration và Seed Dữ liệu

Tài liệu này hướng dẫn cách thực hiện migration và seed dữ liệu cho ứng dụng `projects` trong hệ thống quản lý dự án.

## Tổng quan

Các thay đổi chính trong thiết kế database:

1. **TaskAssignments**: 
   - Thêm trường `role` với các lựa chọn: Thực hiện chính, Đồng thực hiện, Review, Test, Khác.
   - Thêm trường `actual_time` để lưu tổng thời gian thực tế từ `TimeEntries`.
   - Cập nhật ràng buộc `unique_together` thành (`task`, `user`, `role`).

2. **TimeEntries**: 
   - Chuyển liên kết từ `Task` và `User` sang `TaskAssignment`.
   - Thêm validation để kiểm tra `end_time > start_time`.
   - Thêm chỉ mục trên `task_assignment` và `start_time`.

3. **TeamProjectMembership**:
   - Thêm trường `role` để lưu vai trò của thành viên trong dự án.

4. **Các model khác**:
   - Thêm `verbose_name` và `verbose_name_plural` cho tất cả các model.
   - Thêm các chỉ mục để tối ưu truy vấn.

## Các bước thực hiện

### Bước 1: Chuẩn bị

Đảm bảo bạn đã kích hoạt môi trường ảo:

```bash
source .venv/bin/activate
```

### Bước 2: Thực hiện migration và seed dữ liệu

Có hai cách để thực hiện:

#### Cách 1: Sử dụng script Python

```bash
cd /path/to/humanity_os
python projects/migrations/migrate_and_seed.py
```

Script này sẽ:
- Thực hiện migration
- Xóa dữ liệu cũ trong các bảng của ứng dụng `projects`
- Seed dữ liệu mẫu mới
- Di chuyển dữ liệu từ bảng `time_entries` cũ sang bảng mới
- Đổi tên bảng `time_entries_new` thành `time_entries`

#### Cách 2: Thực hiện thủ công

1. **Thực hiện migration**:

```bash
python manage.py migrate projects
```

2. **Xóa dữ liệu cũ và seed dữ liệu mới**:

```bash
mysql -u username -p database_name < projects/migrations/clear_and_seed_data.sql
```

### Bước 3: Kiểm tra

Sau khi thực hiện migration và seed dữ liệu, bạn có thể kiểm tra bằng cách:

1. **Kiểm tra cấu trúc bảng**:

```sql
DESCRIBE task_assignments;
DESCRIBE time_entries;
```

2. **Kiểm tra dữ liệu**:

```sql
SELECT * FROM projects LIMIT 5;
SELECT * FROM tasks LIMIT 5;
SELECT * FROM task_assignments LIMIT 5;
SELECT * FROM time_entries LIMIT 5;
```

3. **Kiểm tra tính năng**:

Truy cập các trang sau để kiểm tra tính năng:
- http://localhost:8000/projects/projects/
- http://localhost:8000/projects/my-tasks/
- http://localhost:8000/projects/tasks/1/

## Lưu ý

- Quá trình migration sẽ **không ảnh hưởng** đến bảng `users.Users` hoặc các bảng trong các ứng dụng khác.
- Tất cả dữ liệu trong các bảng của ứng dụng `projects` sẽ bị xóa và thay thế bằng dữ liệu mẫu mới.
- Nếu bạn muốn giữ lại dữ liệu cũ, hãy sao lưu trước khi thực hiện migration.

## Xử lý lỗi

Nếu gặp lỗi trong quá trình migration hoặc seed dữ liệu:

1. **Lỗi kết nối cơ sở dữ liệu**: Kiểm tra cấu hình kết nối trong file `.env`.
2. **Lỗi ràng buộc khóa ngoại**: Đảm bảo rằng bạn đã tắt ràng buộc khóa ngoại trước khi xóa dữ liệu.
3. **Lỗi migration**: Kiểm tra file migration để đảm bảo rằng nó phù hợp với cấu trúc hiện tại của cơ sở dữ liệu. 