-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: humanity_os
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

USE humanity_os;-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: humanity_os
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dữ liệu cho bảng `auth_group`
INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admin'),
(2, 'Manager'),
(3, 'Employee'),
(4, 'Intern');

-- Dữ liệu cho bảng `users`
INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `avatar`, `phone`) VALUES
(1, 'pbkdf2_sha256', '2025-03-23 10:00:00.000000', 1, 'admin', 'Quản Trị', 'Hệ Thống', 'admin@humanityos.com', 1, 1, '2025-01-01 00:00:00.000000', 'avatars/admin.jpg', '0901234567'),
(2, 'pbkdf2_sha256', NULL, 0, 'manager1', 'Nguyễn', 'Văn A', 'vana@humanityos.com', 1, 1, '2025-01-02 00:00:00.000000', 'avatars/manager1.jpg', '0912345678'),
(3, 'pbkdf2_sha256', NULL, 0, 'manager2', 'Trần', 'Thị D', 'thid@humanityos.com', 1, 1, '2025-01-03 00:00:00.000000', 'avatars/manager2.jpg', '0923456789'),
(4, 'pbkdf2_sha256', NULL, 0, 'employee1', 'Lê', 'Văn B', 'vanb@humanityos.com', 0, 1, '2025-01-04 00:00:00.000000', 'avatars/employee1.jpg', '0934567890'),
(5, 'pbkdf2_sha256', NULL, 0, 'employee2', 'Phạm', 'Thị C', 'thic@humanityos.com', 0, 1, '2025-01-05 00:00:00.000000', 'avatars/employee2.jpg', '0945678901'),
(6, 'pbkdf2_sha256', NULL, 0, 'employee3', 'Hoàng', 'Văn E', 'vane@humanityos.com', 0, 1, '2025-01-06 00:00:00.000000', 'avatars/employee3.jpg', '0956789012'),
(7, 'pbkdf2_sha256', NULL, 0, 'intern1', 'Ngô', 'Thị F', 'thif@humanityos.com', 0, 1, '2025-01-07 00:00:00.000000', 'avatars/intern1.jpg', '0967890123');

-- Lưu ý: Mật khẩu thực tế
-- admin: Admin@123
-- manager1: Manager@123
-- manager2: Manager@123
-- employee1: Employee@123
-- employee2: Employee@456
-- employee3: Employee@456
-- intern1: Intern@123

