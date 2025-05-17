-- Tắt ràng buộc khóa ngoại tạm thời
SET FOREIGN_KEY_CHECKS = 0;

-- Xóa dữ liệu từ các bảng liên quan
DELETE FROM time_entries;
DELETE FROM task_assignments;
DELETE FROM deadline_extension_requests;
DELETE FROM tasks;
DELETE FROM team_project_memberships;
DELETE FROM projects;

-- Bật lại ràng buộc khóa ngoại
SET FOREIGN_KEY_CHECKS = 1;

-- Tạo dữ liệu mẫu cho bảng projects
INSERT INTO projects (id, name, description, start_date, end_date, manager_id) VALUES
(1, 'Dự án Quản lý Nhân sự', 'Phát triển hệ thống quản lý nhân sự cho công ty ABC', '2024-05-01 08:00:00', '2024-08-31 17:00:00', 1),
(2, 'Dự án Cổng thông tin điện tử', 'Xây dựng cổng thông tin điện tử cho Sở Giáo dục và Đào tạo', '2024-05-15 08:00:00', '2024-09-15 17:00:00', 2);

-- Tạo dữ liệu mẫu cho bảng team_project_memberships
INSERT INTO team_project_memberships (id, project_id, user_id, join_date, role) VALUES
(1, 1, 1, '2024-05-01 08:00:00', 'Project Manager'),
(2, 1, 3, '2024-05-01 08:00:00', 'Developer'),
(3, 1, 4, '2024-05-01 08:00:00', 'Designer'),
(4, 2, 2, '2024-05-15 08:00:00', 'Project Manager'),
(5, 2, 3, '2024-05-15 08:00:00', 'Developer'),
(6, 2, 5, '2024-05-15 08:00:00', 'Tester');

-- Tạo dữ liệu mẫu cho bảng tasks
INSERT INTO tasks (id, project_id, title, description, deadline, status, difficulty, estimated_time, github_link, total_time, is_tracking, notes, start_date, completed_date) VALUES
(1, 1, 'Phân tích yêu cầu', 'Phân tích yêu cầu chi tiết cho hệ thống quản lý nhân sự', '2024-05-15 17:00:00', 'Completed', 'Medium', 20, NULL, 18.5, 0, 'Đã hoàn thành đúng tiến độ', '2024-05-01 09:00:00', '2024-05-14 17:00:00'),
(2, 1, 'Thiết kế cơ sở dữ liệu', 'Thiết kế schema cơ sở dữ liệu cho hệ thống', '2024-05-25 17:00:00', 'Completed', 'Hard', 15, 'https://github.com/abc/hrm-db', 16.2, 0, NULL, '2024-05-15 09:00:00', '2024-05-24 17:00:00'),
(3, 1, 'Phát triển module quản lý nhân viên', 'Xây dựng module quản lý thông tin nhân viên', '2024-06-15 17:00:00', 'In progress', 'Hard', 40, 'https://github.com/abc/hrm-employee', 20.5, 0, NULL, '2024-05-25 09:00:00', NULL),
(4, 1, 'Phát triển module chấm công', 'Xây dựng module chấm công và tính lương', '2024-06-30 17:00:00', 'To-do', 'Hard', 35, NULL, 0, 0, NULL, NULL, NULL),
(5, 1, 'Kiểm thử hệ thống', 'Kiểm thử toàn bộ hệ thống', '2024-07-15 17:00:00', 'To-do', 'Medium', 25, NULL, 0, 0, NULL, NULL, NULL),
(6, 2, 'Phân tích yêu cầu', 'Phân tích yêu cầu chi tiết cho cổng thông tin điện tử', '2024-05-30 17:00:00', 'Completed', 'Medium', 18, NULL, 17.8, 0, NULL, '2024-05-15 09:00:00', '2024-05-29 17:00:00'),
(7, 2, 'Thiết kế giao diện', 'Thiết kế UI/UX cho cổng thông tin', '2024-06-15 17:00:00', 'In progress', 'Medium', 20, 'https://github.com/abc/portal-ui', 12.5, 0, NULL, '2024-05-31 09:00:00', NULL),
(8, 2, 'Phát triển module tin tức', 'Xây dựng module quản lý tin tức', '2024-06-30 17:00:00', 'To-do', 'Medium', 25, NULL, 0, 0, NULL, NULL, NULL),
(9, 2, 'Phát triển module tài liệu', 'Xây dựng module quản lý tài liệu', '2024-07-15 17:00:00', 'To-do', 'Medium', 22, NULL, 0, 0, NULL, NULL, NULL),
(10, 2, 'Kiểm thử và triển khai', 'Kiểm thử và triển khai hệ thống', '2024-08-15 17:00:00', 'To-do', 'Hard', 30, NULL, 0, 0, NULL, NULL, NULL);