-- Dữ liệu cho bảng `users_groups`
INSERT INTO `users_groups` (`id`, `users_id`, `group_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 2),
(4, 4, 3),
(5, 5, 3),
(6, 6, 3),
(7, 7, 4);

-- Dữ liệu cho bảng `teams`
INSERT INTO `teams` (`id`, `name`, `description`, `manager_id`) VALUES
(1, 'Đội phát triển phần mềm', 'Đội ngũ phát triển các sản phẩm phần mềm', 2),
(2, 'Đội hỗ trợ khách hàng', 'Đội ngũ hỗ trợ kỹ thuật và chăm sóc khách hàng', 3),
(3, 'Đội QA', 'Đội ngũ kiểm thử chất lượng phần mềm', 2);

-- Dữ liệu cho bảng `team_members`
INSERT INTO `team_members` (`id`, `user_id`, `team_id`) VALUES
(1, 4, 1),
(2, 5, 1),
(3, 6, 1),
(4, 4, 2),
(5, 5, 2),
(6, 7, 3);

-- Dữ liệu cho bảng `projects`
INSERT INTO `projects` (`id`, `name`, `description`, `start_date`, `end_date`, `manager_id`) VALUES
(1, 'Hệ thống HRM', 'Xây dựng hệ thống quản lý nhân sự', '2025-01-01', '2025-06-30', 2),
(2, 'Ứng dụng hỗ trợ', 'Phát triển ứng dụng hỗ trợ khách hàng', '2025-02-01', '2025-08-31', 3),
(3, 'Website bán hàng', 'Thiết kế website thương mại điện tử', '2025-03-01', '2025-09-30', 2),
(4, 'Ứng dụng nội bộ', 'Phát triển ứng dụng quản lý nội bộ', '2025-04-01', '2025-10-31', 3);

-- Dữ liệu cho bảng `tasks`
INSERT INTO `tasks` (`id`, `title`, `description`, `deadline`, `status`, `difficulty`, `estimated_time`, `github_link`, `project_id`) VALUES
(1, 'Thiết kế DB HRM', 'Thiết kế cơ sở dữ liệu cho HRM', '2025-02-15', 'Completed', 'Medium', 20.5, 'https://github.com/org/hrm-db', 1),
(2, 'API nhân viên', 'Xây dựng API quản lý nhân viên', '2025-03-15', 'In Progress', 'Hard', 30.0, 'https://github.com/org/hrm-api', 1),
(3, 'Giao diện HRM', 'Thiết kế UI cho HRM', '2025-04-10', 'Pending', 'Easy', 15.0, NULL, 1),
(4, 'API hỗ trợ', 'Xây dựng API cho ứng dụng hỗ trợ', '2025-05-01', 'In Progress', 'Medium', 25.0, 'https://github.com/org/support-api', 2),
(5, 'Kiểm thử hỗ trợ', 'Kiểm thử ứng dụng hỗ trợ', '2025-06-01', 'Pending', 'Easy', 10.0, NULL, 2),
(6, 'Thiết kế website', 'Thiết kế giao diện website bán hàng', '2025-07-01', 'Pending', 'Medium', 20.0, 'https://github.com/org/ecommerce-ui', 3),
(7, 'API nội bộ', 'Xây dựng API quản lý nội bộ', '2025-08-01', 'Pending', 'Hard', 35.0, 'https://github.com/org/internal-api', 4);

-- Dữ liệu cho bảng `task_assignments`
INSERT INTO `task_assignments` (`id`, `user_id`, `task_id`) VALUES
(1, 4, 1),
(2, 5, 2),
(3, 6, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 7);

-- Dữ liệu cho bảng `time_entries`
INSERT INTO `time_entries` (`id`, `start_time`, `end_time`, `task_id`, `user_id`) VALUES
(1, '2025-02-01 09:00:00.000000', '2025-02-01 17:00:00.000000', 1, 4),
(2, '2025-03-01 08:00:00.000000', '2025-03-01 12:00:00.000000', 2, 5),
(3, '2025-03-02 13:00:00.000000', '2025-03-02 17:00:00.000000', 2, 5),
(4, '2025-04-01 09:00:00.000000', NULL, 4, 4),
(5, '2025-04-02 08:00:00.000000', '2025-04-02 16:00:00.000000', 3, 6);

-- Dữ liệu cho bảng `kpis`
INSERT INTO `kpis` (`id`, `name`, `description`) VALUES
(1, 'Doanh thu dự án', 'Doanh thu hàng tháng từ dự án', 'Đo lường hiệu quả kinh doanh'),
(2, 'Hoàn thành nhiệm vụ', 'Tỷ lệ nhiệm vụ hoàn thành đúng hạn', 'Đo lường hiệu suất cá nhân'),
(3, 'Thời gian phản hồi', 'Thời gian trung bình phản hồi khách hàng', 'Đo lường chất lượng hỗ trợ'),
(4, 'Lỗi phát sinh', 'Số lỗi phát sinh trong dự án', 'Đo lường chất lượng sản phẩm');

-- Dữ liệu cho bảng `employee_kpis`
INSERT INTO `employee_kpis` (`id`, `target_value`, `actual_value`, `period`, `kpi_id`, `user_id`) VALUES
(1, '1000000', '1200000', '2025-Q1', 1, 2),
(2, '90', '85', '2025-Q1', 2, 4),
(3, '90', '95', '2025-Q1', 2, 5),
(4, '10', '8', '2025-Q1', 3, 4),
(5, '5', '3', '2025-Q1', 4, 6),
(6, '1000000', '950000', '2025-Q2', 1, 3);

-- Dữ liệu cho bảng `personal_goals`
INSERT INTO `personal_goals` (`id`, `goal_description`, `target_date`, `status`, `user_id`) VALUES
(1, 'Hoàn thành khóa học Python', '2025-05-01', 'In Progress', 4),
(2, 'Đạt chứng chỉ AWS', '2025-07-01', 'Pending', 5),
(3, 'Học ReactJS', '2025-06-01', 'Pending', 6),
(4, 'Cải thiện kỹ năng giao tiếp', '2025-08-01', 'In Progress', 7);

-- Dữ liệu cho bảng `forms`
INSERT INTO `forms` (`id`, `name`, `type`, `period`) VALUES
(1, 'Đánh giá nhân viên Q1', 'Survey', '2025-Q1'),
(2, 'Phản hồi dự án HRM', 'Feedback', '2025-Q2'),
(3, 'Đánh giá nhân viên Q2', 'Survey', '2025-Q2'),
(4, 'Phản hồi ứng dụng hỗ trợ', 'Feedback', '2025-Q3');

-- Dữ liệu cho bảng `form_questions`
INSERT INTO `form_questions` (`id`, `question_text`, `form_id`) VALUES
(1, 'Bạn đánh giá hiệu suất của nhân viên này như thế nào?', 1),
(2, 'Nhân viên có hoàn thành nhiệm vụ đúng hạn không?', 1),
(3, 'Dự án có đáp ứng được kỳ vọng không?', 2),
(4, 'Bạn đánh giá chất lượng dự án thế nào?', 2),
(5, 'Nhân viên có cải thiện kỹ năng không?', 3),
(6, 'Ứng dụng hỗ trợ có dễ sử dụng không?', 4);

-- Dữ liệu cho bảng `form_responses`
INSERT INTO `form_responses` (`id`, `answer`, `target_user_id`, `user_id`, `form_id`) VALUES
(1, 'Rất tốt', 4, 2, 1),
(2, 'Có', 4, 2, 1),
(3, 'Có, nhưng cần cải thiện tốc độ', 2, 4, 2),
(4, 'Khá tốt', 2, 5, 2),
(5, 'Có', 5, 3, 3),
(6, 'Rất dễ', 3, 4, 4);

-- Dữ liệu cho bảng `django_session`
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('abc123xyz', 'e30:{-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: humanity_os
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

USE humanity_os;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dữ liệu cho bảng `auth_group`
INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admin'),
(2, 'Manager'),
(3, 'Employee'),
(4, 'Intern');

-- Dữ liệu cho bảng `users`
INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `avatar`, `phone`) VALUES
(3, 'pbkdf2_sha256', '2025-03-23 10:00:00.000000', 1, 'admin', 'Quản Trị', 'Hệ Thống', 'admin@humanityos.com', 1, 1, '2025-01-01 00:00:00.000000', 'avatars/admin.jpg', '0901234567'),
(4, 'pbkdf2_sha256', NULL, 0, 'manager1', 'Nguyễn', 'Văn A', 'vana@humanityos.com', 1, 1, '2025-01-02 00:00:00.000000', 'avatars/manager1.jpg', '0912345678'),
(5, 'pbkdf2_sha256', NULL, 0, 'manager2', 'Trần', 'Thị D', 'thid@humanityos.com', 1, 1, '2025-01-03 00:00:00.000000', 'avatars/manager2.jpg', '0923456789'),
(6, 'pbkdf2_sha256', NULL, 0, 'employee1', 'Lê', 'Văn B', 'vanb@humanityos.com', 0, 1, '2025-01-04 00:00:00.000000', 'avatars/employee1.jpg', '0934567890'),
(7, 'pbkdf2_sha256', NULL, 0, 'employee2', 'Phạm', 'Thị C', 'thic@humanityos.com', 0, 1, '2025-01-05 00:00:00.000000', 'avatars/employee2.jpg', '0945678901'),
(8, 'pbkdf2_sha256', NULL, 0, 'employee3', 'Hoàng', 'Văn E', 'vane@humanityos.com', 0, 1, '2025-01-06 00:00:00.000000', 'avatars/employee3.jpg', '0956789012'),
(9, 'pbkdf2_sha256', NULL, 0, 'intern1', 'Ngô', 'Thị F', 'thif@humanityos.com', 0, 1, '2025-01-07 00:00:00.000000', 'avatars/intern1.jpg', '0967890123');

-- Lưu ý: Mật khẩu thực tế
-- admin: Admin@123
-- manager1: Manager@123
-- manager2: Manager@123
-- employee1: Employee@123
-- employee2: Employee@456
-- employee3: Employee@456
-- intern1: Intern@123

-- Dữ liệu cho bảng `users_groups`
INSERT INTO `users_groups` (`id`, `users_id`, `group_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 2),
(4, 4, 3),
(5, 5, 3),
(6, 6, 3),
(7, 7, 4);

-- Dữ liệu cho bảng `teams`
INSERT INTO `teams` (`id`, `name`, `description`, `manager_id`) VALUES
(1, 'Đội phát triển phần mềm', 'Đội ngũ phát triển các sản phẩm phần mềm', 2),
(2, 'Đội hỗ trợ khách hàng', 'Đội ngũ hỗ trợ kỹ thuật và chăm sóc khách hàng', 3),
(3, 'Đội QA', 'Đội ngũ kiểm thử chất lượng phần mềm', 2);

-- Dữ liệu cho bảng `team_members`
INSERT INTO `team_members` (`id`, `user_id`, `team_id`) VALUES
(1, 4, 1),
(2, 5, 1),
(3, 6, 1),
(4, 4, 2),
(5, 5, 2),
(6, 7, 3);

-- Dữ liệu cho bảng `projects`
INSERT INTO `projects` (`id`, `name`, `description`, `start_date`, `end_date`, `manager_id`) VALUES
(1, 'Hệ thống HRM', 'Xây dựng hệ thống quản lý nhân sự', '2025-01-01', '2025-06-30', 2),
(2, 'Ứng dụng hỗ trợ', 'Phát triển ứng dụng hỗ trợ khách hàng', '2025-02-01', '2025-08-31', 3),
(3, 'Website bán hàng', 'Thiết kế website thương mại điện tử', '2025-03-01', '2025-09-30', 2),
(4, 'Ứng dụng nội bộ', 'Phát triển ứng dụng quản lý nội bộ', '2025-04-01', '2025-10-31', 3);

-- Dữ liệu cho bảng `tasks`
INSERT INTO `tasks` (`id`, `title`, `description`, `deadline`, `status`, `difficulty`, `estimated_time`, `github_link`, `project_id`) VALUES
(1, 'Thiết kế DB HRM', 'Thiết kế cơ sở dữ liệu cho HRM', '2025-02-15', 'Completed', 'Medium', 20.5, 'https://github.com/org/hrm-db', 1),
(2, 'API nhân viên', 'Xây dựng API quản lý nhân viên', '2025-03-15', 'In Progress', 'Hard', 30.0, 'https://github.com/org/hrm-api', 1),
(3, 'Giao diện HRM', 'Thiết kế UI cho HRM', '2025-04-10', 'Pending', 'Easy', 15.0, NULL, 1),
(4, 'API hỗ trợ', 'Xây dựng API cho ứng dụng hỗ trợ', '2025-05-01', 'In Progress', 'Medium', 25.0, 'https://github.com/org/support-api', 2),
(5, 'Kiểm thử hỗ trợ', 'Kiểm thử ứng dụng hỗ trợ', '2025-06-01', 'Pending', 'Easy', 10.0, NULL, 2),
(6, 'Thiết kế website', 'Thiết kế giao diện website bán hàng', '2025-07-01', 'Pending', 'Medium', 20.0, 'https://github.com/org/ecommerce-ui', 3),
(7, 'API nội bộ', 'Xây dựng API quản lý nội bộ', '2025-08-01', 'Pending', 'Hard', 35.0, 'https://github.com/org/internal-api', 4);