-- Tạo dữ liệu mẫu cho bảng task_assignments
INSERT INTO task_assignments (id, task_id, user_id, role, estimated_time, actual_time, status) VALUES
(1, 1, 1, 'Thực hiện chính', 15, 14.5, 'Completed'),
(2, 1, 3, 'Đồng thực hiện', 5, 4, 'Completed'),
(3, 2, 3, 'Thực hiện chính', 15, 16.2, 'Completed'),
(4, 3, 3, 'Thực hiện chính', 30, 15.5, 'In progress'),
(5, 3, 4, 'Review', 10, 5, 'In progress'),
(6, 4, 3, 'Thực hiện chính', 25, 0, 'To-do'),
(7, 4, 4, 'Test', 10, 0, 'To-do'),
(8, 5, 4, 'Thực hiện chính', 15, 0, 'To-do'),
(9, 5, 3, 'Review', 10, 0, 'To-do'),
(10, 6, 2, 'Thực hiện chính', 12, 12.8, 'Completed'),
(11, 6, 5, 'Review', 6, 5, 'Completed'),
(12, 7, 4, 'Thực hiện chính', 20, 12.5, 'In progress'),
(13, 8, 3, 'Thực hiện chính', 25, 0, 'To-do'),
(14, 9, 5, 'Thực hiện chính', 22, 0, 'To-do'),
(15, 10, 5, 'Thực hiện chính', 20, 0, 'To-do'),
(16, 10, 3, 'Đồng thực hiện', 10, 0, 'To-do');

-- Tạo dữ liệu mẫu cho bảng time_entries_new (bảng mới)
INSERT INTO time_entries (id, task_assignment_id, start_time, end_time, duration) VALUES
(1, 1, '2024-05-01 09:00:00', '2024-05-01 17:00:00', 8),
(2, 1, '2024-05-02 09:00:00', '2024-05-02 15:30:00', 6.5),
(3, 2, '2024-05-01 13:00:00', '2024-05-01 17:00:00', 4),
(4, 3, '2024-05-15 09:00:00', '2024-05-15 17:00:00', 8),
(5, 3, '2024-05-16 09:00:00', '2024-05-16 17:00:00', 8),
(6, 3, '2024-05-17 09:00:00', '2024-05-17 09:12:00', 0.2),
(7, 4, '2024-05-25 09:00:00', '2024-05-25 17:00:00', 8),
(8, 4, '2024-05-26 09:00:00', '2024-05-26 16:30:00', 7.5),
(9, 5, '2024-05-27 13:00:00', '2024-05-27 18:00:00', 5),
(10, 10, '2024-05-15 09:00:00', '2024-05-15 17:00:00', 8),
(11, 10, '2024-05-16 09:00:00', '2024-05-16 13:48:00', 4.8),
(12, 11, '2024-05-17 13:00:00', '2024-05-17 18:00:00', 5),
(13, 12, '2024-05-31 09:00:00', '2024-05-31 17:00:00', 8),
(14, 12, '2024-06-01 09:00:00', '2024-06-01 13:30:00', 4.5);

-- Tạo dữ liệu mẫu cho bảng deadline_extension_requests
INSERT INTO deadline_extension_requests (id, task_id, requested_by_id, requested_deadline, status, reason, created_at) VALUES
(1, 3, 3, '2024-06-30 17:00:00', 'Approved', 'Cần thêm thời gian để hoàn thiện các tính năng phức tạp', '2024-06-01 10:30:00'),
(2, 7, 4, '2024-06-30 17:00:00', 'Pending', 'Gặp khó khăn trong việc tích hợp với hệ thống bên thứ ba', '2024-06-05 14:15:00'); 