-- Dữ liệu cho bảng `task_assignments`
INSERT INTO `task_assignments` (`id`, `user_id`, `task_id`) VALUES
(1, 4, 1),
(2, 5, 2),
(3, 6, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 7);

-- Dữ liệu cho bảng `time_entries`
INSERT INTO `time_entries` (`id`, `start_time`, `end_time`, `task_id`, `user_id`) VALUES
(1, '2025-02-01 09:00:00.000000', '2025-02-01 17:00:00.000000', 1, 4),
(2, '2025-03-01 08:00:00.000000', '2025-03-01 12:00:00.000000', 2, 5),
(3, '2025-03-02 13:00:00.000000', '2025-03-02 17:00:00.000000', 2, 5),
(4, '2025-04-01 09:00:00.000000', NULL, 4, 4),
(5, '2025-04-02 08:00:00.000000', '2025-04-02 16:00:00.000000', 3, 6);

-- Dữ liệu cho bảng `kpis`
INSERT INTO `kpis` (`id`, `name`, `description`) VALUES
(1, 'Doanh thu dự án', 'Doanh thu hàng tháng từ dự án', 'Đo lường hiệu quả kinh doanh'),
(2, 'Hoàn thành nhiệm vụ', 'Tỷ lệ nhiệm vụ hoàn thành đúng hạn', 'Đo lường hiệu suất cá nhân'),
(3, 'Thời gian phản hồi', 'Thời gian trung bình phản hồi khách hàng', 'Đo lường chất lượng hỗ trợ'),
(4, 'Lỗi phát sinh', 'Số lỗi phát sinh trong dự án', 'Đo lường chất lượng sản phẩm');

-- Dữ liệu cho bảng `employee_kpis`
INSERT INTO `employee_kpis` (`id`, `target_value`, `actual_value`, `period`, `kpi_id`, `user_id`) VALUES
(1, '1000000', '1200000', '2025-Q1', 1, 2),
(2, '90', '85', '2025-Q1', 2, 4),
(3, '90', '95', '2025-Q1', 2, 5),
(4, '10', '8', '2025-Q1', 3, 4),
(5, '5', '3', '2025-Q1', 4, 6),
(6, '1000000', '950000', '2025-Q2', 1, 3);

-- Dữ liệu cho bảng `personal_goals`
INSERT INTO `personal_goals` (`id`, `goal_description`, `target_date`, `status`, `user_id`) VALUES
(1, 'Hoàn thành khóa học Python', '2025-05-01', 'In Progress', 4),
(2, 'Đạt chứng chỉ AWS', '2025-07-01', 'Pending', 5),
(3, 'Học ReactJS', '2025-06-01', 'Pending', 6),
(4, 'Cải thiện kỹ năng giao tiếp', '2025-08-01', 'In Progress', 7);

-- Dữ liệu cho bảng `forms`
INSERT INTO `forms` (`id`, `name`, `type`, `period`) VALUES
(1, 'Đánh giá nhân viên Q1', 'Survey', '2025-Q1'),
(2, 'Phản hồi dự án HRM', 'Feedback', '2025-Q2'),
(3, 'Đánh giá nhân viên Q2', 'Survey', '2025-Q2'),
(4, 'Phản hồi ứng dụng hỗ trợ', 'Feedback', '2025-Q3');

-- Dữ liệu cho bảng `form_questions`
INSERT INTO `form_questions` (`id`, `question_text`, `form_id`) VALUES
(1, 'Bạn đánh giá hiệu suất của nhân viên này như thế nào?', 1),
(2, 'Nhân viên có hoàn thành nhiệm vụ đúng hạn không?', 1),
(3, 'Dự án có đáp ứng được kỳ vọng không?', 2),
(4, 'Bạn đánh giá chất lượng dự án thế nào?', 2),
(5, 'Nhân viên có cải thiện kỹ năng không?', 3),
(6, 'Ứng dụng hỗ trợ có dễ sử dụng không?', 4);

-- Dữ liệu cho bảng `form_responses`
INSERT INTO `form_responses` (`id`, `answer`, `target_user_id`, `user_id`, `form_id`) VALUES
(1, 'Rất tốt', 4, 2, 1),
(2, 'Có', 4, 2, 1),
(3, 'Có, nhưng cần cải thiện tốc độ', 2, 4, 2),
(4, 'Khá tốt', 2, 5, 2),
(5, 'Có', 5, 3, 3),
(6, 'Rất dễ', 3, 4, 4);

-- Dữ liệu cho bảng `django_session`
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('abc123xyz', 'e30:{-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: humanity_os
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

USE humanity_os;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dữ liệu cho bảng `auth_group`
INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admin'),
(2, 'Manager'),
(3, 'Employee'),
(4, 'Intern');

-- Dữ liệu cho bảng `users`
INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `avatar`, `phone`) VALUES
(1, 'pbkdf2_sha256', '2025-03-23 10:00:00.000000', 1, 'admin', 'Quản Trị', 'Hệ Thống', 'admin@humanityos.com', 1, 1, '2025-01-01 00:00:00.000000', 'avatars/admin.jpg', '0901234567'),
(2, 'pbkdf2_sha256', NULL, 0, 'manager1', 'Nguyễn', 'Văn A', 'vana@humanityos.com', 1, 1, '2025-01-02 00:00:00.000000', 'avatars/manager1.jpg', '0912345678'),
(3, 'pbkdf2_sha256', NULL, 0, 'manager2', 'Trần', 'Thị D', 'thid@humanityos.com', 1, 1, '2025-01-03 00:00:00.000000', 'avatars/manager2.jpg', '0923456789'),
(4, 'pbkdf2_sha256', NULL, 0, 'employee1', 'Lê', 'Văn B', 'vanb@humanityos.com', 0, 1, '2025-01-04 00:00:00.000000', 'avatars/employee1.jpg', '0934567890'),
(5, 'pbkdf2_sha256', NULL, 0, 'employee2', 'Phạm', 'Thị C', 'thic@humanityos.com', 0, 1, '2025-01-05 00:00:00.000000', 'avatars/employee2.jpg', '0945678901'),
(6, 'pbkdf2_sha256', NULL, 0, 'employee3', 'Hoàng', 'Văn E', 'vane@humanityos.com', 0, 1, '2025-01-06 00:00:00.000000', 'avatars/employee3.jpg', '0956789012'),
(7, 'pbkdf2_sha256', NULL, 0, 'intern1', 'Ngô', 'Thị F', 'thif@humanityos.com', 0, 1, '2025-01-07 00:00:00.000000', 'avatars/intern1.jpg', '0967890123');

-- Lưu ý: Mật khẩu thực tế
-- admin: Admin@123
-- manager1: Manager@123
-- manager2: Manager@123
-- employee1: Employee@123
-- employee2: Employee@456
-- employee3: Employee@456
-- intern1: Intern@123

-- Dữ liệu cho bảng `users_groups`
INSERT INTO `users_groups` (`id`, `users_id`, `group_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 2),
(4, 4, 3),
(5, 5, 3),
(6, 6, 3),
(7, 7, 4);

-- Dữ liệu cho bảng `teams`
INSERT INTO `teams` (`id`, `name`, `description`, `manager_id`) VALUES
(1, 'Đội phát triển phần mềm', 'Đội ngũ phát triển các sản phẩm phần mềm', 2),
(2, 'Đội hỗ trợ khách hàng', 'Đội ngũ hỗ trợ kỹ thuật và chăm sóc khách hàng', 3),
(3, 'Đội QA', 'Đội ngũ kiểm thử chất lượng phần mềm', 2);

-- Dữ liệu cho bảng `team_members`
INSERT INTO `team_members` (`id`, `user_id`, `team_id`) VALUES
(1, 4, 1),
(2, 5, 1),
(3, 6, 1),
(4, 4, 2),
(5, 5, 2),
(6, 7, 3);

-- Dữ liệu cho bảng `projects`
INSERT INTO `projects` (`id`, `name`, `description`, `start_date`, `end_date`, `manager_id`) VALUES
(1, 'Hệ thống HRM', 'Xây dựng hệ thống quản lý nhân sự', '2025-01-01', '2025-06-30', 2),
(2, 'Ứng dụng hỗ trợ', 'Phát triển ứng dụng hỗ trợ khách hàng', '2025-02-01', '2025-08-31', 3),
(3, 'Website bán hàng', 'Thiết kế website thương mại điện tử', '2025-03-01', '2025-09-30', 2),
(4, 'Ứng dụng nội bộ', 'Phát triển ứng dụng quản lý nội bộ', '2025-04-01', '2025-10-31', 3);

-- Dữ liệu cho bảng `tasks`
INSERT INTO `tasks` (`id`, `title`, `description`, `deadline`, `status`, `difficulty`, `estimated_time`, `github_link`, `project_id`) VALUES
(1, 'Thiết kế DB HRM', 'Thiết kế cơ sở dữ liệu cho HRM', '2025-02-15', 'Completed', 'Medium', 20.5, 'https://github.com/org/hrm-db', 1),
(2, 'API nhân viên', 'Xây dựng API quản lý nhân viên', '2025-03-15', 'In Progress', 'Hard', 30.0, 'https://github.com/org/hrm-api', 1),
(3, 'Giao diện HRM', 'Thiết kế UI cho HRM', '2025-04-10', 'Pending', 'Easy', 15.0, NULL, 1),
(4, 'API hỗ trợ', 'Xây dựng API cho ứng dụng hỗ trợ', '2025-05-01', 'In Progress', 'Medium', 25.0, 'https://github.com/org/support-api', 2),
(5, 'Kiểm thử hỗ trợ', 'Kiểm thử ứng dụng hỗ trợ', '2025-06-01', 'Pending', 'Easy', 10.0, NULL, 2),
(6, 'Thiết kế website', 'Thiết kế giao diện website bán hàng', '2025-07-01', 'Pending', 'Medium', 20.0, 'https://github.com/org/ecommerce-ui', 3),
(7, 'API nội bộ', 'Xây dựng API quản lý nội bộ', '2025-08-01', 'Pending', 'Hard', 35.0, 'https://github.com/org/internal-api', 4);

-- Dữ liệu cho bảng `task_assignments`
INSERT INTO `task_assignments` (`id`, `user_id`, `task_id`) VALUES
(1, 4, 1),
(2, 5, 2),
(3, 6, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 7);

-- Dữ liệu cho bảng `time_entries`
INSERT INTO `time_entries` (`id`, `start_time`, `end_time`, `task_id`, `user_id`) VALUES
(1, '2025-02-01 09:00:00.000000', '2025-02-01 17:00:00.000000', 1, 4),
(2, '2025-03-01 08:00:00.000000', '2025-03-01 12:00:00.000000', 2, 5),
(3, '2025-03-02 13:00:00.000000', '2025-03-02 17:00:00.000000', 2, 5),
(4, '2025-04-01 09:00:00.000000', NULL, 4, 4),
(5, '2025-04-02 08:00:00.000000', '2025-04-02 16:00:00.000000', 3, 6);

-- Dữ liệu cho bảng `kpis`
INSERT INTO `kpis` (`id`, `name`, `description`) VALUES
(1, 'Doanh thu dự án', 'Doanh thu hàng tháng từ dự án', 'Đo lường hiệu quả kinh doanh'),
(2, 'Hoàn thành nhiệm vụ', 'Tỷ lệ nhiệm vụ hoàn thành đúng hạn', 'Đo lường hiệu suất cá nhân'),
(3, 'Thời gian phản hồi', 'Thời gian trung bình phản hồi khách hàng', 'Đo lường chất lượng hỗ trợ'),
(4, 'Lỗi phát sinh', 'Số lỗi phát sinh trong dự án', 'Đo lường chất lượng sản phẩm');

-- Dữ liệu cho bảng `employee_kpis`
INSERT INTO `employee_kpis` (`id`, `target_value`, `actual_value`, `period`, `kpi_id`, `user_id`) VALUES
(1, '1000000', '1200000', '2025-Q1', 1, 2),
(2, '90', '85', '2025-Q1', 2, 4),
(3, '90', '95', '2025-Q1', 2, 5),
(4, '10', '8', '2025-Q1', 3, 4),
(5, '5', '3', '2025-Q1', 4, 6),
(6, '1000000', '950000', '2025-Q2', 1, 3);

-- Dữ liệu cho bảng `personal_goals`
INSERT INTO `personal_goals` (`id`, `goal_description`, `target_date`, `status`, `user_id`) VALUES
(1, 'Hoàn thành khóa học Python', '2025-05-01', 'In Progress', 4),
(2, 'Đạt chứng chỉ AWS', '2025-07-01', 'Pending', 5),
(3, 'Học ReactJS', '2025-06-01', 'Pending', 6),
(4, 'Cải thiện kỹ năng giao tiếp', '2025-08-01', 'In Progress', 7);

-- Dữ liệu cho bảng `forms`
INSERT INTO `forms` (`id`, `name`, `type`, `period`) VALUES
(1, 'Đánh giá nhân viên Q1', 'Survey', '2025-Q1'),
(2, 'Phản hồi dự án HRM', 'Feedback', '2025-Q2'),
(3, 'Đánh giá nhân viên Q2', 'Survey', '2025-Q2'),
(4, 'Phản hồi ứng dụng hỗ trợ', 'Feedback', '2025-Q3');

-- Dữ liệu cho bảng `form_questions`
INSERT INTO `form_questions` (`id`, `question_text`, `form_id`) VALUES
(1, 'Bạn đánh giá hiệu suất của nhân viên này như thế nào?', 1),
(2, 'Nhân viên có hoàn thành nhiệm vụ đúng hạn không?', 1),
(3, 'Dự án có đáp ứng được kỳ vọng không?', 2),
(4, 'Bạn đánh giá chất lượng dự án thế nào?', 2),
(5, 'Nhân viên có cải thiện kỹ năng không?', 3),
(6, 'Ứng dụng hỗ trợ có dễ sử dụng không?', 4);

-- Dữ liệu cho bảng `form_responses`
INSERT INTO `form_responses` (`id`, `answer`, `target_user_id`, `user_id`, `form_id`) VALUES
(1, 'Rất tốt', 4, 2, 1),
(2, 'Có', 4, 2, 1),
(3, 'Có, nhưng cần cải thiện tốc độ', 2, 4, 2),
(4, 'Khá tốt', 2, 5, 2),
(5, 'Có', 5, 3, 3),
(6, 'Rất dễ', 3, 4, 4);

-- Dữ liệu cho bảng `django_session`
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('abc123xyz', 'e30:{", "2025-04-06 10:00:00.000000'),
('def456uvw', 'e30:{}", "2025-04-07 12:00:00.000000');

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23 15:04:19}", "2025-04-06 10:00:00.000000'),
('def456uvw', 'e30:{}", "2025-04-07 12:00:00.000000');

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23 15:04:19}", "2025-04-06 10:00:00.000000'),
('def456uvw', 'e30:{}", "2025-04-07 12:00:00.000000');

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23 15:04:19}

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dữ liệu cho bảng `auth_group`
INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admin'),
(2, 'Manager'),
(3, 'Employee'),
(4, 'Intern');

-- Dữ liệu cho bảng `users`
INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `avatar`, `phone`) VALUES
(3, 'pbkdf2_sha256$390000$X7oK9v8zL3pQ$abc123hashed', '2025-03-23 10:00:00.000000', 1, 'admin', 'Quản Trị', 'Hệ Thống', 'admin@humanityos.com', 1, 1, '2025-01-01 00:00:00.000000', 'avatars/admin.jpg', '0901234567'),
(4, 'pbkdf2_sha256$390000$X7oK9v8zL3pQ$xyz789hashed', NULL, 0, 'manager1', 'Nguyễn', 'Văn A', 'vana@humanityos.com', 1, 1, '2025-01-02 00:00:00.000000', 'avatars/manager1.jpg', '0912345678'),
(5, 'pbkdf2_sha256$390000$X7oK9v8zL3pQ$def456hashed', NULL, 0, 'manager2', 'Trần', 'Thị D', 'thid@humanityos.com', 1, 1, '2025-01-03 00:00:00.000000', 'avatars/manager2.jpg', '0923456789'),
(6, 'pbkdf2_sha256$390000$X7oK9v8zL3pQ$ghi789hashed', NULL, 0, 'employee1', 'Lê', 'Văn B', 'vanb@humanityos.com', 0, 1, '2025-01-04 00:00:00.000000', 'avatars/employee1.jpg', '0934567890'),
(7, 'pbkdf2_sha256$390000$X7oK9v8zL3pQ$jkl012hashed', NULL, 0, 'employee2', 'Phạm', 'Thị C', 'thic@humanityos.com', 0, 1, '2025-01-05 00:00:00.000000', 'avatars/employee2.jpg', '0945678901'),
(8, 'pbkdf2_sha256$390000$X7oK9v8zL3pQ$mno345hashed', NULL, 0, 'employee3', 'Hoàng', 'Văn E', 'vane@humanityos.com', 0, 1, '2025-01-06 00:00:00.000000', 'avatars/employee3.jpg', '0956789012'),
(9, 'pbkdf2_sha256$390000$X7oK9v8zL3pQ$pqr678hashed', NULL, 0, 'intern1', 'Ngô', 'Thị F', 'thif@humanityos.com', 0, 1, '2025-01-07 00:00:00.000000', 'avatars/intern1.jpg', '0967890123');

-- Lưu ý: Mật khẩu thực tế
-- admin: Admin@123
-- manager1: Manager@123
-- manager2: Manager@123
-- employee1: Employee@123
-- employee2: Employee@456
-- employee3: Employee@456
-- intern1: Intern@123

-- Dữ liệu cho bảng `users_groups`
INSERT INTO `users_groups` (`id`, `users_id`, `group_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 2),
(4, 4, 3),
(5, 5, 3),
(6, 6, 3),
(7, 7, 4);

-- Dữ liệu cho bảng `teams`
INSERT INTO `teams` (`id`, `name`, `description`, `manager_id`) VALUES
(1, 'Đội phát triển phần mềm', 'Đội ngũ phát triển các sản phẩm phần mềm', 2),
(2, 'Đội hỗ trợ khách hàng', 'Đội ngũ hỗ trợ kỹ thuật và chăm sóc khách hàng', 3),
(3, 'Đội QA', 'Đội ngũ kiểm thử chất lượng phần mềm', 2);

-- Dữ liệu cho bảng `team_members`
INSERT INTO `team_members` (`id`, `user_id`, `team_id`) VALUES
(1, 4, 1),
(2, 5, 1),
(3, 6, 1),
(4, 4, 2),
(5, 5, 2),
(6, 7, 3);

-- Dữ liệu cho bảng `projects`
INSERT INTO `projects` (`id`, `name`, `description`, `start_date`, `end_date`, `manager_id`) VALUES
(1, 'Hệ thống HRM', 'Xây dựng hệ thống quản lý nhân sự', '2025-01-01', '2025-06-30', 2),
(2, 'Ứng dụng hỗ trợ', 'Phát triển ứng dụng hỗ trợ khách hàng', '2025-02-01', '2025-08-31', 3),
(3, 'Website bán hàng', 'Thiết kế website thương mại điện tử', '2025-03-01', '2025-09-30', 2),
(4, 'Ứng dụng nội bộ', 'Phát triển ứng dụng quản lý nội bộ', '2025-04-01', '2025-10-31', 3);

-- Dữ liệu cho bảng `tasks`
INSERT INTO `tasks` (`id`, `title`, `description`, `deadline`, `status`, `difficulty`, `estimated_time`, `github_link`, `project_id`) VALUES
(1, 'Thiết kế DB HRM', 'Thiết kế cơ sở dữ liệu cho HRM', '2025-02-15', 'Completed', 'Medium', 20.5, 'https://github.com/org/hrm-db', 1),
(2, 'API nhân viên', 'Xây dựng API quản lý nhân viên', '2025-03-15', 'In Progress', 'Hard', 30.0, 'https://github.com/org/hrm-api', 1),
(3, 'Giao diện HRM', 'Thiết kế UI cho HRM', '2025-04-10', 'Pending', 'Easy', 15.0, NULL, 1),
(4, 'API hỗ trợ', 'Xây dựng API cho ứng dụng hỗ trợ', '2025-05-01', 'In Progress', 'Medium', 25.0, 'https://github.com/org/support-api', 2),
(5, 'Kiểm thử hỗ trợ', 'Kiểm thử ứng dụng hỗ trợ', '2025-06-01', 'Pending', 'Easy', 10.0, NULL, 2),
(6, 'Thiết kế website', 'Thiết kế giao diện website bán hàng', '2025-07-01', 'Pending', 'Medium', 20.0, 'https://github.com/org/ecommerce-ui', 3),
(7, 'API nội bộ', 'Xây dựng API quản lý nội bộ', '2025-08-01', 'Pending', 'Hard', 35.0, 'https://github.com/org/internal-api', 4);

-- Dữ liệu cho bảng `task_assignments`
INSERT INTO `task_assignments` (`id`, `user_id`, `task_id`) VALUES
(1, 4, 1),
(2, 5, 2),
(3, 6, 3),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6),
(7, 7, 7);

-- Dữ liệu cho bảng `time_entries`
INSERT INTO `time_entries` (`id`, `start_time`, `end_time`, `task_id`, `user_id`) VALUES
(1, '2025-02-01 09:00:00.000000', '2025-02-01 17:00:00.000000', 1, 4),
(2, '2025-03-01 08:00:00.000000', '2025-03-01 12:00:00.000000', 2, 5),
(3, '2025-03-02 13:00:00.000000', '2025-03-02 17:00:00.000000', 2, 5),
(4, '2025-04-01 09:00:00.000000', NULL, 4, 4),
(5, '2025-04-02 08:00:00.000000', '2025-04-02 16:00:00.000000', 3, 6);

-- Dữ liệu cho bảng `kpis`
INSERT INTO `kpis` (`id`, `name`, `description`) VALUES
(1, 'Doanh thu dự án', 'Doanh thu hàng tháng từ dự án', 'Đo lường hiệu quả kinh doanh'),
(2, 'Hoàn thành nhiệm vụ', 'Tỷ lệ nhiệm vụ hoàn thành đúng hạn', 'Đo lường hiệu suất cá nhân'),
(3, 'Thời gian phản hồi', 'Thời gian trung bình phản hồi khách hàng', 'Đo lường chất lượng hỗ trợ'),
(4, 'Lỗi phát sinh', 'Số lỗi phát sinh trong dự án', 'Đo lường chất lượng sản phẩm');

-- Dữ liệu cho bảng `employee_kpis`
INSERT INTO `employee_kpis` (`id`, `target_value`, `actual_value`, `period`, `kpi_id`, `user_id`) VALUES
(1, '1000000', '1200000', '2025-Q1', 1, 2),
(2, '90', '85', '2025-Q1', 2, 4),
(3, '90', '95', '2025-Q1', 2, 5),
(4, '10', '8', '2025-Q1', 3, 4),
(5, '5', '3', '2025-Q1', 4, 6),
(6, '1000000', '950000', '2025-Q2', 1, 3);

-- Dữ liệu cho bảng `personal_goals`
INSERT INTO `personal_goals` (`id`, `goal_description`, `target_date`, `status`, `user_id`) VALUES
(1, 'Hoàn thành khóa học Python', '2025-05-01', 'In Progress', 4),
(2, 'Đạt chứng chỉ AWS', '2025-07-01', 'Pending', 5),
(3, 'Học ReactJS', '2025-06-01', 'Pending', 6),
(4, 'Cải thiện kỹ năng giao tiếp', '2025-08-01', 'In Progress', 7);

-- Dữ liệu cho bảng `forms`
INSERT INTO `forms` (`id`, `name`, `type`, `period`) VALUES
(1, 'Đánh giá nhân viên Q1', 'Survey', '2025-Q1'),
(2, 'Phản hồi dự án HRM', 'Feedback', '2025-Q2'),
(3, 'Đánh giá nhân viên Q2', 'Survey', '2025-Q2'),
(4, 'Phản hồi ứng dụng hỗ trợ', 'Feedback', '2025-Q3');

-- Dữ liệu cho bảng `form_questions`
INSERT INTO `form_questions` (`id`, `question_text`, `form_id`) VALUES
(1, 'Bạn đánh giá hiệu suất của nhân viên này như thế nào?', 1),
(2, 'Nhân viên có hoàn thành nhiệm vụ đúng hạn không?', 1),
(3, 'Dự án có đáp ứng được kỳ vọng không?', 2),
(4, 'Bạn đánh giá chất lượng dự án thế nào?', 2),
(5, 'Nhân viên có cải thiện kỹ năng không?', 3),
(6, 'Ứng dụng hỗ trợ có dễ sử dụng không?', 4);

-- Dữ liệu cho bảng `form_responses`
INSERT INTO `form_responses` (`id`, `answer`, `target_user_id`, `user_id`, `form_id`) VALUES
(1, 'Rất tốt', 4, 2, 1),
(2, 'Có', 4, 2, 1),
(3, 'Có, nhưng cần cải thiện tốc độ', 2, 4, 2),
(4, 'Khá tốt', 2, 5, 2),
(5, 'Có', 5, 3, 3),
(6, 'Rất dễ', 3, 4, 4);

-- Dữ liệu cho bảng `django_session`
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('abc123xyz', 'e30:{}", "2025-04-06 10:00:00.000000'),
('def456uvw', 'e30:{}", "2025-04-07 12:00:00.000000');

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-23 15:04:19