-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: humanity_os
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ai_chat_messages`
--

DROP TABLE IF EXISTS `ai_chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_chat_messages` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(10) NOT NULL,
  `content` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ai_chat_messages_user_id_6152a183_fk_users_id` (`user_id`),
  CONSTRAINT `ai_chat_messages_user_id_6152a183_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_chat_messages`
--

LOCK TABLES `ai_chat_messages` WRITE;
/*!40000 ALTER TABLE `ai_chat_messages` DISABLE KEYS */;
INSERT INTO `ai_chat_messages` VALUES (1,'user','Giải thích về trang web này và cách sử dụng','2025-05-15 17:24:41.317402',9),(2,'model','Chào Lộc Huỳnh! Humanity OS là hệ thống quản lý nhân sự và công việc giúp bạn theo dõi công việc, điểm danh và đánh giá hiệu suất.  Hiện tại bạn chưa check-in, cần check-in ngay để cập nhật thời gian làm việc. Bạn có 20 công việc, 5 công việc quá hạn, cần ưu tiên hoàn thành chúng.  KPI hiện tại là 75%, cần cải thiện để đạt mục tiêu.  Hệ thống cho thấy bạn làm việc nhiều giờ hơn quy định (143.79%).  Hãy tập trung vào các công việc quan trọng, đặc biệt là `Push Notification System` và `Offline Mode Support` theo gợi ý của hệ thống để nâng cao hiệu suất và giảm số công việc quá hạn.  Bạn có thể xem chi tiết các dự án, công việc, KPI và lịch sử điểm danh trên giao diện hệ thống, rất dễ sử dụng.  Hãy liên hệ bộ phận hỗ trợ nếu cần giúp đỡ thêm.\n','2025-05-15 17:24:41.325983',9),(3,'user','Giải thích về trang web này và cách sử dụng','2025-05-15 17:35:26.822087',9),(4,'model','Chào Lộc Huỳnh! Humanity OS là hệ thống quản lý công việc và nhân sự giúp bạn theo dõi hiệu suất làm việc.  Giao diện đơn giản, gồm bảng điều khiển tổng quan (Dashboard) hiển thị công việc, KPI, thời gian làm việc và các menu điều hướng (Sidebar).\n\nBạn cần chú ý:\n\n* **Điểm danh:**  Hãy check-in/check-out đúng giờ để hệ thống tính toán thời gian làm việc chính xác.  Lưu ý check-in lúc 17:29:41 ngày 15/05/2025 không hợp lệ.\n* **Công việc quá hạn:**  Bạn có 5 công việc quá hạn, cần ưu tiên hoàn thành, đặc biệt là \"Push Notification System\" và \"Offline Mode Support\".\n* **KPI:** Hiệu suất KPI hiện tại là 75%, cần cải thiện.\n* **Thời gian làm việc:** Bạn đang làm việc nhiều hơn quy định (143.79%). Hãy quản lý thời gian hiệu quả hơn.\n\n\nĐể sử dụng hệ thống, bạn vào các mục trong Sidebar:  Dự án để xem tiến độ, Công việc để quản lý task, KPI để xem chỉ số hiệu quả, Điểm danh để xem lịch sử và Hồ sơ cá nhân để cập nhật thông tin. Trợ lý AI hỗ trợ giải đáp thắc mắc.  Hãy tập trung hoàn thành các công việc quá hạn và nâng cao KPI để đạt hiệu quả tốt nhất.\n','2025-05-15 17:35:26.830974',9),(5,'user','Giải thích về trang web này và cách sử dụng','2025-05-15 18:11:03.480212',9),(6,'model','Chào Lộc Huỳnh! Humanity OS là hệ thống quản lý công việc và nhân sự giúp bạn theo dõi hiệu suất.  Giao diện gồm bảng điều khiển tổng quan (Dashboard) và menu điều hướng (Sidebar).\n\n* **Điểm danh:**  Hãy check-in/check-out đúng giờ để hệ thống tính toán chính xác.  Check-in lúc 17:29:41 ngày 15/05/2025 không hợp lệ.\n* **Công việc:** Bạn có 20 công việc, 5 quá hạn (ưu tiên \"Push Notification System\" và \"Offline Mode Support\").  KPI hiện tại 75%, cần cải thiện.\n* **Thời gian:** Bạn làm việc vượt quá quy định (143.79%).  Quản lý thời gian hiệu quả hơn.\n\nSử dụng các mục trong Sidebar: Dự án, Công việc, KPI, Điểm danh, Hồ sơ.  Trợ lý AI hỗ trợ.  Tập trung hoàn thành công việc quá hạn và cải thiện KPI.  Thời gian làm việc nhiều quá có thể ảnh hưởng đến hiệu quả, cần xem xét lại.\n','2025-05-15 18:11:03.488634',9),(7,'user','Giải thích về trang web này và cách sử dụng','2025-05-15 18:19:00.887342',9),(8,'model','Chào Lộc Huỳnh! Humanity OS là hệ thống quản lý công việc và nhân sự giúp bạn quản lý hiệu quả thời gian và công việc.  Giao diện đơn giản với bảng điều khiển (Dashboard) tổng quan về công việc, KPI và thời gian làm việc, cùng thanh điều hướng (Sidebar) để truy cập các chức năng.\n\n* **Điểm danh:** Check-in/check-out đúng giờ rất quan trọng.  Check-in 17:29:41 ngày 15/05/2025 không hợp lệ, hãy kiểm tra lại.\n* **Công việc:**  Bạn có 20 công việc, 5 quá hạn.  Ưu tiên hoàn thành \"Push Notification System\" và \"Offline Mode Support\".\n* **KPI:**  KPI hiện tại là 75%, cần cải thiện.\n* **Thời gian:** Bạn làm việc vượt quá quy định (143.79%), hãy quản lý thời gian hiệu quả hơn.\n\nSử dụng các mục trong Sidebar: *Dự án*, *Công việc*, *KPI*, *Điểm danh*, *Hồ sơ* để quản lý mọi thứ.  Trợ lý AI sẵn sàng hỗ trợ.  Tập trung vào công việc quá hạn và cải thiện KPI.  Giảm thời gian làm việc để tăng hiệu quả.\n','2025-05-15 18:19:00.896232',9),(9,'user','Tiếp tục chi tiết hơn','2025-05-15 18:19:13.761034',9),(10,'model','Chào Lộc Huỳnh!  Humanity OS giúp bạn quản lý công việc và hiệu suất.  Hiện tại, bạn có 20 công việc, 5 trong số đó quá hạn.  KPI của bạn là 75%, cần cải thiện.  Thời gian làm việc vượt quá quy định (143.79%).  Check-in lúc 17:29:41 ngày 15/05/2025 không hợp lệ, cần kiểm tra lại.\n\n* **Ưu tiên:** Hoàn thành \"Push Notification System\" và \"Offline Mode Support\".\n* **Sử dụng:**  Thanh bên (Sidebar) có các mục: Dự án, Công việc, KPI, Điểm danh, Hồ sơ.  Trợ lý AI hỗ trợ.\n* **Cải thiện:**  Quản lý thời gian hiệu quả hơn để đạt KPI cao hơn và giảm số công việc quá hạn.  Check-in/check-out đúng giờ.\n\nHãy tập trung vào công việc quan trọng, quản lý thời gian hợp lý và liên hệ hỗ trợ nếu cần.  Tôi có thể giúp gì thêm cho bạn không?\n','2025-05-15 18:19:13.769831',9),(11,'user','Giải thích về trang web này và cách sử dụng','2025-05-15 18:26:08.629972',9),(12,'model','Chào Lộc Huỳnh! Humanity OS là hệ thống quản lý công việc và nhân sự giúp bạn theo dõi hiệu suất.  Giao diện có bảng điều khiển (Dashboard) hiển thị tổng quan và thanh điều hướng (Sidebar) để truy cập các chức năng: Dự án, Công việc, KPI, Điểm danh, Hồ sơ.\n\n* **Điểm danh:**  Hãy check-in/check-out đúng giờ.  Check-in lúc 17:29:41 ngày 15/05/2025 không hợp lệ.\n* **Công việc:** Bạn có 20 công việc, 5 quá hạn. Ưu tiên \"Push Notification System\" và \"Offline Mode Support\". KPI hiện tại 75%, cần cải thiện.\n* **Thời gian:** Bạn làm việc vượt quá quy định (143.79%).  Quản lý thời gian hiệu quả hơn.\n\nTrợ lý AI sẵn sàng hỗ trợ.  Tập trung vào công việc quá hạn, cải thiện KPI và quản lý thời gian để đạt hiệu quả tối đa.  Check-in/check-out không hợp lệ ảnh hưởng đến thống kê thời gian, cần điều chỉnh.\n','2025-05-15 18:26:08.638685',9),(13,'user','Giải thích về trang web này và cách sử dụng','2025-05-15 18:39:44.762329',9),(14,'model','Chào Lộc Huỳnh! Humanity OS là hệ thống quản lý công việc và nhân sự giúp bạn theo dõi hiệu suất.  Giao diện gồm bảng điều khiển (Dashboard) và thanh điều hướng (Sidebar).  \n\n* **Điểm danh:** Check-in/check-out đúng giờ rất quan trọng.  Check-in 17:29:41 ngày 15/05/2025 không hợp lệ, cần sửa lại.\n* **Công việc:** Bạn có 20 công việc, 5 quá hạn, cần ưu tiên \"Push Notification System\" và \"Offline Mode Support\". KPI hiện tại 75%, cần cải thiện.\n* **Thời gian:** Bạn làm việc vượt quá quy định (143.79%), hãy quản lý thời gian hiệu quả hơn.\n\nSử dụng Sidebar để điều hướng đến các chức năng: Dự án, Công việc, KPI, Điểm danh, Hồ sơ.  Trợ lý AI hỗ trợ bạn.  Tập trung hoàn thành công việc quá hạn và nâng cao KPI.  Giảm thời gian làm việc để tăng hiệu quả.  Hãy kiểm tra lại lịch sử điểm danh để đảm bảo tính chính xác của dữ liệu.\n','2025-05-15 18:39:44.770892',9),(15,'user','Phần điểm danh bạn cần nói sửa gì','2025-05-15 18:53:49.281875',9),(16,'model','Chào Lộc Huỳnh!  Humanity OS giúp bạn quản lý công việc và hiệu suất.  Dữ liệu cho thấy bạn cần chú trọng vào điểm danh:  Check-in lúc 17:29:41 ngày 15/05/2025 không hợp lệ, ảnh hưởng đến tính toán thời gian làm việc và KPI.  Hãy kiểm tra lại và sửa thời gian check-in cho chính xác.\n\n* **Công việc quá hạn:** 5 công việc cần ưu tiên, đặc biệt là \"Push Notification System\" và \"Offline Mode Support\".\n* **KPI thấp:** KPI hiện tại 75%, cần cải thiện bằng cách hoàn thành các công việc đúng hạn và quản lý thời gian hiệu quả hơn.\n* **Thời gian làm việc:** Bạn làm việc vượt quá 100% (143.79%),  hãy cân bằng giữa công việc và nghỉ ngơi để đạt hiệu quả cao nhất.\n\nHumanity OS cung cấp các chức năng quản lý dự án, công việc, KPI và điểm danh (xem Sidebar).  Trợ lý AI luôn sẵn sàng hỗ trợ.  Hãy tập trung vào công việc quan trọng, quản lý thời gian hợp lý và đảm bảo check-in/check-out chính xác để có báo cáo hiệu suất chính xác.\n','2025-05-15 18:53:49.290514',9),(17,'user','Bạn hiểu gì về trang web này có thể cung cấp, trình bày cho tôi không','2025-05-15 19:08:09.646486',9),(18,'model','Chào Lộc Huỳnh! Humanity OS là hệ thống quản lý nhân sự và công việc giúp bạn theo dõi hiệu suất và quản lý thời gian hiệu quả.  Như dữ liệu cho thấy, bạn đang gặp một số vấn đề cần giải quyết:\n\n**1. Điểm danh không hợp lệ:** Check-in ngày 15/05/2025 lúc 17:29:41 không hợp lệ.  Điều này ảnh hưởng đến tính toán thời gian làm việc và KPI của bạn.  **Hãy kiểm tra lại lịch sử điểm danh và sửa chữa thời gian check-in/check-out cho chính xác.**  Bạn có thể tìm thấy lịch sử điểm danh và chức năng chỉnh sửa trong mục \"Điểm danh\" trên thanh điều hướng bên (Sidebar).\n\n**2. Công việc quá hạn:** Bạn có 5 công việc quá hạn, ảnh hưởng đến KPI và hiệu suất tổng thể.  **Ưu tiên hoàn thành \"Push Notification System\" và \"Offline Mode Support\" trước, vì chúng có vẻ quan trọng và đang trong tình trạng \"To-do\" hoặc \"In progress\".**  Bạn có thể xem chi tiết các công việc quá hạn trong mục \"Công việc\" trên Sidebar.  Hãy cập nhật trạng thái và tiến độ công việc thường xuyên.\n\n**3. KPI thấp:** KPI hiện tại của bạn là 75%, chưa đạt mục tiêu.  **Cải thiện KPI bằng cách hoàn thành công việc đúng hạn, quản lý thời gian hiệu quả hơn và đảm bảo check-in/check-out chính xác.**  Mục \"KPI\" trên Sidebar cho phép bạn theo dõi chỉ số hiệu quả cá nhân.\n\n**4. Thời gian làm việc vượt quá quy định:** Bạn làm việc vượt quá quy định (143.79%).  **Mặc dù điều này cho thấy sự tận tâm, nhưng cần cân bằng giữa công việc và nghỉ ngơi để đảm bảo sức khỏe và hiệu quả làm việc lâu dài.  Hãy phân bổ thời gian hợp lý hơn cho từng công việc.**  Bạn có thể xem phân bổ thời gian theo dự án trong mục \"Thời gian làm việc\" (có thể nằm trong mục \"Điểm danh\" hoặc \"Công việc\").\n\n**5. Sử dụng Humanity OS:**  Giao diện chính gồm Dashboard (tổng quan) và Sidebar (điều hướng).  Các chức năng chính:\n\n* **Dự án:** Quản lý các dự án bạn đang tham gia.\n* **Công việc:** Xem, cập nhật trạng thái và tiến độ công việc.\n* **KPI:** Theo dõi chỉ số hiệu quả cá nhân.\n* **Điểm danh:** Check-in/check-out và xem lịch sử điểm danh.\n* **Hồ sơ:** Quản lý thông tin cá nhân.\n\n**Trợ lý AI** luôn sẵn sàng hỗ trợ bạn.  Hãy tận dụng các tính năng này để quản lý công việc hiệu quả hơn.\n\nTóm lại, tập trung vào việc sửa chữa điểm danh không hợp lệ, ưu tiên hoàn thành các công việc quá hạn, đặc biệt là hai công việc được đề cập, và quản lý thời gian hiệu quả hơn để cải thiện KPI.  Humanity OS cung cấp đầy đủ công cụ để bạn làm điều đó.\n','2025-05-15 19:08:09.657162',9),(19,'user','Tôi nên thực hiện task Inventory Dashboard trong bao lâu là hợp lý','2025-05-15 19:10:00.262536',9),(20,'model','Chào Lộc Huỳnh!  Để trả lời câu hỏi \"Tôi nên thực hiện task Inventory Dashboard trong bao lâu là hợp lý?\", cần xem xét nhiều yếu tố:\n\n* **Độ phức tạp của task:** Task Inventory Dashboard có độ khó \"Medium\" (trung bình).  Điều này cho thấy thời gian hoàn thành không quá ngắn cũng không quá dài.\n* **Thời hạn:**  Deadline của task là 30/04/2025, hiện đã quá hạn 15 ngày.  Vì vậy, cần ưu tiên hoàn thành càng sớm càng tốt.\n* **Thời gian đã dành:**  Dữ liệu hiện tại không cho biết bạn đã dành bao nhiêu thời gian cho task này.\n* **Khả năng của bạn:**  Hiệu suất KPI hiện tại của bạn là 75%, và thời gian làm việc vượt quá quy định. Điều này cho thấy bạn cần quản lý thời gian hiệu quả hơn.\n* **Các task khác:** Bạn có 19 task khác, 4 task đã hoàn thành, và 5 task quá hạn.  Cần cân nhắc thời gian dành cho các task khác khi lên kế hoạch cho Inventory Dashboard.\n\n\n**Gợi ý:**\n\n* **Phân tích task:** Chia nhỏ task Inventory Dashboard thành các sub-task nhỏ hơn, dễ quản lý hơn.  Điều này giúp bạn ước lượng thời gian chính xác hơn.\n* **Ước lượng thời gian:**  Dựa trên độ khó \"Medium\" và kinh nghiệm của bạn, ước lượng thời gian cần thiết cho mỗi sub-task.  Tổng hợp lại để có thời gian hoàn thành tổng thể.\n* **Lên kế hoạch:**  Lập kế hoạch cụ thể với thời gian bắt đầu và kết thúc cho từng sub-task.  Đảm bảo thời gian hoàn thành tổng thể không ảnh hưởng đến các task quan trọng khác, đặc biệt là những task quá hạn.\n* **Cập nhật tiến độ:**  Cập nhật tiến độ thường xuyên trên Humanity OS để theo dõi hiệu quả công việc.\n\n\n**Không có câu trả lời chính xác về thời gian hoàn thành.**  Bạn cần tự ước lượng dựa trên các yếu tố trên và kinh nghiệm cá nhân.  Hãy sử dụng Humanity OS để quản lý thời gian và tiến độ công việc hiệu quả hơn.  Nếu gặp khó khăn, hãy liên hệ với quản lý hoặc đồng nghiệp để được hỗ trợ.  Hãy nhớ ưu tiên hoàn thành các task quá hạn trước.\n','2025-05-15 19:10:00.271370',9),(21,'user','Phần điểm danh bạn cần nói sửa gì','2025-05-16 00:24:19.839803',9),(22,'model','Chào Lộc Huỳnh!  Như bạn đã thấy, Humanity OS báo cáo một số điểm danh của bạn không hợp lệ (17:29:41 ngày 15/05 và thời điểm tương tự ngày 16/05).  Điều này ảnh hưởng đến tính toán thời gian làm việc và KPI.  Bạn **cần sửa lại thời gian check-in/check-out cho chính xác**.  \n\nĐể làm điều này, hãy vào mục **Điểm danh** trên thanh điều hướng bên (Sidebar).  Tìm ngày 15/05 và 16/05.  Hệ thống sẽ cho phép bạn chỉnh sửa hoặc xóa các điểm danh không chính xác.  Sau khi sửa xong, hệ thống sẽ tự động cập nhật lại thời gian làm việc và KPI của bạn.  Hãy đảm bảo check-in/check-out đúng giờ trong những ngày tiếp theo để tránh tình trạng tương tự.\n\nNgoài ra, hãy ưu tiên hoàn thành các công việc quá hạn, đặc biệt là \"Push Notification System\" và \"Offline Mode Support\".  Quản lý thời gian hiệu quả hơn để đạt KPI cao hơn.  Hãy tận dụng trợ lý AI để được hỗ trợ trong quá trình làm việc.  Nếu cần hỗ trợ thêm, đừng ngần ngại liên hệ bộ phận hỗ trợ của Humanity OS.\n','2025-05-16 00:24:19.848727',9),(23,'user','Bạn là ai dựa trên model nào','2025-05-17 08:28:34.248335',9),(24,'model','Tôi là một mô hình ngôn ngữ lớn, được huấn luyện bởi Google.  Tôi không có tên, vai trò hay bộ phận như Lộc Huỳnh trong Humanity OS.  Tôi chỉ là một trợ lý AI, được lập trình để xử lý và trả lời câu hỏi của bạn dựa trên dữ liệu bạn cung cấp về hệ thống Humanity OS.  Tôi không có kinh nghiệm làm việc thực tế hay quyền truy cập vào hệ thống Humanity OS.  Tôi chỉ có thể trả lời dựa trên thông tin bạn đã cung cấp.\n','2025-05-17 08:28:34.257656',9),(25,'user','Bạn hiểu gì về trang web này có thể cung cấp, trình bày cho tôi không','2025-05-17 14:45:32.950776',9),(26,'model','Chào Lộc Huỳnh!  Humanity OS là hệ thống quản lý nhân sự và công việc của bạn.  Dữ liệu hiện tại cho thấy bạn cần chú trọng một số điểm:\n\n* **Điểm danh không chính xác:**  Các lần check-in ngày 15/05 (17:29:41) và 16/05 (00:22:18) không hợp lệ.  Vào mục **Điểm danh** (trong Sidebar), tìm các ngày này, sửa hoặc xóa các mục không chính xác để hệ thống tính toán lại thời gian làm việc và KPI.\n\n* **Nhiều công việc quá hạn:**  Bạn có 5 công việc quá hạn, ảnh hưởng lớn đến KPI.  Ưu tiên hoàn thành **\"Phát triển module quản lý nhân viên,\" \"Phát triển module chấm công,\" \"Kiểm thử hệ thống,\" \"Phát triển module tin tức,\" và \"Kiểm thử và triển khai.\"**  Cập nhật trạng thái công việc thường xuyên trong mục **Công việc** (Sidebar).\n\n* **KPI cần cải thiện:**  KPI hiện tại là 83.33%, cần nỗ lực hơn để đạt hiệu suất cao hơn.  Hoàn thành các công việc đúng hạn và quản lý thời gian hiệu quả là chìa khóa.  Xem chi tiết KPI trong mục **KPI** (Sidebar).\n\n* **Thời gian làm việc:** Mặc dù tỷ lệ hiệu suất thời gian là 95.87%, bạn cần cân bằng thời gian làm việc để tránh quá tải.  Phân bổ thời gian hợp lý cho từng công việc.\n\n* **Thời gian làm việc hôm nay:** 0 giờ.  Hãy chắc chắn check-in/check-out đúng giờ.\n\n**Humanity OS cung cấp các tính năng:**\n\n* **Dashboard:** Tổng quan về công việc, thời gian, KPI, và tiến độ dự án.\n* **Sidebar:**  Điều hướng nhanh đến các mục: Dự án, Công việc, KPI, Điểm danh, Hồ sơ.\n* **Dự án/Công việc:** Quản lý dự án, tạo, phân công và theo dõi công việc.\n* **KPI:**  Theo dõi chỉ số hiệu quả cá nhân.\n* **Điểm danh:**  Check-in/check-out, xem lịch sử điểm danh.\n* **Hồ sơ:**  Quản lý thông tin cá nhân.\n* **Trợ lý AI:**  Hỗ trợ giải đáp thắc mắc và gợi ý.\n\n\nTóm lại, tập trung vào việc sửa lỗi điểm danh, hoàn thành các công việc quá hạn và quản lý thời gian hiệu quả để đạt được KPI cao hơn.  Hãy tận dụng đầy đủ các tính năng của Humanity OS để tối ưu hóa công việc.\n','2025-05-17 14:45:32.956858',9),(27,'user','Thống kê của tôi tháng này tốt không','2025-05-18 11:04:06.156183',9),(28,'model','Chào Lộc Huỳnh! Để đánh giá hiệu suất tháng này, cần xem xét nhiều yếu tố:\n\n* **KPI:** KPI tổng thể của bạn đạt 83.33%, khá tốt. Tuy nhiên, một số chỉ số thành phần như \"Số lượng task hoàn thành\" chỉ đạt 80%, cần cải thiện.  Hãy xem xét kỹ các mục tiêu và xem mình cần nỗ lực ở đâu để đạt được 100%.\n\n* **Công việc:** Bạn đã hoàn thành 1/7 công việc và có 4 công việc quá hạn.  Đây là điểm cần cải thiện đáng kể.  Hãy ưu tiên hoàn thành các công việc quá hạn, đặc biệt là \"Phát triển module quản lý nhân viên\" và \"Phát triển module chấm công\" vì chúng có độ khó cao và đã quá hạn rất lâu.\n\n* **Thời gian làm việc:** Trung bình bạn làm việc 6.36 giờ/ngày, tỷ lệ hiệu suất thời gian là 79.51%.  Mặc dù đã hoàn thành một số công việc, nhưng thời gian làm việc nhiều hơn quy định và có nhiều công việc quá hạn cho thấy bạn cần cải thiện khả năng quản lý thời gian.  Hãy phân tích xem nguyên nhân nào khiến bạn làm việc nhiều giờ nhưng vẫn có nhiều công việc quá hạn.  Có thể bạn cần chia nhỏ công việc thành các task nhỏ hơn, dễ quản lý hơn.\n\n* **Điểm danh:**  Bạn đã có một số lần check-in/check-out không hợp lệ.  Điều này ảnh hưởng đến tính toán thời gian làm việc chính xác và có thể làm giảm KPI.  Hãy đảm bảo check-in/check-out đúng giờ và chính xác trong những ngày còn lại của tháng.\n\n**Tổng kết:**\n\nThống kê tháng này của bạn cho thấy điểm mạnh ở KPI tổng thể, tuy nhiên vẫn còn nhiều điểm yếu cần cải thiện, đặc biệt là về việc quản lý thời gian và hoàn thành công việc đúng hạn.  Tập trung vào việc hoàn thành các công việc quá hạn và cải thiện quản lý thời gian sẽ giúp bạn nâng cao hiệu suất tổng thể.  Hãy sử dụng Humanity OS để theo dõi tiến độ công việc và cải thiện hiệu quả làm việc.  Nếu cần hỗ trợ, hãy liên hệ với quản lý hoặc đồng nghiệp.\n','2025-05-18 11:04:06.165740',9),(29,'user','Giải thích về trang web này và cách sử dụng','2025-05-22 06:18:04.410480',1),(30,'model','Chào lochuynh,\n\nHumanity OS là một hệ thống quản lý nhân sự và công việc trực tuyến, giúp bạn theo dõi công việc, quản lý thời gian và đánh giá hiệu suất một cách hiệu quả.  Là một nhân viên, bạn sẽ chủ yếu tương tác với các tính năng sau:\n\n**1. Điểm danh:**\n\n* **Check-in/Check-out:**  Bạn cần check-in và check-out mỗi ngày bằng tính năng nhận diện khuôn mặt và vị trí địa lý (nếu được cài đặt).  Hệ thống sẽ tự động ghi nhận thời gian làm việc của bạn.  Hiện tại bạn chưa check-in/check-out hôm nay, hãy làm điều này ngay để hệ thống cập nhật thời gian làm việc chính xác.\n* **Xem lịch sử điểm danh:**  Bạn có thể xem lịch sử điểm danh của mình để theo dõi thời gian làm việc hàng ngày, hàng tuần và hàng tháng.  Hiện tại lịch sử điểm danh của bạn đang trống.\n\n**2. Quản lý công việc:**\n\n* **Xem công việc được giao:** Bạn có thể xem danh sách công việc được giao, trạng thái (To-do, In progress, Completed, Late), hạn chót và các thông tin liên quan.  Bạn đã hoàn thành một công việc (\"Phân tích yêu cầu\") và hiện không có công việc nào quá hạn.\n* **Cập nhật trạng thái công việc:**  Hãy cập nhật trạng thái công việc của mình thường xuyên để quản lý dự án được chính xác.\n* **Xem tiến độ dự án:** Bạn có thể xem tiến độ của các dự án mình tham gia, bao gồm \"Dự án Quản lý Nhân sự\".\n\n**3. Theo dõi KPI:**\n\n* **Xem KPI cá nhân:**  Hiện tại, KPI của bạn đang ở mức 0%.  Điều này cần được xem xét và tìm hiểu nguyên nhân.  Hãy liên hệ với quản lý để hiểu rõ hơn về KPI và cách cải thiện.  Việc cập nhật thời gian làm việc chính xác và hoàn thành công việc đúng hạn sẽ giúp cải thiện KPI.\n\n**4. Sử dụng Trợ lý AI:**\n\n* **Hỏi đáp và hỗ trợ:**  Nếu gặp bất kỳ khó khăn nào trong quá trình sử dụng hệ thống, hãy sử dụng trợ lý AI để được hỗ trợ.\n\n**Gợi ý cải thiện:**\n\n* **Check-in/Check-out ngay lập tức:**  Việc này rất quan trọng để đảm bảo tính chính xác của thời gian làm việc và KPI.\n* **Kiểm tra KPI:**  Hãy liên hệ với quản lý để hiểu rõ hơn về KPI và cách thức cải thiện.\n* **Cập nhật thông tin cá nhân:**  Hãy cập nhật bộ phận và ngày tham gia để hồ sơ của bạn được đầy đủ.\n* **Xem xét phân bổ thời gian:** Bạn đã dành 14.5 giờ cho Dự án Quản lý Nhân sự. Hãy cân nhắc xem liệu thời gian này có phù hợp với tiến độ và khối lượng công việc hay không.\n\n\n**Cách sử dụng hệ thống:**\n\n* **Đăng nhập:**  Sử dụng tên đăng nhập \"lochuynh\" để đăng nhập vào hệ thống.\n* **Điều hướng:**  Sử dụng thanh sidebar để điều hướng đến các chức năng chính (Dự án, Công việc, KPI, Điểm danh, Hồ sơ).\n* **Dashboard:**  Xem tổng quan về công việc, thời gian làm việc, KPI và tiến độ dự án trên dashboard.\n\n\nTóm lại, Humanity OS là một công cụ mạnh mẽ giúp bạn quản lý công việc hiệu quả hơn. Hãy tận dụng các tính năng của hệ thống để theo dõi tiến độ, cải thiện hiệu suất và đóng góp vào thành công của công ty.  Nếu có thắc mắc, hãy sử dụng trợ lý AI hoặc liên hệ với quản lý của bạn.\n','2025-05-22 06:18:04.413316',1),(31,'user','Tình hình các dự án công việc hiện tại như thế nào rồi','2025-05-25 11:39:54.087862',1),(32,'model','Chào ,\n\nTình hình các dự án và công việc hiện tại như sau:\n\n**Tổng quan:**\n\n* Hệ thống đang quản lý 2 dự án, cả hai đều đang hoạt động.  Tuy nhiên, hiệu suất tổng thể đang gây lo ngại. Chỉ có 30% công việc đã hoàn thành, và đáng chú ý là có 4 công việc đang quá hạn.  Tổng thời gian làm việc hôm nay là 0 giờ, cho thấy tỷ lệ điểm danh rất thấp (chỉ 9.1%).  Điều này cần được giải quyết ngay lập tức.\n\n**Vấn đề ưu tiên:**\n\n* **Công việc quá hạn:** Lộc Huỳnh có 3 công việc quá hạn.  Đây là vấn đề nghiêm trọng cần được giải quyết ngay lập tức.  Cần liên hệ với Lộc Huỳnh để hiểu rõ nguyên nhân và hỗ trợ giải quyết.\n* **Vắng mặt không báo trước:** Bob Johnson, Carol Wilson, David Lee, Hoa Nguyễn và Thảo Lê đều không check-in trong 7 ngày qua.  Đây là một vấn đề nghiêm trọng ảnh hưởng đến tiến độ dự án.  Cần liên hệ với từng người để xác minh tình hình và tìm hiểu nguyên nhân vắng mặt.  Nếu không có lý do chính đáng, cần xem xét các biện pháp kỷ luật.\n\n**Phân tích chi tiết:**\n\n* **Hiệu suất nhân sự:** Điểm KPI trung bình là 82.22%, tuy nhiên con số này có thể bị ảnh hưởng bởi việc nhiều nhân viên không check-in.  Cần theo dõi sát sao KPI của từng cá nhân sau khi vấn đề điểm danh được giải quyết.\n* **Phân bổ công việc:** John Doe đang gánh quá nhiều công việc (7 tasks), trong khi có một người chỉ có 1 task.  Cần xem xét lại việc phân bổ công việc để đảm bảo công việc được phân phối đều và hiệu quả hơn.  John Doe cũng làm việc nhiều giờ nhất (35.7 giờ), điều này cần được đánh giá xem có phù hợp với năng suất hay không, hoặc có cần hỗ trợ thêm hay không.\n\n**Đề xuất hành động:**\n\n1. **Khẩn cấp liên hệ:** Liên hệ ngay với Lộc Huỳnh, Bob Johnson, Carol Wilson, David Lee, Hoa Nguyễn và Thảo Lê để tìm hiểu nguyên nhân của các vấn đề nêu trên.\n2. **Xem xét lại quy trình điểm danh:** Cần đánh giá lại quy trình điểm danh để đảm bảo tính chính xác và hiệu quả.  Có thể cần thêm các biện pháp nhắc nhở hoặc hỗ trợ kỹ thuật.\n3. **Cân bằng tải lượng công việc:** Phân bổ lại công việc cho các thành viên trong nhóm để đảm bảo công việc được phân phối đều và hiệu quả hơn.\n4. **Theo dõi sát sao KPI:** Theo dõi sát sao KPI của từng cá nhân để đánh giá hiệu suất và đưa ra các biện pháp hỗ trợ kịp thời.\n5. **Cập nhật thông tin cá nhân:**  Cần cập nhật thông tin phòng ban và ngày tham gia cho tất cả người dùng, bao gồm cả bạn.\n\nTôi sẽ tiếp tục theo dõi tình hình và cung cấp báo cáo cập nhật.  Hãy cho tôi biết nếu bạn cần thêm thông tin hoặc hỗ trợ.\n','2025-05-25 11:39:54.111538',1),(33,'user','trình bày thống kê cho tôi sơ tình hình tuần vừa qua sao rồi','2025-05-25 11:40:56.809933',1),(34,'model','Chào ,\n\nBáo cáo tổng quan tuần vừa qua của hệ thống Humanity OS:\n\n**I. Hiệu suất tổng thể:**\n\n* **Hoàn thành công việc:** Chỉ đạt 30% tổng số công việc (3/10).  Đây là con số rất thấp và đáng báo động, cho thấy hiệu suất tổng thể của nhóm đang gặp vấn đề nghiêm trọng.\n* **Công việc quá hạn:** 4/10 công việc đã quá hạn, chủ yếu tập trung ở Lộc Huỳnh (3 công việc).  Điều này ảnh hưởng trực tiếp đến tiến độ dự án và cần được giải quyết ngay lập tức.\n* **Điểm danh:** Tỷ lệ điểm danh rất thấp, chỉ 9.1% (1/11 người) trong ngày hôm nay.  Điều này gây khó khăn trong việc theo dõi thời gian làm việc và đánh giá hiệu suất chính xác.  Đặc biệt đáng chú ý là 6 thành viên (Bob Johnson, Carol Wilson, David Lee, Hoa Nguyễn, Thảo Lê) vắng mặt không báo trước trong 7 ngày qua.\n* **KPI trung bình:** Mặc dù KPI trung bình đạt 82.22%, con số này có thể bị ảnh hưởng bởi tỷ lệ điểm danh thấp và số lượng công việc quá hạn.  Cần phân tích lại KPI của từng cá nhân sau khi giải quyết các vấn đề về điểm danh và hoàn thành công việc.\n\n**II. Phân tích chi tiết theo từng vấn đề:**\n\n* **Vấn đề Lộc Huỳnh:** 3 công việc quá hạn cần được giải quyết ngay lập tức.  Cần liên hệ trực tiếp với Lộc Huỳnh để tìm hiểu nguyên nhân và hỗ trợ kịp thời.  Có thể cần xem xét lại khả năng của Lộc Huỳnh trong việc đảm nhiệm các công việc được giao.\n* **Vấn đề vắng mặt:** 6 thành viên vắng mặt không báo trước trong 7 ngày qua là vấn đề nghiêm trọng ảnh hưởng đến tiến độ dự án.  Cần liên hệ ngay với từng người để xác minh lý do và đưa ra các biện pháp xử lý phù hợp.  Nếu không có lý do chính đáng, cần xem xét các biện pháp kỷ luật.\n* **Phân bổ công việc:** Sự chênh lệch lớn về số lượng công việc giữa các thành viên (John Doe: 7 tasks,  : 1 task) cho thấy sự bất cân bằng trong phân bổ công việc.  Cần xem xét lại chiến lược phân bổ công việc để đảm bảo công việc được phân phối đều và hiệu quả hơn, tránh tình trạng quá tải cho một số người và thiếu việc cho người khác.  Việc John Doe làm việc 35.7 giờ cũng cần được đánh giá xem có phù hợp với năng suất và sức khỏe hay không.\n\n**III. Đề xuất hành động:**\n\n1. **Khẩn cấp liên hệ:** Liên hệ ngay với Lộc Huỳnh và 6 thành viên vắng mặt để tìm hiểu nguyên nhân và đưa ra giải pháp.\n2. **Xem xét lại quy trình điểm danh:** Cần đánh giá lại quy trình điểm danh để đảm bảo tính chính xác và hiệu quả.  Có thể cần thêm các biện pháp nhắc nhở hoặc hỗ trợ kỹ thuật.\n3. **Cân bằng tải lượng công việc:** Phân bổ lại công việc cho các thành viên trong nhóm để đảm bảo công việc được phân phối đều và hiệu quả hơn.\n4. **Theo dõi sát sao KPI:** Theo dõi sát sao KPI của từng cá nhân để đánh giá hiệu suất và đưa ra các biện pháp hỗ trợ kịp thời.  Cần xem xét lại cách tính KPI để phản ánh chính xác hơn hiệu suất làm việc.\n5. **Cập nhật thông tin cá nhân:** Cần cập nhật thông tin phòng ban và ngày tham gia cho tất cả người dùng, bao gồm cả bạn.\n6. **Thảo luận về hiệu suất:** Tổ chức một cuộc họp để thảo luận về hiệu suất tổng thể của nhóm, xác định nguyên nhân của các vấn đề và đưa ra kế hoạch hành động cụ thể.\n\n\nTôi sẽ tiếp tục theo dõi tình hình và cung cấp báo cáo cập nhật.  Hãy cho tôi biết nếu bạn cần thêm thông tin hoặc hỗ trợ.\n','2025-05-25 11:40:56.819322',1),(35,'user','Thống kê tình hình dự án, công việc tuần vừa qua sao rồi','2025-05-25 11:42:25.427644',9),(36,'model','Chào Lộc Huỳnh! Tuần vừa qua (từ ngày 24/05/2025 đến nay), tình hình công việc và dự án của bạn như sau:\n\n**Điểm danh và Thời gian làm việc:**\n\n* Bạn đã check-in đúng giờ vào ngày 24/05 và làm việc được 7.66 giờ.  Tuy nhiên, ngày 18/05 và 16/05 có điểm danh không hợp lệ, cần kiểm tra và điều chỉnh lại.  Ngày 17/05 bạn chỉ làm việc 0.00 giờ.\n* Tổng thời gian làm việc tuần này là 8 giờ 33 phút, trung bình 4.28 giờ/ngày.  Tỷ lệ hiệu suất thời gian là 53.49%, cần cải thiện.\n\n**Công việc:**\n\n* Bạn đã hoàn thành 1 công việc (\"Thiết kế cơ sở dữ liệu\").\n* Hiện tại bạn đang làm 7 công việc, trong đó có 3 công việc quá hạn (\"Kiểm thử hệ thống\", \"Phát triển module chấm công\", \"Kiểm thử và triển khai\").  Đây là vấn đề cần được giải quyết ngay lập tức.\n* Tỷ lệ hoàn thành công việc là 14.29%, cần cải thiện đáng kể.\n\n**Dự án:**\n\n* **Dự án Quản lý Nhân sự:** Tiến độ 40%, thời gian đã dành 22.08 giờ.  Hai công việc quá hạn (\"Kiểm thử hệ thống\", \"Phát triển module chấm công\") đang ảnh hưởng đến tiến độ dự án.\n* **Dự án Cổng thông tin điện tử:** Tiến độ 20%, thời gian đã dành 4.02 giờ.  Một công việc quá hạn (\"Kiểm thử và triển khai\") đang ảnh hưởng đến tiến độ dự án.\n\n**KPI:**\n\n* KPI tổng thể hiện tại là 83.33%, cần duy trì và cải thiện hơn nữa.  Tuy nhiên, việc có nhiều công việc quá hạn sẽ ảnh hưởng đến KPI trong các tuần tiếp theo.\n\n**Gợi ý cải thiện:**\n\n* **Ưu tiên công việc quá hạn:**  Tập trung hoàn thành 3 công việc quá hạn ngay lập tức.  Sử dụng tính năng quản lý công việc của Humanity OS để lên kế hoạch và theo dõi tiến độ.\n* **Quản lý thời gian hiệu quả:**  Phân tích thời gian làm việc của bạn để xác định nguyên nhân của việc nhiều công việc quá hạn.  Chia nhỏ công việc thành các task nhỏ hơn, dễ quản lý hơn.\n* **Sửa lỗi điểm danh:**  Kiểm tra và điều chỉnh lại các lần check-in/check-out không hợp lệ.\n* **Cập nhật tiến độ thường xuyên:**  Cập nhật trạng thái công việc trên Humanity OS để quản lý và theo dõi hiệu quả hơn.\n\nHãy tận dụng các tính năng của Humanity OS như trợ lý AI để hỗ trợ bạn trong việc quản lý công việc và cải thiện hiệu suất.  Nếu gặp khó khăn, hãy liên hệ với quản lý hoặc đồng nghiệp để được hỗ trợ.\n','2025-05-25 11:42:25.437905',9),(37,'user','Bạn biết các thông tin dự án, thông tin, hiệu suất của các user khác không, cho tôi biết đi','2025-05-25 11:43:13.047065',9),(38,'model','Chào Lộc Huỳnh!  Tôi hiểu bạn muốn biết liệu mình có thể xem thông tin dự án, thông tin cá nhân và hiệu suất của người dùng khác trong Humanity OS hay không.\n\n**Câu trả lời là KHÔNG.**  Với vai trò là `Employee` (Nhân viên), bạn chỉ có quyền truy cập vào thông tin cá nhân, công việc và KPI của **chính mình**.  Bạn không thể xem thông tin của các thành viên khác trong nhóm hay các dự án mà bạn không tham gia.  Đây là để đảm bảo tính bảo mật và riêng tư của dữ liệu người dùng.\n\nNếu bạn cần thông tin về dự án hoặc hiệu suất của người khác, bạn cần liên hệ với quản lý dự án hoặc người có quyền truy cập vào thông tin đó.  Họ sẽ cung cấp cho bạn thông tin cần thiết.\n\nTôi hy vọng điều này giải đáp được thắc mắc của bạn.  Nếu bạn có bất kỳ câu hỏi nào khác, hãy cứ hỏi tôi!\n','2025-05-25 11:43:13.056155',9);
/*!40000 ALTER TABLE `ai_chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Administrators'),(4,'Developers'),(5,'HR'),(2,'Managers'),(3,'Team Leads');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add users',6,'add_users'),(22,'Can change users',6,'change_users'),(23,'Can delete users',6,'delete_users'),(24,'Can view users',6,'view_users'),(25,'Can add check in check out',7,'add_checkincheckout'),(26,'Can change check in check out',7,'change_checkincheckout'),(27,'Can delete check in check out',7,'delete_checkincheckout'),(28,'Can view check in check out',7,'view_checkincheckout'),(29,'Can add team members',8,'add_teammembers'),(30,'Can change team members',8,'change_teammembers'),(31,'Can delete team members',8,'delete_teammembers'),(32,'Can view team members',8,'view_teammembers'),(33,'Can add teams',9,'add_teams'),(34,'Can change teams',9,'change_teams'),(35,'Can delete teams',9,'delete_teams'),(36,'Can view teams',9,'view_teams'),(37,'Can add projects',10,'add_projects'),(38,'Can change projects',10,'change_projects'),(39,'Can delete projects',10,'delete_projects'),(40,'Can view projects',10,'view_projects'),(41,'Can add task assignments',11,'add_taskassignments'),(42,'Can change task assignments',11,'change_taskassignments'),(43,'Can delete task assignments',11,'delete_taskassignments'),(44,'Can view task assignments',11,'view_taskassignments'),(45,'Can add tasks',12,'add_tasks'),(46,'Can change tasks',12,'change_tasks'),(47,'Can delete tasks',12,'delete_tasks'),(48,'Can view tasks',12,'view_tasks'),(49,'Can add time entries',13,'add_timeentries'),(50,'Can change time entries',13,'change_timeentries'),(51,'Can delete time entries',13,'delete_timeentries'),(52,'Can view time entries',13,'view_timeentries'),(53,'Can add form questions',14,'add_formquestions'),(54,'Can change form questions',14,'change_formquestions'),(55,'Can delete form questions',14,'delete_formquestions'),(56,'Can view form questions',14,'view_formquestions'),(57,'Can add form responses',15,'add_formresponses'),(58,'Can change form responses',15,'change_formresponses'),(59,'Can delete form responses',15,'delete_formresponses'),(60,'Can view form responses',15,'view_formresponses'),(61,'Can add forms',16,'add_forms'),(62,'Can change forms',16,'change_forms'),(63,'Can delete forms',16,'delete_forms'),(64,'Can view forms',16,'view_forms'),(65,'Can add employee kp is',17,'add_employeekpis'),(66,'Can change employee kp is',17,'change_employeekpis'),(67,'Can delete employee kp is',17,'delete_employeekpis'),(68,'Can view employee kp is',17,'view_employeekpis'),(69,'Can add kp is',18,'add_kpis'),(70,'Can change kp is',18,'change_kpis'),(71,'Can delete kp is',18,'delete_kpis'),(72,'Can view kp is',18,'view_kpis'),(73,'Can add team project membership',19,'add_teamprojectmembership'),(74,'Can change team project membership',19,'change_teamprojectmembership'),(75,'Can delete team project membership',19,'delete_teamprojectmembership'),(76,'Can view team project membership',19,'view_teamprojectmembership'),(77,'Can add goals',20,'add_goals'),(78,'Can change goals',20,'change_goals'),(79,'Can delete goals',20,'delete_goals'),(80,'Can view goals',20,'view_goals'),(81,'Can add deadline extension request',21,'add_deadlineextensionrequest'),(82,'Can change deadline extension request',21,'change_deadlineextensionrequest'),(83,'Can delete deadline extension request',21,'delete_deadlineextensionrequest'),(84,'Can view deadline extension request',21,'view_deadlineextensionrequest'),(85,'Can add user face image',22,'add_userfaceimage'),(86,'Can change user face image',22,'change_userfaceimage'),(87,'Can delete user face image',22,'delete_userfaceimage'),(88,'Can view user face image',22,'view_userfaceimage'),(89,'Can add ai chat message',23,'add_aichatmessage'),(90,'Can change ai chat message',23,'change_aichatmessage'),(91,'Can delete ai chat message',23,'delete_aichatmessage'),(92,'Can view ai chat message',23,'view_aichatmessage'),(93,'Can add Time Entry',24,'add_timeentriesnew'),(94,'Can change Time Entry',24,'change_timeentriesnew'),(95,'Can delete Time Entry',24,'delete_timeentriesnew'),(96,'Can view Time Entry',24,'view_timeentriesnew');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checkin_checkout`
--

DROP TABLE IF EXISTS `checkin_checkout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `checkin_checkout` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `checkin_time` datetime(6) DEFAULT NULL,
  `checkout_time` datetime(6) DEFAULT NULL,
  `checkin_image` varchar(100) DEFAULT NULL,
  `checkout_image` varchar(100) DEFAULT NULL,
  `date` date NOT NULL,
  `user_id` bigint NOT NULL,
  `checkin_location` varchar(100) DEFAULT NULL,
  `checkout_location` varchar(100) DEFAULT NULL,
  `is_valid_checkin` tinyint(1) NOT NULL,
  `is_valid_checkout` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `checkin_che_date_4a512a_idx` (`date`),
  KEY `checkin_che_user_id_677476_idx` (`user_id`,`date`),
  KEY `checkin_checkout_user_id_ada68373` (`user_id`),
  CONSTRAINT `checkin_checkout_user_id_ada68373_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checkin_checkout`
--

LOCK TABLES `checkin_checkout` WRITE;
/*!40000 ALTER TABLE `checkin_checkout` DISABLE KEYS */;
INSERT INTO `checkin_checkout` VALUES (59,'2025-05-13 07:56:19.000000','2025-05-13 18:56:40.000000','checkin_images/checkin_lochuynh2_2025-05-13_1747104979.jpg','checkout_images/checkout_lochuynh2_2025-05-13_1747105000.jpg','2025-05-13',9,'16.0514567,108.2244186','16.0514567,108.2244186',1,1),(60,'2025-05-12 06:00:00.000000','2025-05-12 18:00:00.000000','checkin_images/Photo_from_2025-05-06_22-42-31.579917.jpeg','checkout_images/Photo_from_2025-05-06_22-42-27.066309.jpeg','2025-05-12',9,'16.0610909,108.172527','16.0610909,108.172527',1,1),(61,'2025-05-11 06:00:00.000000','2025-05-11 18:00:00.000000','checkin_images/Photo_from_2025-05-11_14-46-52.319794.jpeg','checkout_images/checkin_lochuynh2_2025-05-13_1747102526.jpg','2025-05-11',9,'16.0765337,108.1608241','16.0765337,108.1608241',1,1),(62,'2025-05-10 06:00:00.000000','2025-05-13 18:00:00.000000','checkin_images/Photo_from_2025-05-11_14-46-56_zqnpXyL.381557.jpeg','checkout_images/checkin_lochuynh2_2025-05-13_1747099642.jpg','2025-05-10',9,'16.0770582,108.1369375','16.0770582,108.1369375',1,1),(63,'2025-05-15 17:29:41.540816',NULL,'checkin_images/checkin_lochuynh2_2025-05-15_1747330181.jpg','','2025-05-15',9,'16.0765556,108.1608085',NULL,0,0),(64,'2025-05-16 00:22:18.081273',NULL,'checkin_images/checkin_lochuynh2_2025-05-16_1747354938.jpg','','2025-05-16',9,'16.0747391,108.15316',NULL,0,0),(68,'2025-05-17 08:56:36.182247','2025-05-17 08:56:45.974038','checkin_images/checkin_lochuynh2_2025-05-17_1747472196.jpg','checkout_images/checkout_lochuynh2_2025-05-17_1747472205.jpg','2025-05-17',9,'15.9481856,108.1376768','15.9481856,108.1376768',1,1),(69,'2025-05-18 08:10:14.861496','2025-05-18 10:36:13.952722','checkin_images/checkin_lochuynh2_2025-05-18_1747555814.jpg','checkout_images/checkout_lochuynh2_2025-05-18_1747564573.jpg','2025-05-18',9,'16.0765926,108.1608047','16.0765711,108.160805',0,0),(71,'2025-05-24 10:07:03.757404','2025-05-24 17:46:23.353200','checkin_images/checkin_lochuynh2_2025-05-24_1748081223.jpg','checkout_images/checkout_lochuynh2_2025-05-24_1748108783.jpg','2025-05-24',9,'16.4591117,107.607571','16.0765973,108.160787',1,0),(72,'2025-05-25 10:48:07.000000',NULL,'checkin_images/checkin_lochuynh2_2025-05-25_1748170087.jpg','checkout_images/checkin_lochuynh2_2025-05-24_1748081223.jpg','2025-05-25',9,'16.0765893,108.1608068','16.0765893,108.1608068',1,1);
/*!40000 ALTER TABLE `checkin_checkout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deadline_extension_requests`
--

DROP TABLE IF EXISTS `deadline_extension_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deadline_extension_requests` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `requested_deadline` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `reason` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `requested_by_id` bigint NOT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `deadline_extension_requests_requested_by_id_28feab40_fk_users_id` (`requested_by_id`),
  KEY `deadline_extension_requests_task_id_ecbd46d3_fk_tasks_id` (`task_id`),
  KEY `deadline_extension_requests_task_status_idx` (`task_id`,`status`),
  KEY `deadline_extension_requests_user_status_idx` (`requested_by_id`,`status`),
  CONSTRAINT `deadline_extension_requests_requested_by_id_28feab40_fk_users_id` FOREIGN KEY (`requested_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `deadline_extension_requests_task_id_ecbd46d3_fk_tasks_id` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deadline_extension_requests`
--

LOCK TABLES `deadline_extension_requests` WRITE;
/*!40000 ALTER TABLE `deadline_extension_requests` DISABLE KEYS */;
INSERT INTO `deadline_extension_requests` VALUES (1,'2024-06-30 17:00:00.000000','Approved','Cần thêm thời gian để hoàn thiện các tính năng phức tạp','2024-06-01 10:30:00.000000',3,3),(2,'2024-06-30 17:00:00.000000','Approved','Gặp khó khăn trong việc tích hợp với hệ thống bên thứ ba','2024-06-05 14:15:00.000000',4,7),(6,'2025-05-20 00:00:00.000000','Approved','New requirement','2025-05-18 09:42:06.853690',9,4);
/*!40000 ALTER TABLE `deadline_extension_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-04-03 17:04:23.565456','9','lochuynh2',1,'[{\"added\": {}}]',6,1),(2,'2025-04-03 17:04:30.523598','9','lochuynh2',2,'[]',6,1),(3,'2025-04-03 17:08:03.329419','6','Employee Survey - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(4,'2025-04-03 17:08:10.418172','5','API Rate Limiting - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(5,'2025-04-03 17:08:14.788730','4','Mobile Navigation - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(6,'2025-04-03 17:08:18.992385','3','Profile Page UI - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(7,'2025-04-03 17:08:35.847684','6','lochuynh2 - API Rate Limiting (2024-04-03 13:00:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(8,'2025-04-03 17:08:41.508856','4','lochuynh2 - Implement Auth API (2024-04-02 14:00:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(9,'2025-04-03 17:08:58.757340','2','lochuynh2 - Design Login Page (2024-04-01 13:30:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(10,'2025-04-03 17:09:04.219206','1','lochuynh2 - Design Login Page (2024-04-01 09:00:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(11,'2025-04-03 17:09:35.548623','7','Frontend Team - lochuynh2',1,'[{\"added\": {}}]',8,1),(12,'2025-04-03 17:09:41.446815','4','Backend Team - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',8,1),(13,'2025-04-03 17:10:14.874719','6','lochuynh2 -> asmith (Employee Satisfaction)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',15,1),(14,'2025-04-03 17:10:19.340035','4','bjohnson -> lochuynh2 (Peer Feedback)',2,'[{\"changed\": {\"fields\": [\"Target user\"]}}]',15,1),(15,'2025-04-03 17:10:27.799472','1','lochuynh2 -> lochuynh (Performance Review)',2,'[{\"changed\": {\"fields\": [\"User\", \"Target user\"]}}]',15,1),(16,'2025-04-03 17:14:01.106418','9','lochuynh2 - Employee Satisfaction (Annual)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',17,1),(17,'2025-04-03 17:14:05.306597','7','lochuynh2 - Code Quality (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',17,1),(18,'2025-04-03 17:14:11.202604','5','lochuynh2 - Task Completion (Quarterly)',2,'[{\"changed\": {\"fields\": [\"User\", \"Evaluation\"]}}]',17,1),(19,'2025-04-03 17:14:15.428983','2','lochuynh2 - Task Completion (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\", \"Evaluation\"]}}]',17,1),(20,'2025-04-03 17:14:20.390616','1','lochuynh2 - Code Quality (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\", \"Evaluation\"]}}]',17,1),(21,'2025-04-14 17:12:51.558591','9','lochuynh2 - 2025-04-14',3,'',7,1),(22,'2025-04-15 17:11:20.161237','8','lochuynh2 - Task Completion (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',17,1),(23,'2025-04-15 17:11:33.936359','5','lochuynh2 -> cwilson (Peer Feedback)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',15,1),(24,'2025-04-15 17:11:50.207150','6','Employee Survey - lochuynh2',2,'[]',11,1),(25,'2025-05-04 13:28:10.867396','8','lochuynh2 - Task Completion (Monthly)',3,'',17,1),(26,'2025-05-04 13:28:25.461512','7','lochuynh2 - Code Quality (Monthly)',3,'',17,1),(27,'2025-05-04 13:28:38.048806','5','lochuynh2 - Task Completion (Quarterly)',3,'',17,1),(28,'2025-05-04 13:28:50.644671','1','lochuynh2 - Code Quality (Monthly)',3,'',17,1),(29,'2025-05-04 13:29:31.399803','2','lochuynh2 - Task Completion (Monthly)',3,'',17,1),(30,'2025-05-06 16:25:45.609018','10','Face image for lochuynh2',3,'',22,1),(31,'2025-05-06 16:25:45.609045','9','Face image for lochuynh2',3,'',22,1),(32,'2025-05-06 16:25:45.609058','8','Face image for lochuynh2',3,'',22,1),(33,'2025-05-06 16:25:45.609067','7','Face image for lochuynh2',3,'',22,1),(34,'2025-05-06 16:25:45.609075','6','Face image for admin',3,'',22,1),(35,'2025-05-06 16:25:45.609084','5','Face image for admin',3,'',22,1),(36,'2025-05-06 16:25:45.609093','4','Face image for admin',3,'',22,1),(37,'2025-05-06 16:25:45.609100','3','Face image for admin',3,'',22,1),(38,'2025-05-06 16:26:13.416697','30','lochuynh2 - 2025-05-06',3,'',7,1),(39,'2025-05-06 16:26:13.416747','29','lochuynh2 - 2025-05-06',3,'',7,1),(40,'2025-05-06 16:26:13.416781','28','lochuynh2 - 2025-05-06',3,'',7,1),(41,'2025-05-06 16:26:13.416801','27','lochuynh2 - 2025-05-06',3,'',7,1),(42,'2025-05-06 16:26:13.416824','26','lochuynh2 - 2025-05-05',3,'',7,1),(43,'2025-05-06 16:26:13.416843','25','lochuynh2 - 2025-05-04',3,'',7,1),(44,'2025-05-06 16:26:13.416864','24','lochuynh2 - 2025-04-27',3,'',7,1),(45,'2025-05-06 16:26:13.416881','23','lochuynh2 - 2025-04-24',3,'',7,1),(46,'2025-05-06 16:26:13.416897','22','lochuynh2 - 2025-04-21',3,'',7,1),(47,'2025-05-06 16:26:13.416913','21','lochuynh2 - 2025-04-17',3,'',7,1),(48,'2025-05-06 16:26:13.416930','20','asmith - 2025-04-15',3,'',7,1),(49,'2025-05-06 16:26:13.416946','19','jdoe - 2025-04-16',3,'',7,1),(50,'2025-05-06 16:26:13.416964','18','lethithao - 2025-04-16',3,'',7,1),(51,'2025-05-06 16:26:13.416980','17','nguyenhoa - 2025-04-16',3,'',7,1),(52,'2025-05-06 16:26:13.416995','16','lochuynh2 - 2025-04-13',3,'',7,1),(53,'2025-05-06 16:26:13.417010','15','lochuynh2 - 2025-04-14',3,'',7,1),(54,'2025-05-06 16:26:13.417025','14','lochuynh2 - 2025-04-15',3,'',7,1),(55,'2025-05-06 16:26:13.417041','13','lochuynh2 - 2025-04-16',3,'',7,1),(56,'2025-05-06 16:26:13.417056','12','lochuynh2 - 2025-04-16',3,'',7,1),(57,'2025-05-06 16:26:13.417070','11','lochuynh2 - 2025-04-15',3,'',7,1),(58,'2025-05-06 16:26:13.417085','10','lochuynh2 - 2025-04-14',3,'',7,1),(59,'2025-05-06 16:26:13.417103','8','lochuynh2 - 2025-04-13',3,'',7,1),(60,'2025-05-06 16:26:13.417118','7','lochuynh2 - 2025-04-13',3,'',7,1),(61,'2025-05-06 16:26:13.417142','6','cwilson - 2024-04-03',3,'',7,1),(62,'2025-05-06 16:26:13.417158','5','asmith - 2024-04-03',3,'',7,1),(63,'2025-05-06 16:26:13.417174','4','cwilson - 2024-04-02',3,'',7,1),(64,'2025-05-06 16:26:13.417192','3','asmith - 2024-04-02',3,'',7,1),(65,'2025-05-06 16:26:13.417208','2','cwilson - 2024-04-01',3,'',7,1),(66,'2025-05-06 16:26:13.417223','1','asmith - 2024-04-01',3,'',7,1),(67,'2025-05-06 16:43:56.908268','36','lochuynh2 - 2025-05-06',3,'',7,1),(68,'2025-05-06 16:43:56.908315','35','lochuynh2 - 2025-05-06',3,'',7,1),(69,'2025-05-06 16:43:56.908340','34','lochuynh2 - 2025-05-06',3,'',7,1),(70,'2025-05-06 16:43:56.908363','33','lochuynh2 - 2025-05-06',3,'',7,1),(71,'2025-05-06 16:43:56.908384','32','lochuynh2 - 2025-05-06',3,'',7,1),(72,'2025-05-06 17:16:53.764867','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(73,'2025-05-06 17:17:15.938011','38','lochuynh2 - 2025-05-06',3,'',7,1),(74,'2025-05-06 17:17:15.938058','37','lochuynh2 - 2025-05-06',3,'',7,1),(75,'2025-05-11 07:31:04.284918','42','lochuynh2 - 2025-05-11',3,'',7,1),(76,'2025-05-11 07:31:04.284993','41','lochuynh2 - 2025-05-11',3,'',7,1),(77,'2025-05-11 07:31:04.285027','40','lochuynh2 - 2025-05-06',3,'',7,1),(78,'2025-05-11 07:31:04.285056','39','lochuynh2 - 2025-05-06',3,'',7,1),(79,'2025-05-11 07:44:17.404574','44','lochuynh2 - 2025-05-11',3,'',7,1),(80,'2025-05-11 07:44:17.404607','43','lochuynh2 - 2025-05-11',3,'',7,1),(81,'2025-05-11 07:46:24.733642','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(82,'2025-05-11 07:47:05.802806','46','lochuynh2 - 2025-05-11',3,'',7,1),(83,'2025-05-11 07:47:21.708680','14','Face image for lochuynh2',3,'',22,1),(84,'2025-05-11 07:47:21.708704','13','Face image for lochuynh2',3,'',22,1),(85,'2025-05-11 07:47:21.708714','12','Face image for lochuynh2',3,'',22,1),(86,'2025-05-11 07:47:21.708722','11','Face image for lochuynh2',3,'',22,1),(87,'2025-05-11 07:48:39.149320','47','lochuynh2 - 2025-05-11',3,'',7,1),(88,'2025-05-12 15:05:45.534563','51','lochuynh2 - 2025-05-12',3,'',7,1),(89,'2025-05-12 15:05:45.534609','50','lochuynh2 - 2025-05-11',3,'',7,1),(90,'2025-05-13 02:06:24.433384','54','lochuynh2 - 2025-05-13',3,'',7,1),(91,'2025-05-13 02:06:24.433472','53','lochuynh2 - 2025-05-13',3,'',7,1),(92,'2025-05-13 02:06:24.433503','52','lochuynh2 - 2025-05-12',3,'',7,1),(93,'2025-05-13 02:15:15.936160','56','lochuynh2 - 2025-05-13',3,'',7,1),(94,'2025-05-13 02:15:15.936205','55','lochuynh2 - 2025-05-13',3,'',7,1),(95,'2025-05-13 02:52:07.883256','57','lochuynh2 - 2025-05-13',3,'',7,1),(96,'2025-05-13 02:52:32.949612','17','Face image for lochuynh2',3,'',22,1),(97,'2025-05-13 02:52:32.949642','16','Face image for lochuynh2',3,'',22,1),(98,'2025-05-13 02:52:32.949655','15','Face image for lochuynh2',3,'',22,1),(99,'2025-05-13 02:55:07.205545','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(100,'2025-05-13 02:55:25.513991','58','lochuynh2 - 2025-05-13',3,'',7,1),(101,'2025-05-13 02:55:56.699558','19','Face image for lochuynh2',3,'',22,1),(102,'2025-05-13 03:23:06.763288','59','lochuynh2 - 2025-05-13',2,'[{\"changed\": {\"fields\": [\"Checkin time\", \"Checkout time\"]}}]',7,1),(103,'2025-05-13 03:25:04.460571','60','lochuynh2 - 2025-05-12',1,'[{\"added\": {}}]',7,1),(104,'2025-05-13 03:25:24.876855','60','lochuynh2 - 2025-05-12',2,'[{\"changed\": {\"fields\": [\"Checkin image\", \"Checkout image\"]}}]',7,1),(105,'2025-05-13 03:26:35.758691','61','lochuynh2 - 2025-05-11',1,'[{\"added\": {}}]',7,1),(106,'2025-05-13 03:27:34.243682','62','lochuynh2 - 2025-05-10',1,'[{\"added\": {}}]',7,1),(107,'2025-05-16 00:32:47.993084','31','Tích hợp email marketing - lochuynh2',2,'[]',11,1),(108,'2025-05-16 00:34:07.058104','26','Tassk 2',1,'[{\"added\": {}}]',12,1),(109,'2025-05-17 08:43:38.041768','29','Face image for lochuynh2',1,'[{\"added\": {}}]',22,1),(110,'2025-05-17 08:45:14.996840','20','Face image for lochuynh2',3,'',22,1),(111,'2025-05-17 08:47:45.931416','30','Face image for lochuynh2',1,'[{\"added\": {}}]',22,1),(112,'2025-05-17 08:48:04.451651','65','lochuynh2 - 2025-05-17',3,'',7,1),(113,'2025-05-17 08:50:23.839569','31','Face image for lochuynh2',1,'[{\"added\": {}}]',22,1),(114,'2025-05-17 08:54:44.670515','32','Face image for lochuynh2',1,'[{\"added\": {}}]',22,1),(115,'2025-05-17 08:54:52.237586','66','lochuynh2 - 2025-05-17',3,'',7,1),(116,'2025-05-17 08:55:30.131596','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(117,'2025-05-17 08:56:19.813122','67','lochuynh2 - 2025-05-17',3,'',7,1),(118,'2025-05-17 11:54:11.074859','32','Thiết kế cơ sở dữ liệu - lochuynh2 (Thực hiện chính)',1,'[{\"added\": {}}]',11,1),(119,'2025-05-17 11:54:25.439867','33','Phát triển module quản lý nhân viên - lochuynh2 (Thực hiện chính)',1,'[{\"added\": {}}]',11,1),(120,'2025-05-17 11:54:35.817885','34','Phát triển module chấm công - lochuynh2 (Thực hiện chính)',1,'[{\"added\": {}}]',11,1),(121,'2025-05-17 11:54:47.310049','35','Kiểm thử hệ thống - lochuynh2 (Test)',1,'[{\"added\": {}}]',11,1),(122,'2025-05-17 11:55:00.575872','36','Phát triển module tin tức - lochuynh2 (Đồng thực hiện)',1,'[{\"added\": {}}]',11,1),(123,'2025-05-17 11:55:15.597754','37','Kiểm thử và triển khai - lochuynh2 (Review)',1,'[{\"added\": {}}]',11,1),(124,'2025-05-17 11:55:30.099969','38','Phát triển module tài liệu - lochuynh2 (Thực hiện chính)',1,'[{\"added\": {}}]',11,1),(125,'2025-05-17 11:56:17.502456','64','lochuynh2 - Thiết kế cơ sở dữ liệu (2025-05-10 18:56:02+00:00)',1,'[{\"added\": {}}]',13,1),(126,'2025-05-17 11:56:41.962341','65','lochuynh2 - Phát triển module quản lý nhân viên (2025-05-12 18:56:29+00:00)',1,'[{\"added\": {}}]',13,1),(127,'2025-05-17 11:57:08.634559','66','lochuynh2 - Phát triển module tin tức (2025-05-14 18:56:54+00:00)',1,'[{\"added\": {}}]',13,1),(128,'2025-05-17 14:57:09.740009','2','Dự án Cổng thông tin điện tử',2,'[{\"changed\": {\"fields\": [\"End date\"]}}]',10,1),(129,'2025-05-17 14:57:22.872713','1','Dự án Quản lý Nhân sự',2,'[{\"changed\": {\"fields\": [\"End date\"]}}]',10,1),(130,'2025-05-21 17:39:54.541610','2','Request for Thiết kế giao diện by asmith',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',21,1),(131,'2025-05-23 09:21:22.833720','32','Face image for lochuynh2',3,'',22,1),(132,'2025-05-23 09:21:54.862396','31','Face image for lochuynh2',3,'',22,1),(133,'2025-05-23 09:52:44.983635','6','Request for Phát triển module chấm công by lochuynh2',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',21,1),(134,'2025-05-23 09:52:50.101223','6','Request for Phát triển module chấm công by lochuynh2',2,'[]',21,1),(135,'2025-05-23 10:11:47.646113','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',6,1),(136,'2025-05-24 10:06:17.336835','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(137,'2025-05-24 10:06:49.336625','70','lochuynh2 - 2025-05-24',3,'',7,1),(138,'2025-05-24 17:50:18.555631','10','Kiểm thử và triển khai',2,'[{\"changed\": {\"fields\": [\"Github link\"]}}]',12,1),(139,'2025-05-25 09:10:59.117798','2','admin',2,'[]',6,1),(140,'2025-05-25 10:47:15.820405','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(141,'2025-05-25 10:57:07.797099','9','Ý kiến đóng góp cho đồng nghiệp?',2,'[{\"changed\": {\"fields\": [\"Max score\"]}}]',14,1),(142,'2025-05-25 10:57:10.433276','9','Ý kiến đóng góp cho đồng nghiệp?',2,'[]',14,1),(143,'2025-06-02 08:37:27.555972','2','admin',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(144,'2025-06-02 08:43:01.955902','2','admin',2,'[{\"changed\": {\"fields\": [\"Avatar\", \"Phone\"]}}]',6,1),(145,'2025-06-02 08:45:06.983631','4','Loilevan',2,'[{\"changed\": {\"fields\": [\"Username\", \"Email address\", \"Avatar\", \"Phone\", \"Department\", \"Fixed location\"]}}]',6,1),(146,'2025-06-02 08:46:22.399020','5','Sontranvan',2,'[{\"changed\": {\"fields\": [\"Username\", \"Email address\", \"Avatar\", \"Phone\", \"Department\", \"Fixed location\", \"Staff status\"]}}]',6,1),(147,'2025-06-02 08:48:07.665749','6','Maithithao',2,'[{\"changed\": {\"fields\": [\"Username\", \"Email address\", \"Avatar\", \"Phone\", \"Department\", \"Fixed location\", \"Staff status\"]}}]',6,1),(148,'2025-06-02 08:48:44.115717','11','lethithao',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(149,'2025-06-02 08:49:09.589525','10','nguyenhoa',2,'[{\"changed\": {\"fields\": [\"Avatar\", \"Fixed location\", \"Staff status\"]}}]',6,1),(150,'2025-06-02 08:49:27.787755','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Department\", \"Staff status\"]}}]',6,1),(151,'2025-06-02 08:49:41.215751','11','lethithao',2,'[{\"changed\": {\"fields\": [\"Avatar\", \"Staff status\"]}}]',6,1),(152,'2025-06-02 08:50:15.169892','7','TranVanThai',2,'[{\"changed\": {\"fields\": [\"Username\", \"Email address\", \"Avatar\", \"Phone\", \"Department\", \"Fixed location\", \"Staff status\"]}}]',6,1),(153,'2025-06-02 08:51:11.536702','8','NguyenThiThanh',2,'[{\"changed\": {\"fields\": [\"Username\", \"Email address\", \"Avatar\", \"Phone\", \"Fixed location\"]}}]',6,1),(154,'2025-06-02 08:52:08.588372','3','PhanTanPhat',2,'[{\"changed\": {\"fields\": [\"Username\", \"Email address\", \"Avatar\", \"Phone\", \"Department\", \"Fixed location\"]}}]',6,1),(155,'2025-06-02 08:52:51.026932','1','lochuynh',2,'[{\"changed\": {\"fields\": [\"Avatar\", \"Phone\", \"Department\", \"Fixed location\"]}}]',6,1),(156,'2025-06-02 08:53:07.153210','10','nguyenhoa',2,'[{\"changed\": {\"fields\": [\"Department\"]}}]',6,1),(157,'2025-06-02 08:53:34.847177','8','NguyenThiThanh',2,'[{\"changed\": {\"fields\": [\"Department\"]}}]',6,1),(158,'2025-06-02 08:54:04.768264','2','admin',2,'[{\"changed\": {\"fields\": [\"Department\"]}}]',6,1),(159,'2025-06-02 08:54:12.720234','1','lochuynh',2,'[{\"changed\": {\"fields\": [\"Department\"]}}]',6,1),(160,'2025-06-02 08:56:37.330553','33','Face image for PhanTanPhat',1,'[{\"added\": {}}]',22,1),(161,'2025-06-02 08:56:45.533296','34','Face image for PhanTanPhat',1,'[{\"added\": {}}]',22,1),(162,'2025-06-02 08:56:58.128889','35','Face image for PhanTanPhat',1,'[{\"added\": {}}]',22,1),(163,'2025-06-02 08:57:06.115071','36','Face image for PhanTanPhat',1,'[{\"added\": {}}]',22,1),(164,'2025-06-02 08:57:14.905524','37','Face image for PhanTanPhat',1,'[{\"added\": {}}]',22,1),(165,'2025-06-02 08:57:26.532715','38','Face image for PhanTanPhat',1,'[{\"added\": {}}]',22,1),(166,'2025-06-02 08:59:19.459693','39','Face image for Maithithao',1,'[{\"added\": {}}]',22,1),(167,'2025-06-02 08:59:26.799274','40','Face image for Maithithao',1,'[{\"added\": {}}]',22,1),(168,'2025-06-02 08:59:34.353978','41','Face image for Maithithao',1,'[{\"added\": {}}]',22,1),(169,'2025-06-02 09:00:03.602629','41','Face image for Maithithao',2,'[{\"changed\": {\"fields\": [\"Face image\"]}}]',22,1),(170,'2025-06-02 09:00:09.490287','40','Face image for Maithithao',2,'[]',22,1),(171,'2025-06-02 09:00:16.739467','39','Face image for Maithithao',2,'[{\"changed\": {\"fields\": [\"Face image\"]}}]',22,1),(172,'2025-06-02 09:01:00.622165','34','Face image for PhanTanPhat',3,'',22,1),(173,'2025-06-02 09:12:52.968272','72','lochuynh2 - 2025-05-25',2,'[{\"changed\": {\"fields\": [\"Checkout location\", \"Is valid checkout\"]}}]',7,1),(174,'2025-06-02 09:13:35.965836','72','lochuynh2 - 2025-05-25',2,'[{\"changed\": {\"fields\": [\"Checkout image\"]}}]',7,1),(175,'2025-06-02 09:14:40.286354','6','Peer review tháng 6',1,'[{\"added\": {}}]',16,1),(176,'2025-06-02 09:15:01.096454','9','Ý kiến đóng góp cho đồng nghiệp?',2,'[]',14,1),(177,'2025-06-02 09:15:05.777467','8','Bạn đánh giá thế nào về tinh thần hợp tác của đồng',2,'[]',14,1),(178,'2025-06-02 09:15:13.345982','6','Gợi ý cải thiện teamwork?',2,'[]',14,1),(179,'2025-06-02 09:15:18.203458','5','Mức độ hỗ trợ từ team?',2,'[]',14,1),(180,'2025-06-02 09:15:58.929607','3','Feedback tháng 5',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',16,1),(181,'2025-06-02 09:16:35.406097','1','Peer Feedback tháng 6',2,'[{\"changed\": {\"fields\": [\"Name\", \"Deadline\"]}}]',16,1),(182,'2025-06-02 09:16:43.519820','1','Feedback tháng 6',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',16,1),(183,'2025-06-02 09:17:59.330125','3','Hiệu suất làm việc của nhân viên?',2,'[]',14,1),(184,'2025-06-02 09:18:05.033826','4','Khu vực cần cải thiện?',2,'[]',14,1),(185,'2025-06-02 09:19:19.789811','4','Các khuyến điểm mà nhân viên cần cải thiện?',2,'[{\"changed\": {\"fields\": [\"Question text\"]}}]',14,1),(186,'2025-06-02 09:19:58.826540','10','Ưu điểm của nhân viên cần được phát huy',1,'[{\"added\": {}}]',14,1),(187,'2025-06-02 09:20:29.435338','11','Dánh giá tổng thế kết quả của nhân viên trong quý ',1,'[{\"added\": {}}]',14,1),(188,'2025-06-02 09:20:37.506340','11','Đánh giá tổng thế kết quả của nhân viên trong quý ',2,'[{\"changed\": {\"fields\": [\"Question text\"]}}]',14,1),(189,'2025-06-02 09:21:53.516685','12','Mức độ hài lòng của các thành viên khác trong team',1,'[{\"added\": {}}]',14,1),(190,'2025-06-02 09:22:02.955949','11','Đánh giá tổng thế kết quả của nhân viên trong quý ',2,'[{\"changed\": {\"fields\": [\"Max score\"]}}]',14,1),(191,'2025-06-02 09:22:09.458408','10','Ưu điểm của nhân viên cần được phát huy',2,'[{\"changed\": {\"fields\": [\"Max score\"]}}]',14,1),(192,'2025-06-02 09:22:53.855894','13','Đánh giá mức độ phát huy của nhân viên so với quý ',1,'[{\"added\": {}}]',14,1),(193,'2025-06-02 09:23:08.602499','13','Đánh giá mức độ phát huy của nhân viên so với quý ',2,'[{\"changed\": {\"fields\": [\"Question type\"]}}]',14,1),(194,'2025-06-02 09:23:21.124775','9','Ý kiến đóng góp cho đồng nghiệp?',2,'[{\"changed\": {\"fields\": [\"Max score\"]}}]',14,1),(195,'2025-06-02 09:23:35.525524','8','Bạn đánh giá thế nào về tinh thần hợp tác của đồng',2,'[]',14,1),(196,'2025-06-02 09:24:07.861753','6','Ý kiến đóng góp cho đồng nghiệp',2,'[{\"changed\": {\"fields\": [\"Question text\"]}}]',14,1),(197,'2025-06-02 09:24:15.917764','9','Ý kiến đóng góp cho đồng nghiệp',2,'[{\"changed\": {\"fields\": [\"Question text\"]}}]',14,1),(198,'2025-06-02 09:24:44.932525','5','Bạn đánh giá thế nào về mức độ hợp tác của động ng',2,'[{\"changed\": {\"fields\": [\"Question text\", \"Max score\"]}}]',14,1),(199,'2025-06-02 09:24:54.614355','8','Bạn đánh giá thế nào về tinh thần hợp tác của đồng',2,'[{\"changed\": {\"fields\": [\"Max score\"]}}]',14,1),(200,'2025-06-02 09:25:11.851676','3','Hiệu suất làm việc của nhân viên?',2,'[{\"changed\": {\"fields\": [\"Max score\"]}}]',14,1),(201,'2025-06-02 09:25:31.045814','2','Điểm mạnh của đồng nghiệp là gì?',2,'[{\"changed\": {\"fields\": [\"Form\"]}}]',14,1),(202,'2025-06-02 09:25:45.579638','1','Đánh giá khả năng hợp tác của đồng nghiệp',2,'[{\"changed\": {\"fields\": [\"Form\", \"Max score\"]}}]',14,1),(203,'2025-06-02 09:26:03.902426','14','Điểm mạnh của đồng nghiệp là gì',1,'[{\"added\": {}}]',14,1),(204,'2025-06-02 09:26:26.702417','15','Đánh giá mức độ hài lòng về đồng nghiệp',1,'[{\"added\": {}}]',14,1),(205,'2025-06-02 09:29:03.529542','8','Phản hồi từ đồng nghiệp',2,'[{\"changed\": {\"fields\": [\"Name\", \"Description\", \"Kpi type\", \"Unit\"]}}]',18,1),(206,'2025-06-02 09:30:33.150684','7','Thời gian giao tiếp',2,'[{\"changed\": {\"fields\": [\"Name\", \"Description\", \"Kpi type\", \"Unit\", \"Weight\"]}}]',18,1),(207,'2025-06-02 09:30:44.616565','6','API Response Time',3,'',18,1),(208,'2025-06-02 09:30:44.616603','5','Feature Delivery',3,'',18,1),(209,'2025-06-02 09:30:44.616625','4','Employee Satisfaction',3,'',18,1),(210,'2025-06-02 09:30:44.616644','3','Bug Rate',3,'',18,1),(211,'2025-06-02 09:30:44.616663','2','Task Completion',3,'',18,1),(212,'2025-06-02 09:30:44.616680','1','Code Quality',3,'',18,1),(213,'2025-06-02 09:32:51.645577','14','Số lỗi mắc phải',1,'[{\"added\": {}}]',18,1),(214,'2025-06-02 09:33:14.869012','2','Dự án Cổng thông tin điện tử',2,'[{\"changed\": {\"fields\": [\"Manager\"]}}]',10,1),(215,'2025-06-02 09:57:24.632655','2','Dự án Cổng thông tin điện tử',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',10,1),(216,'2025-06-02 10:15:43.666454','1','Dự án Quản lý Nhân sự',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',10,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(8,'companies','teammembers'),(9,'companies','teams'),(4,'contenttypes','contenttype'),(14,'evaluations','formquestions'),(15,'evaluations','formresponses'),(16,'evaluations','forms'),(17,'kpis','employeekpis'),(18,'kpis','kpis'),(21,'projects','deadlineextensionrequest'),(10,'projects','projects'),(11,'projects','taskassignments'),(12,'projects','tasks'),(19,'projects','teamprojectmembership'),(13,'projects','timeentries'),(24,'projects','timeentriesnew'),(5,'sessions','session'),(23,'users','aichatmessage'),(7,'users','checkincheckout'),(20,'users','goals'),(22,'users','userfaceimage'),(6,'users','users');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-21 03:15:51.828731'),(2,'contenttypes','0002_remove_content_type_name','2025-05-21 03:15:51.832409'),(3,'auth','0001_initial','2025-05-21 03:15:51.834700'),(4,'auth','0002_alter_permission_name_max_length','2025-05-21 03:15:51.836609'),(5,'auth','0003_alter_user_email_max_length','2025-05-21 03:15:51.838047'),(6,'auth','0004_alter_user_username_opts','2025-05-21 03:15:51.839564'),(7,'auth','0005_alter_user_last_login_null','2025-05-21 03:15:51.840912'),(8,'auth','0006_require_contenttypes_0002','2025-05-21 03:15:51.842401'),(9,'auth','0007_alter_validators_add_error_messages','2025-05-21 03:15:51.844888'),(10,'auth','0008_alter_user_username_max_length','2025-05-21 03:15:51.847341'),(11,'auth','0009_alter_user_last_name_max_length','2025-05-21 03:15:51.849682'),(12,'auth','0010_alter_group_name_max_length','2025-05-21 03:15:51.852334'),(13,'auth','0011_update_proxy_permissions','2025-05-21 03:15:51.853891'),(14,'auth','0012_alter_user_first_name_max_length','2025-05-21 03:15:51.855726'),(15,'users','0001_initial','2025-05-21 03:15:51.857332'),(16,'admin','0001_initial','2025-05-21 03:15:51.858968'),(17,'admin','0002_logentry_remove_auto_add','2025-05-21 03:15:51.860903'),(18,'admin','0003_logentry_add_action_flag_choices','2025-05-21 03:15:51.862433'),(19,'evaluations','0001_initial','2025-05-21 03:15:51.863857'),(20,'evaluations','0002_initial','2025-05-21 03:15:51.865306'),(21,'projects','0001_initial','2025-05-21 03:15:51.867571'),(22,'kpis','0001_initial','2025-05-21 03:15:51.869376'),(23,'kpis','0002_initial','2025-05-21 03:15:51.870920'),(24,'projects','0002_initial','2025-05-21 03:15:51.898379'),(25,'sessions','0001_initial','2025-05-21 03:15:51.901333'),(26,'evaluations','0003_alter_formquestions_options_and_more','2025-05-22 04:23:15.013859'),(27,'kpis','0003_alter_employeekpis_options_alter_kpis_options','2025-05-22 04:23:15.033258'),(28,'projects','0003_alter_deadlineextensionrequest_options','2025-05-22 04:23:15.045073'),(29,'users','0002_alter_aichatmessage_options_and_more','2025-05-22 04:23:15.071309');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2uu497e132c70t9qo5eto5cz2gb8o7id','.eJxVjEEOwiAQRe_C2hCKTAdcuvcMBJhBqgaS0q6Md7dNutDtf-_9t_BhXYpfO89-InERTpx-txjSk-sO6BHqvcnU6jJPUe6KPGiXt0b8uh7u30EJvWx1JAY0SI4TgLPnQWW2AcygdUIiGB1sClmtOWMYs0oKEzBCRBttNuLzBfVeOFo:1uIobG:6dAgYLzeOnsf0QdlXRXM_XApb0M8bNP70qCVOXL1dWI','2025-06-07 13:07:42.913986'),('4ifmv5fnxb23f04kpeecykx286l2ji0q','.eJxVjEEOwiAQRe_C2hCKTAdcuvcMBJhBqgaS0q6Md7dNutDtf-_9t_BhXYpfO89-InERTpx-txjSk-sO6BHqvcnU6jJPUe6KPGiXt0b8uh7u30EJvWx1JAY0SI4TgLPnQWW2AcygdUIiGB1sClmtOWMYs0oKEzBCRBttNuLzBfVeOFo:1uJ8tJ:tFpFcUsXrP7nAkLW98DPWC7xdWXWLCermMXB_1JgLy4','2025-06-08 10:47:41.055722'),('6qyo16zf5b3j8tmlngetfzje6s4r7dwl','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uGbOF:zQt-PYum61FngoSReGAlPnljtbeEsSUA6cyHNW5dJCg','2025-06-01 10:37:07.317362'),('96m87fd9wbsmaemkejwhlxc70bjfsfjr','.eJxVjEEOwiAQRe_C2hCKTAdcuvcMBJhBqgaS0q6Md7dNutDtf-_9t_BhXYpfO89-InERTpx-txjSk-sO6BHqvcnU6jJPUe6KPGiXt0b8uh7u30EJvWx1JAY0SI4TgLPnQWW2AcygdUIiGB1sClmtOWMYs0oKEzBCRBttNuLzBfVeOFo:1uIPNm:MoK7yFUL2dDx6FI0ssIHHUyzLd2vbnNq-SOIblJDE3g','2025-06-06 10:12:06.565099'),('bbjwqb7r10xuh8jmovwxrjszlyqipof0','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uE0BP:1B6mfkJpkgeeoIJVQNqlfjYMj_gE-g3Lnjw0cH7FhrU','2025-05-25 06:29:07.943494'),('dxt3lcccl12983eaedtgc0v1ecbvrjq8','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uItMA:WD2UktvnGC89K68j-SycA71jAULPEuIvf3W86iUL2n4','2025-06-07 18:12:26.943480'),('e3upjii43b60h8s7mdazvve25yz5d4sn','.eJxVTEsOwiAQvQtrQ4oMIC7d9wxk6EylaiAp7cp499Kki7p5ef-vCLguKayV5zCRuAsvLmcv4vDmvAf0wvwscih5maco94o80ir7Qvx5HN2_g4Q1tbVxoG_R4ahYNxI7D0CRFXlN3japgZwFbGCMQQQcrw7RM1iw1Cnx2wDfrDev:1uFj22:e4MqNXLaSyjhrM1joIUyYlSJQpiYJ6sZpdlYEzmeRfA','2025-05-30 00:34:34.847897'),('eyhcatccprbchdrac4x3l22pkjzbxav5','.eJxVjEEOwiAQRe_C2pAphcK4dO8ZyDBDpWpoUtqV8e7apAvd_vfef6lI21ri1vISJ1Fnher0uyXiR647kDvV26x5rusyJb0r-qBNX2fJz8vh_h0UauVbs_cskHoDFAyFHNBhGG0_eALrgBnAD5KcM8mwt9aMzJwRkTpHJJ16fwDaXzfS:1uGbLH:YgmwmS0GWlT8zyr8v7M_tqOmklTyQxJSqvDhLf9TIMs','2025-06-01 10:34:03.529159'),('g46lyqwkezero4pt731kw5yx4vsw61xs','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uGD6b:i9K9vJOZ-zo2fJTaVEPVZXzEwaF206H9_9D354P1W_Q','2025-05-31 08:41:17.348755'),('jqipyb4yakw8pxqk4habt5wwm9q2mvlo','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uGDA7:Ksa5tHS_wahrywgQsGKnapVWUsk3-XHPrqzBaVtCfWk','2025-05-31 08:44:55.418177'),('lot5czxmg1jx3m2ri3f26fc9meiis6sd','.eJxVjDsOwjAQBe_iGlne-LempOcMlj9rHEC2FCcV4u4QKQW0b2bei_mwrdVvgxY_Z3ZmwE6_WwzpQW0H-R7arfPU27rMke8KP-jg157peTncv4MaRv3WolgLGidRQApnQGrlJGEqiJlUcGBcDqpgogKERkGUJkkko4Wzcors_QG5ezb-:1uM0dA:ovLkYBz_-cDKxR9qk4LwMI79rNPSzKckz-4yK6ucHg4','2025-06-16 08:34:52.023964'),('luaseydapmy8gj863jljj4v19tzstz5f','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uEeP8:UEITJyFgzaqjdVc6ImlH3oUkK9gP-mB89ZpceL6fkTI','2025-05-27 01:25:58.294813'),('se4gs8th7363u2hqxif1wykkd4b9a66a','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uEUia:S4duw5OPodjNUpijo_eCx217IELY_TOAmx8SR_xClVA','2025-05-26 15:05:24.128586'),('t1qboivx5y9wq7706l6lx1yoweyyk0y2','.eJxVjDEOAiEQRe9CbcjgggyW9p6BzDAoqwaSZbcy3t2QbKHtf-_9t4q0rSVuPS9xFnVWQR1-N6b0zHUAeVC9N51aXZeZ9VD0Tru-Nsmvy-7-HRTqZdSGxRtwQmDBAdrJMzBg8o6PToIhnLKkQAJCJ0R2N8goybEVIUzq8wXiCjiE:1uM0cC:0zt5gytbiQ-6QNGyahbIku5fKX7JLJap32LHqjrnLZ4','2025-06-16 08:33:52.099355'),('w0z5m5cczxg464dxklzkoy4nc3uu3ope','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uHc40:ZTdrWYxxITAdvnK5LxOiw-NN44gZ4evQ-jLbGmnhi04','2025-06-04 05:32:24.489978'),('w2voqjcx4sct9pmbl6auoguototu4m4q','.eJxVjEEOwiAQRe_C2hCKTAdcuvcMBJhBqgaS0q6Md7dNutDtf-_9t_BhXYpfO89-InERTpx-txjSk-sO6BHqvcnU6jJPUe6KPGiXt0b8uh7u30EJvWx1JAY0SI4TgLPnQWW2AcygdUIiGB1sClmtOWMYs0oKEzBCRBttNuLzBfVeOFo:1uIqpS:wK6w8bW_DqJ7SdpCgXO08RjTzrEhLtWaz0WwwXss-Rc','2025-06-07 15:30:30.434440'),('zsk1gvq8f11exq9yqca5fo6p4z0pcsxw','.eJxVjMsOwiAQRf-FtSGFkZdL934DAWaQqoGktCvjv0uTLnR7zrn3zXzY1uK3ToufkV2YY6dfFkN6Ut0FPkK9N55aXZc58j3hh-381pBe16P9Oyihl7EO4LTUIhNEMjGDRpo0nsEOLFCIOAKpcFJkrDIJUlQZg5MOdEKwkn2-4yE3sw:1u4Ml3:pPCBfkL0_54C5U904sDtzNuoDxrgwOPCxLeq9YhAL4Q','2025-04-28 16:34:05.048151');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_kpis`
--

DROP TABLE IF EXISTS `employee_kpis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_kpis` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `target_value` double NOT NULL,
  `actual_value` double DEFAULT NULL,
  `time_period` varchar(20) NOT NULL,
  `evaluation` varchar(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `kpi_id` bigint NOT NULL,
  `achieved_percentage` double NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_kp_user_id_2ebafc_idx` (`user_id`,`start_date`),
  KEY `employee_kp_kpi_id_889c8e_idx` (`kpi_id`,`time_period`),
  CONSTRAINT `employee_kpis_kpi_id_31c99cc4_fk_kpis_id` FOREIGN KEY (`kpi_id`) REFERENCES `kpis` (`id`),
  CONSTRAINT `employee_kpis_user_id_9f2d7c4c_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_kpis`
--

LOCK TABLES `employee_kpis` WRITE;
/*!40000 ALTER TABLE `employee_kpis` DISABLE KEYS */;
INSERT INTO `employee_kpis` VALUES (13,1000,950,'Monthly','Partially Achieved',9,7,95,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(14,4,3,'Monthly','Partially Achieved',9,8,75,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(17,1000,900,'Monthly','Not Achieved',11,7,90,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(20,10,8,'Monthly','Partially Achieved',9,9,80,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(21,160,150,'Monthly','Partially Achieved',9,10,93.75,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(22,5,4,'Monthly','Achieved',9,11,80,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(23,10,9,'Monthly','Achieved',9,12,90,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(24,100,95,'Monthly','Achieved',9,13,95,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000');
/*!40000 ALTER TABLE `employee_kpis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form_questions`
--

DROP TABLE IF EXISTS `form_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form_questions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question_text` longtext NOT NULL,
  `form_id` bigint NOT NULL,
  `question_type` varchar(10) NOT NULL DEFAULT 'text',
  `max_score` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `form_questions_form_id_5bf33b25_fk_forms_id` (`form_id`),
  CONSTRAINT `form_questions_form_id_5bf33b25_fk_forms_id` FOREIGN KEY (`form_id`) REFERENCES `forms` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_questions`
--

LOCK TABLES `form_questions` WRITE;
/*!40000 ALTER TABLE `form_questions` DISABLE KEYS */;
INSERT INTO `form_questions` VALUES (1,'Đánh giá khả năng hợp tác của đồng nghiệp',5,'rating',100),(2,'Điểm mạnh của đồng nghiệp là gì?',5,'text',NULL),(3,'Hiệu suất làm việc của nhân viên?',2,'rating',100),(4,'Các khuyến điểm mà nhân viên cần cải thiện?',2,'text',NULL),(5,'Bạn đánh giá thế nào về mức độ hợp tác của động nghiệp',3,'rating',100),(6,'Ý kiến đóng góp cho đồng nghiệp',3,'text',NULL),(8,'Bạn đánh giá thế nào về tinh thần hợp tác của đồng nghiệp?',1,'rating',10),(9,'Ý kiến đóng góp cho đồng nghiệp',1,'text',NULL),(10,'Ưu điểm của nhân viên cần được phát huy',2,'text',NULL),(11,'Đánh giá tổng thế kết quả của nhân viên trong quý vừa qua',2,'text',NULL),(12,'Mức độ hài lòng của các thành viên khác trong team đối với nhân viên',2,'rating',100),(13,'Đánh giá mức độ phát huy của nhân viên so với quý trước',2,'rating',100),(14,'Điểm mạnh của đồng nghiệp là gì',6,'text',NULL),(15,'Đánh giá mức độ hài lòng về đồng nghiệp',6,'rating',100);
/*!40000 ALTER TABLE `form_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form_responses`
--

DROP TABLE IF EXISTS `form_responses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `form_responses` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `answer` longtext NOT NULL,
  `target_user_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `form_id` bigint NOT NULL,
  `question_id` bigint NOT NULL,
  `answer_type` varchar(10) NOT NULL DEFAULT 'text',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `form_responses_target_user_id_ce09b7c1_fk_users_id` (`target_user_id`),
  KEY `form_responses_user_id_2ebdb88f_fk_users_id` (`user_id`),
  KEY `form_responses_form_id_929658e1_fk_forms_id` (`form_id`),
  KEY `form_responses_question_id_fkey` (`question_id`),
  CONSTRAINT `form_responses_form_id_929658e1_fk_forms_id` FOREIGN KEY (`form_id`) REFERENCES `forms` (`id`),
  CONSTRAINT `form_responses_question_id_fkey` FOREIGN KEY (`question_id`) REFERENCES `form_questions` (`id`) ON DELETE CASCADE,
  CONSTRAINT `form_responses_target_user_id_ce09b7c1_fk_users_id` FOREIGN KEY (`target_user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `form_responses_user_id_2ebdb88f_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_responses`
--

LOCK TABLES `form_responses` WRITE;
/*!40000 ALTER TABLE `form_responses` DISABLE KEYS */;
INSERT INTO `form_responses` VALUES (1,'4',9,3,2,3,'numeric','2025-05-03 09:00:00'),(2,'Cải thiện kỹ năng quản lý thời gian',9,3,2,4,'text','2025-05-03 09:00:00'),(3,'3',9,5,1,1,'numeric','2025-05-01 10:00:00'),(4,'Kỹ năng lập trình tốt nhưng cần chủ động hơn',9,5,1,2,'text','2025-05-01 10:00:00'),(5,'5',6,9,1,1,'numeric','2025-05-02 14:00:00'),(6,'Hỗ trợ team rất tích cực',6,9,1,2,'text','2025-05-02 14:00:00'),(7,'4',7,9,3,5,'numeric','2025-05-04 11:00:00'),(8,'Cần cải thiện giao tiếp trong team',7,9,3,6,'text','2025-05-04 11:00:00'),(9,'5',9,6,3,5,'numeric','2025-05-04 12:00:00'),(10,'Rất nhiệt tình trong công việc',9,6,3,6,'text','2025-05-04 12:00:00');
/*!40000 ALTER TABLE `form_responses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forms`
--

DROP TABLE IF EXISTS `forms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forms` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(10) NOT NULL,
  `period` varchar(20) NOT NULL,
  `deadline` datetime DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'open',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forms`
--

LOCK TABLES `forms` WRITE;
/*!40000 ALTER TABLE `forms` DISABLE KEYS */;
INSERT INTO `forms` VALUES (1,'Feedback tháng 6','peer','Quarterly','2025-06-29 23:59:59','open'),(2,'Performance Review Q1 2025','review','Quarterly','2025-06-30 23:59:59','open'),(3,'Feedback tháng 5','feedback','Monthly','2025-05-31 23:59:59','open'),(5,'Peer Review Tháng 5','peer','monthly','2025-05-31 00:00:00','open'),(6,'Peer review tháng 6','peer','monthly','2025-06-29 17:00:00','open');
/*!40000 ALTER TABLE `forms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kpis`
--

DROP TABLE IF EXISTS `kpis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kpis` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `kpi_type` varchar(20) NOT NULL,
  `project_id` bigint DEFAULT NULL,
  `unit` varchar(20) DEFAULT NULL,
  `weight` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `kpis_project_id_292e15be_fk_projects_id` (`project_id`),
  CONSTRAINT `kpis_project_id_292e15be_fk_projects_id` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kpis`
--

LOCK TABLES `kpis` WRITE;
/*!40000 ALTER TABLE `kpis` DISABLE KEYS */;
INSERT INTO `kpis` VALUES (7,'Thời gian giao tiếp','Giảm thiếu các lỗi giao tiếp, tăng hiệu suất khả năng trình bày, phản biện','Quality',2,'score',1.5),(8,'Phản hồi từ đồng nghiệp','Đánh giá dựa trên các phản hồi từ đồng nghiệp','Efficiency',1,'unit',1),(9,'Số lượng task hoàn thành','Số lượng task hoàn thành trong tháng','Quantitative',1,'task',1),(10,'Số giờ làm việc','Tổng số giờ làm việc thực tế','Quantitative',2,'hour',1),(11,'Thái độ làm việc','Đánh giá thái độ làm việc của nhân viên','Qualitative',1,'score',1),(12,'Chất lượng code','Đánh giá chất lượng code qua review','Quality',1,'score',1),(13,'Hiệu suất xử lý task','Tỷ lệ hoàn thành task đúng hạn','Efficiency',2,'%',1),(14,'Số lỗi mắc phải','Số lượng bug mắc phải trong quá trình thực hiện các công việc','Quantitative',1,'Bug',2);
/*!40000 ALTER TABLE `kpis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `manager_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `projects_manager_id_a2bc48df_fk_users_id` (`manager_id`),
  CONSTRAINT `projects_manager_id_a2bc48df_fk_users_id` FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'Dự án Quản lý Nhân sự','## **DỰ ÁN PHẦN MỀM QUẢN LÝ NHÂN SỰ (HRM SYSTEM)**\r\n\r\n### **Mô tả chi tiết dự án**\r\n\r\n---\r\n\r\n### **1. Thông tin tổng quan**\r\n\r\n* **Tên dự án**: Hệ thống Quản lý Nhân sự Tập đoàn XYZ\r\n* **Mục tiêu**:\r\n  Xây dựng một nền tảng quản lý nhân sự tập trung, số hóa toàn bộ quy trình liên quan đến nhân sự, từ tuyển dụng, chấm công, tính lương đến đánh giá hiệu suất, nhằm tăng hiệu quả quản lý, giảm chi phí vận hành và hỗ trợ quá trình chuyển đổi số của doanh nghiệp.\r\n\r\n---\r\n\r\n### **2. Đặc điểm kỹ thuật**\r\n\r\n* **Ngôn ngữ lập trình**: Python (Django), JavaScript (VueJS)\r\n* **CSDL sử dụng**: PostgreSQL 15\r\n* **Kiến trúc hệ thống**: Modular Monolith kết hợp API-first\r\n* **Triển khai**: Docker Compose + Nginx reverse proxy\r\n* **CI/CD**: GitLab CI + Docker Registry nội bộ\r\n* **Hệ điều hành máy chủ**: Ubuntu Server 22.04\r\n* **Cơ chế sao lưu dữ liệu**: Tự động hàng ngày với versioning lưu 30 ngày\r\n* **Bảo mật**:\r\n\r\n  * Mã hóa dữ liệu nhạy cảm (AES-256),\r\n  * Đăng nhập đa yếu tố (2FA),\r\n  * JWT Auth cho API,\r\n  * Role-Based Access Control (RBAC).\r\n\r\n---\r\n\r\n###  **3. Các mô-đun chức năng chính**\r\n\r\n####  **3.1. Quản lý hồ sơ nhân viên**\r\n\r\n* Hồ sơ cá nhân: họ tên, CCCD, ngày sinh, liên lạc, địa chỉ.\r\n* Thông tin hợp đồng: loại hợp đồng, thời hạn, phòng ban, cấp bậc.\r\n* Quản lý tài liệu đính kèm: CMND, bằng cấp, đơn xin việc...\r\n* Lịch sử thay đổi (luân chuyển nội bộ, nghỉ việc, gia hạn HĐ).\r\n\r\n#### **3.2. Tuyển dụng**\r\n\r\n* Đăng tin tuyển dụng nội bộ/ngoại bộ.\r\n* Quản lý ứng viên: CV, trạng thái ứng tuyển, lịch phỏng vấn.\r\n* Chấm điểm ứng viên theo tiêu chí định sẵn.\r\n* Phân tích nguồn ứng viên (jobsite, giới thiệu nội bộ...).\r\n\r\n#### **3.3. Chấm công & Lương**\r\n\r\n* Ghi nhận chấm công theo thiết bị (vân tay/RFID/web/app).\r\n* Cấu hình ca làm việc, làm thêm, nghỉ phép, ngày nghỉ lễ.\r\n* Tính lương tự động theo bảng công và hệ số (kèm phụ cấp).\r\n* Kết xuất bảng lương (Excel, PDF), xuất dữ liệu cho kế toán.\r\n\r\n####  **3.4. Quản lý nghỉ phép**\r\n\r\n* Nhân viên tạo yêu cầu nghỉ phép trực tuyến.\r\n* Tự động trừ phép và gửi phê duyệt tới cấp quản lý.\r\n* Quản lý tồn phép, lịch sử nghỉ theo năm.\r\n\r\n####  **3.5. Đánh giá hiệu suất (KPI)**\r\n\r\n* Thiết lập bộ chỉ tiêu theo vị trí/phòng ban.\r\n* Tự đánh giá, đánh giá từ quản lý.\r\n* Tính điểm tổng, xếp loại A/B/C...\r\n* Đồng bộ với khen thưởng, đề xuất tăng lương.\r\n\r\n#### **3.6. Quản lý đào tạo**\r\n\r\n* Lập kế hoạch đào tạo theo năm/quý.\r\n* Theo dõi khóa học, người tham gia, kết quả đánh giá sau đào tạo.\r\n* Đính kèm tài liệu đào tạo, biểu mẫu.\r\n\r\n####  **3.7. Hệ thống báo cáo**\r\n\r\n* Dashboard thống kê theo thời gian thực.\r\n* Báo cáo định kỳ: biến động nhân sự, hiệu suất phòng ban, tỷ lệ nghỉ phép.\r\n* Xuất báo cáo tùy chỉnh theo bộ lọc đa tiêu chí.\r\n\r\n---\r\n\r\n###  **4. Môi trường triển khai**\r\n\r\n| Môi trường | Mô tả                                            | Địa điểm                  |\r\n| ---------- | ------------------------------------------------ | ------------------------- |\r\n| Local Dev  | Docker-based local stack                         | Máy lập trình viên        |\r\n| Staging    | VPS riêng (4 CPU, 8GB RAM)                       | Cloud nội bộ              |\r\n| Production | Máy chủ vật lý đặt tại trung tâm dữ liệu công ty | On-premise (internal LAN) |\r\n\r\n---\r\n\r\n### **5. Quy trình hoạt động**\r\n\r\n1. **Đăng nhập SSO** thông qua tài khoản công ty (LDAP/Google Workspace).\r\n2. Giao diện dashboard hiển thị thông tin nhanh: ngày nghỉ, bảng công, thông báo.\r\n3. Mỗi người dùng được phân quyền theo vai trò: Nhân viên, Trưởng phòng, HR, Giám đốc.\r\n4. Toàn bộ quy trình đều lưu log (audit trail) phục vụ kiểm tra.\r\n\r\n---\r\n\r\n### **6. Giao diện người dùng**\r\n\r\n* Responsive đầy đủ trên mobile, tablet, desktop.\r\n* Hệ thống giao diện dạng dashboard đơn giản, hiện đại.\r\n* Chế độ tối (Dark Mode).\r\n* Hỗ trợ nhập liệu nhanh, lọc theo nhiều trường.\r\n\r\n---\r\n\r\n### **7. Bảo mật và quyền riêng tư**\r\n\r\n* Mã hóa thông tin cá nhân (PII) và lương nhân viên.\r\n* Tách quyền đọc/ghi theo cấp.\r\n* Theo dõi hành động người dùng (audit logs).\r\n* Cảnh báo đăng nhập bất thường và chống brute-force.\r\n\r\n---\r\n\r\n###  **8. Đội ngũ triển khai**\r\n\r\n* **1 Quản lý dự án (PM)**\r\n* **2 Kỹ sư backend Python**\r\n* **2 Kỹ sư frontend VueJS**\r\n* **1 Kỹ sư DevOps**\r\n* **1 QA Manual**\r\n* **1 QA Automation**\r\n* **1 Chuyên viên nhân sự hỗ trợ nhập liệu và đào tạo**\r\n\r\n---\r\n\r\n### **9. Lịch trình triển khai**\r\n\r\n| Giai đoạn                       | Thời gian | Nội dung                               |\r\n| ------------------------------- | --------- | -------------------------------------- |\r\n| Phân tích yêu cầu               | 2 tuần    | Xây dựng tài liệu URD, luồng nghiệp vụ |\r\n| Thiết kế hệ thống               | 2 tuần    | DB schema, UI/UX, sơ đồ tổng thể       |\r\n| Phát triển chức năng            | 6 tuần    | 7 module chính                         |\r\n| Kiểm thử nội bộ                 | 2 tuần    | UAT với phòng nhân sự                  |\r\n| Đào tạo & triển khai chính thức | 1 tuần    | Tài liệu + workshop                    |\r\n| Bảo trì và nâng cấp             | 12 tháng  | Miễn phí giai đoạn đầu                 |\r\n\r\n---\r\n\r\n###  **10. Lợi ích đạt được**\r\n\r\n* Tự động hóa quy trình nhân sự, giảm hơn 60% thời gian xử lý giấy tờ.\r\n* Minh bạch hóa lương, thưởng, đánh giá – tăng độ hài lòng nhân viên.\r\n* Giúp lãnh đạo ra quyết định chính xác dựa trên dữ liệu nhân sự thời gian thực.\r\n* Hạn chế thất thoát dữ liệu nhân sự, tăng bảo mật thông tin nội bộ.','2024-05-01 08:00:00.000000','2025-10-17 17:00:00.000000',1),(2,'Dự án Cổng thông tin điện tử','## **DỰ ÁN CỔNG THÔNG TIN ĐIỆN TỬ**\r\n\r\n###  **Mô tả chi tiết dự án**\r\n\r\n---\r\n\r\n###  **1. Thông tin chung**\r\n\r\n* **Tên dự án**: Cổng Thông Tin Điện Tử – Văn phòng UBND Tỉnh A\r\n* **Mục tiêu**:\r\n  Phát triển một hệ thống cổng thông tin điện tử hiện đại nhằm cung cấp thông tin hành chính công, văn bản pháp luật, dịch vụ công trực tuyến, và các thông báo chính thức từ UBND tỉnh A đến người dân, doanh nghiệp và cán bộ nhà nước.\r\n  Đồng thời tạo nền tảng tích hợp với các hệ thống hành chính khác (một cửa điện tử, quản lý văn bản điều hành, thư viện số...).\r\n\r\n---\r\n\r\n###  **2. Đặc điểm kỹ thuật chung**\r\n\r\n* **Ngôn ngữ lập trình**: Python (Django), JavaScript (ReactJS)\r\n* **Hệ quản trị CSDL**: MySQL 8.0\r\n* **Công nghệ giao diện**: ReactJS (Tailwind CSS), hỗ trợ Responsive\r\n* **Kiến trúc**: Microservices + REST API\r\n* **Hệ điều hành server**: Ubuntu Server 22.04 LTS\r\n* **Container hóa**: Docker, Docker Compose\r\n* **CI/CD**: GitHub Actions + Docker Hub + Deployment qua SSH\r\n* **Hệ thống giám sát**: Prometheus + Grafana\r\n* **Lưu trữ tệp tin**: MinIO (self-hosted object storage)\r\n* **Bảo mật**:\r\n\r\n  * HTTPS (SSL Let\'s Encrypt),\r\n  * OAuth2 (SSO qua Keycloak),\r\n  * WAF và kiểm soát IP,\r\n  * Bảo vệ CSRF/XSS/SQLi.\r\n\r\n---\r\n\r\n###  **3. Mô-đun chức năng chính**\r\n\r\n####  **3.1. Trang thông tin công cộng**\r\n\r\n* Trang chủ hiển thị tin tức nổi bật, thông báo mới.\r\n* Chuyên mục: Kinh tế, Văn hóa, Giáo dục, Y tế, Đầu tư...\r\n* Tìm kiếm theo từ khóa, thời gian, chuyên mục.\r\n* RSS feeds cho từng chuyên mục.\r\n\r\n####  **3.2. Quản lý văn bản**\r\n\r\n* Quản lý văn bản đến, văn bản đi (PDF, DOCX).\r\n* Cho phép cán bộ đăng tải, phân quyền truy cập nội bộ/ngoại bộ.\r\n* Lưu trữ lịch sử sửa đổi văn bản.\r\n\r\n####  **3.3. Dịch vụ công trực tuyến**\r\n\r\n* Danh mục các dịch vụ công theo lĩnh vực.\r\n* Gửi yêu cầu trực tuyến (hồ sơ điện tử).\r\n* Theo dõi trạng thái xử lý hồ sơ.\r\n* Thông báo tự động qua email/SMS.\r\n\r\n#### **3.4. Quản lý người dùng & phân quyền**\r\n\r\n* Đăng ký công dân, doanh nghiệp.\r\n* Quản lý cán bộ với phân quyền theo phòng ban, vai trò.\r\n* Hệ thống Single Sign-On (SSO) qua Keycloak.\r\n\r\n####  **3.5. CMS quản trị nội dung**\r\n\r\n* Đăng tin, soạn thảo bài viết có hỗ trợ định dạng WYSIWYG.\r\n* Phân loại bài viết theo chuyên mục, trạng thái hiển thị.\r\n* Lưu nháp, kiểm duyệt, xuất bản.\r\n\r\n####  **3.6. Quản trị hệ thống**\r\n\r\n* Dashboard thống kê lượt truy cập, số lượng hồ sơ, văn bản, bài viết.\r\n* Cấu hình hệ thống: logo, banner, footer, ngôn ngữ.\r\n* Quản lý backup dữ liệu, nhật ký hệ thống.\r\n\r\n---\r\n\r\n###  **4. Tích hợp & Liên thông**\r\n\r\n* **Kết nối CSDL quốc gia**: CSDL dân cư (qua API).\r\n* **Tích hợp Zalo OA, Email SMTP, SMS Viettel**: gửi thông báo xử lý hồ sơ.\r\n* **Liên thông dịch vụ công mức độ 3/4** với cổng DVCQG (Cổng Dịch Vụ Công Quốc Gia).\r\n* **LDAP hoặc AD nội bộ**: Đồng bộ nhân sự và phân quyền.\r\n\r\n---\r\n\r\n###  **5. Giao diện và trải nghiệm người dùng**\r\n\r\n* **Responsive**: Tương thích mọi thiết bị (mobile/tablet/PC).\r\n* **Hỗ trợ song ngữ**: Tiếng Việt & Tiếng Anh.\r\n* **Hệ thống theme**: Giao diện có thể tùy chỉnh màu sắc và bố cục.\r\n* **Trợ năng (accessibility)**: Hỗ trợ người khiếm thị qua WCAG 2.1.\r\n\r\n---\r\n\r\n### **6. Môi trường triển khai**\r\n\r\n| Môi trường | Hệ thống                                 | Mục đích             |\r\n| ---------- | ---------------------------------------- | -------------------- |\r\n| Local Dev  | Docker (dev)                             | Phát triển tính năng |\r\n| Staging    | VPS riêng (Ubuntu)                       | Kiểm thử nội bộ, QA  |\r\n| Production | Máy chủ vật lý tại Trung tâm CNTT tỉnh A | Vận hành chính thức  |\r\n\r\n---\r\n\r\n###  **7. Đội ngũ thực hiện**\r\n\r\n* **1 PM** – Quản lý dự án, tiếp nhận yêu cầu từ UBND.\r\n* **3 Dev Backend (Python/Django)**\r\n* **2 Dev Frontend (ReactJS)**\r\n* **1 DevOps** – Xây dựng pipeline CI/CD, bảo mật hệ thống.\r\n* **1 Tester** – Kiểm thử thủ công và tự động.\r\n* **1 Chuyên viên nội dung** – Viết tài liệu hướng dẫn, soạn demo nội dung.\r\n\r\n---\r\n\r\n### **8. Tiến độ dự kiến**\r\n\r\n| Giai đoạn                  | Thời gian   | Nội dung                            |\r\n| -------------------------- | ----------- | ----------------------------------- |\r\n| Khởi động & phân tích      | 2 tuần      | Lấy yêu cầu, viết đặc tả            |\r\n| Thiết kế giao diện & UX    | 2 tuần      | Thiết kế figma, lấy ý kiến phản hồi |\r\n| Phát triển & tích hợp      | 6 tuần      | Toàn bộ backend, frontend, API      |\r\n| Kiểm thử và triển khai thử | 2 tuần      | Staging test, load test, UAT        |\r\n| Đào tạo và chuyển giao     | 1 tuần      | Hướng dẫn sử dụng, bảo trì          |\r\n| Vận hành chính thức        | Sau tuần 13 | Triển khai Production               |\r\n\r\n---\r\n\r\n###  **9. Bảo trì & Hỗ trợ**\r\n\r\n* Bảo trì 12 tháng miễn phí sau nghiệm thu.\r\n* Cung cấp hotline 24/7 trong giai đoạn vận hành 3 tháng đầu.\r\n* Có hệ thống log lỗi, phản hồi người dùng, cập nhật bảo mật định kỳ.\r\n\r\n---\r\n\r\n###  **10. Lợi ích kỳ vọng**\r\n\r\n* Minh bạch thông tin và nâng cao trải nghiệm dịch vụ công cho người dân.\r\n* Rút ngắn thời gian xử lý hồ sơ, giảm tải cho cán bộ hành chính.\r\n* Tạo nền tảng sẵn sàng kết nối Chính phủ điện tử và chuyển đổi số toàn diện.','2024-05-15 08:00:00.000000','2025-09-17 17:00:00.000000',1);
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_assignments`
--

DROP TABLE IF EXISTS `task_assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_assignments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `task_id` bigint NOT NULL,
  `estimated_time` double DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `role` varchar(50) NOT NULL,
  `actual_time` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_assignments_task_id_user_id_role_125ff693_uniq` (`task_id`,`user_id`,`role`),
  KEY `task_assignments_user_id_8237dbae_fk_users_id` (`user_id`),
  KEY `task_assignments_task_id_user_id_idx` (`task_id`,`user_id`),
  KEY `task_assignments_status_idx` (`status`),
  CONSTRAINT `task_assignments_task_id_dbef494b_fk_tasks_id` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `task_assignments_user_id_8237dbae_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_assignments`
--

LOCK TABLES `task_assignments` WRITE;
/*!40000 ALTER TABLE `task_assignments` DISABLE KEYS */;
INSERT INTO `task_assignments` VALUES (1,1,1,15,'Completed','Thực hiện chính',14.5),(2,3,1,5,'Completed','Đồng thực hiện',4),(3,3,2,15,'Completed','Thực hiện chính',16.2),(4,3,3,30,'In progress','Thực hiện chính',15.5),(5,4,3,10,'In progress','Review',5),(6,3,4,25,'To-do','Thực hiện chính',0),(7,4,4,10,'To-do','Test',0),(8,4,5,15,'To-do','Thực hiện chính',0),(9,3,5,10,'To-do','Review',0),(10,2,6,12,'Completed','Thực hiện chính',12.8),(11,5,6,6,'Completed','Review',5),(12,4,7,20,'In progress','Thực hiện chính',12.5),(13,3,8,25,'To-do','Thực hiện chính',0),(14,5,9,22,'To-do','Thực hiện chính',0),(15,5,10,20,'To-do','Thực hiện chính',0),(16,3,10,10,'To-do','Đồng thực hiện',0),(32,9,2,4,'To-do','Thực hiện chính',8.083333333333334),(33,9,3,5,'To-do','Thực hiện chính',5),(34,9,4,3,'Completed','Thực hiện chính',1),(35,9,5,4,'Completed','Test',8),(36,9,8,4,'Completed','Đồng thực hiện',4.016666666666667),(37,9,10,8,'In progress','Review',0),(38,9,9,12,'In progress','Thực hiện chính',0);
/*!40000 ALTER TABLE `task_assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `deadline` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `difficulty` varchar(20) NOT NULL,
  `estimated_time` double DEFAULT NULL,
  `github_link` varchar(200) DEFAULT NULL,
  `project_id` bigint NOT NULL,
  `is_tracking` tinyint(1) NOT NULL,
  `total_time` double NOT NULL,
  `notes` longtext,
  `completed_date` datetime(6) DEFAULT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tasks_project_id_288f49d9_fk_projects_id` (`project_id`),
  KEY `tasks_deadlin_7f16a6_idx` (`deadline`),
  KEY `tasks_status_031d4c_idx` (`status`),
  KEY `tasks_start_d_efea8c_idx` (`start_date`),
  CONSTRAINT `tasks_project_id_288f49d9_fk_projects_id` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Phân tích yêu cầu','Phân tích yêu cầu chi tiết cho hệ thống quản lý nhân sự','2024-05-15 17:00:00.000000','Completed','Medium',20,NULL,1,0,18.5,'Đã hoàn thành đúng tiến độ','2024-05-14 17:00:00.000000','2024-05-01 09:00:00.000000'),(2,'Thiết kế cơ sở dữ liệu','Thiết kế schema cơ sở dữ liệu cho hệ thống','2024-05-25 17:00:00.000000','Completed','Hard',15,'https://github.com/abc/hrm-db',1,0,24.28333333333333,NULL,'2024-05-24 17:00:00.000000','2024-05-15 09:00:00.000000'),(3,'Phát triển module quản lý nhân viên','Xây dựng module quản lý thông tin nhân viên','2024-06-15 17:00:00.000000','In progress','Hard',40,'https://github.com/abc/hrm-employee',1,0,25.5,NULL,NULL,'2024-05-25 09:00:00.000000'),(4,'Phát triển module chấm công','Xây dựng module chấm công và tính lương','2024-06-30 17:00:00.000000','Late','Hard',35,NULL,1,0,1,NULL,NULL,'2025-05-18 07:40:00.000000'),(5,'Kiểm thử hệ thống','Kiểm thử toàn bộ hệ thống','2024-07-15 17:00:00.000000','Late','Medium',25,'https://github.com/loochuynhh/humanity_os/issues/9',1,1,8,'Task mới dễ hơn task cũ',NULL,'2025-05-18 05:10:00.000000'),(6,'Phân tích yêu cầu','Phân tích yêu cầu chi tiết cho cổng thông tin điện tử','2024-05-30 17:00:00.000000','Completed','Medium',18,NULL,2,0,17.8,NULL,'2024-05-29 17:00:00.000000','2024-05-15 09:00:00.000000'),(7,'Thiết kế giao diện','Thiết kế UI/UX cho cổng thông tin','2024-06-15 17:00:00.000000','In progress','Medium',20,'https://github.com/abc/portal-ui',2,0,12.5,NULL,NULL,'2024-05-31 09:00:00.000000'),(8,'Phát triển module tin tức','Xây dựng module quản lý tin tức','2024-06-30 17:00:00.000000','In progress','Medium',25,NULL,2,0,4.016666666666667,NULL,NULL,'2025-05-14 18:56:00.000000'),(9,'Phát triển module tài liệu','Xây dựng module quản lý tài liệu','2024-07-15 17:00:00.000000','To-do','Medium',22,NULL,2,0,0,NULL,NULL,NULL),(10,'Kiểm thử và triển khai','Kiểm thử và triển khai hệ thống','2024-08-15 17:00:00.000000','Late','Hard',30,'https://github.com/loochuynhh/humanity_os/issues/10',2,0,0,'',NULL,NULL);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team_project_memberships`
--

DROP TABLE IF EXISTS `team_project_memberships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team_project_memberships` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `join_date` datetime(6) NOT NULL,
  `project_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `team_project_memberships_project_id_user_id_126ee7ca_uniq` (`project_id`,`user_id`),
  KEY `team_project_memberships_user_id_b2a800f3_fk_users_id` (`user_id`),
  CONSTRAINT `team_project_memberships_project_id_c6bb2041_fk_projects_id` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `team_project_memberships_user_id_b2a800f3_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_project_memberships`
--

LOCK TABLES `team_project_memberships` WRITE;
/*!40000 ALTER TABLE `team_project_memberships` DISABLE KEYS */;
INSERT INTO `team_project_memberships` VALUES (1,'2024-05-01 08:00:00.000000',1,1,'Project Manager'),(2,'2024-05-01 08:00:00.000000',1,3,'Developer'),(3,'2024-05-01 08:00:00.000000',1,4,'Designer'),(4,'2024-05-15 08:00:00.000000',2,2,'Project Manager'),(5,'2024-05-15 08:00:00.000000',2,3,'Developer'),(6,'2024-05-15 08:00:00.000000',2,5,'Tester'),(13,'2025-05-17 18:52:19.000000',1,9,'Developer'),(14,'2025-05-17 18:52:20.000000',2,9,'Developer');
/*!40000 ALTER TABLE `team_project_memberships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_entries`
--

DROP TABLE IF EXISTS `time_entries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `time_entries` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `duration` double DEFAULT NULL,
  `task_assignment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `time_entries_new_task_assignment_start_time_idx` (`task_assignment_id`,`start_time`),
  KEY `time_entries_new_start_time_idx` (`start_time`),
  CONSTRAINT `time_entries_new_task_assignment_id_ad8e5d83_fk_task_assi` FOREIGN KEY (`task_assignment_id`) REFERENCES `task_assignments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_entries`
--

LOCK TABLES `time_entries` WRITE;
/*!40000 ALTER TABLE `time_entries` DISABLE KEYS */;
INSERT INTO `time_entries` VALUES (1,'2024-05-01 09:00:00.000000','2024-05-01 17:00:00.000000',8,1),(2,'2024-05-02 09:00:00.000000','2024-05-02 15:30:00.000000',6.5,1),(3,'2024-05-01 13:00:00.000000','2024-05-01 17:00:00.000000',4,2),(4,'2024-05-15 09:00:00.000000','2024-05-15 17:00:00.000000',8,3),(5,'2024-05-16 09:00:00.000000','2024-05-16 17:00:00.000000',8,3),(6,'2024-05-17 09:00:00.000000','2024-05-17 09:12:00.000000',0.2,3),(7,'2024-05-25 09:00:00.000000','2024-05-25 17:00:00.000000',8,4),(8,'2024-05-26 09:00:00.000000','2024-05-26 16:30:00.000000',7.5,4),(9,'2024-05-27 13:00:00.000000','2024-05-27 18:00:00.000000',5,5),(10,'2024-05-15 09:00:00.000000','2024-05-15 17:00:00.000000',8,10),(11,'2024-05-16 09:00:00.000000','2024-05-16 13:48:00.000000',4.8,10),(12,'2024-05-17 13:00:00.000000','2024-05-17 18:00:00.000000',5,11),(13,'2024-05-31 09:00:00.000000','2024-05-31 17:00:00.000000',8,12),(14,'2024-06-01 09:00:00.000000','2024-06-01 13:30:00.000000',4.5,12),(64,'2025-05-15 08:15:00.000000','2025-05-15 16:20:00.000000',8.083333333333334,32),(65,'2025-05-15 03:46:00.000000','2025-05-15 08:46:00.000000',5,33),(66,'2025-05-14 18:56:00.000000','2025-05-14 22:57:00.000000',4.016666666666667,36),(67,'2025-05-18 08:09:00.000000','2025-05-18 10:09:00.000000',2,35),(68,'2025-05-18 05:10:00.000000','2025-05-18 10:10:00.000000',5,35),(69,'2025-05-18 07:40:00.000000','2025-05-18 08:40:00.000000',1,34),(70,'2025-05-18 14:46:00.000000','2025-05-18 15:46:00.000000',1,35);
/*!40000 ALTER TABLE `time_entries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_face_images`
--

DROP TABLE IF EXISTS `user_face_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_face_images` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `face_image` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_face_images_user_id_c01f364d_fk_users_id` (`user_id`),
  CONSTRAINT `user_face_images_user_id_c01f364d_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_face_images`
--

LOCK TABLES `user_face_images` WRITE;
/*!40000 ALTER TABLE `user_face_images` DISABLE KEYS */;
INSERT INTO `user_face_images` VALUES (18,'face_images/Photo_from_2025-05-11_14-46-56.381557.jpeg','2025-05-11 07:47:51.535213',9),(21,'face_images/Photo_from_2025-05-11_14-46-49_kjXhXdz.975635.jpeg','2025-05-13 02:53:27.421460',9),(22,'face_images/checkin_lochuynh2_2025-05-13_1747102526.jpg','2025-05-13 02:53:40.414752',9),(23,'face_images/checkin_lochuynh2_2025-05-13_1747102005_8x0bZSe.jpg','2025-05-13 02:53:47.321307',9),(24,'face_images/checkin_lochuynh2_2025-05-12_1747062207.jpg','2025-05-13 02:53:55.807615',9),(25,'face_images/checkin_lochuynh2_2025-05-13_1747099642.jpg','2025-05-13 02:54:02.948161',9),(26,'face_images/checkin_lochuynh2_2025-05-12_1747062364.jpg','2025-05-13 02:54:10.947019',9),(27,'face_images/Photo_from_2025-05-13_09-55-36.471145.jpeg','2025-05-13 02:56:09.456998',9),(28,'face_images/Photo_from_2025-05-11_14-46-56_EArmSkd.381557.jpeg','2025-05-13 06:22:35.598192',9),(29,'face_images/webcam-toy-photo1.jpg','2025-05-17 08:43:38.040878',9),(30,'face_images/webcam-toy-photo2.jpg','2025-05-17 08:47:45.930927',9),(33,'face_images/son-tung-mtp-08110778-1651217357607701319631.jpg','2025-06-02 08:56:37.329039',3),(35,'face_images/4KG2VgKFDJWqdtg4UMRqk5CnkJVoCpe5QMd20Pf7.jpg','2025-06-02 08:56:58.128313',3),(36,'face_images/ab6761610000e5eb5a79a6ca8c60e4ec1440be53.jpeg','2025-06-02 08:57:06.114024',3),(37,'face_images/Son_Tung_M-TP_1_2017.png','2025-06-02 08:57:14.904836',3),(38,'face_images/channels4_profile.jpg','2025-06-02 08:57:26.531876',3),(39,'face_images/bp_Lege2lm.jpeg','2025-06-02 08:59:19.458604',6),(40,'face_images/bp.jpeg','2025-06-02 08:59:26.798294',6),(41,'face_images/bp2bp.jpeg','2025-06-02 08:59:34.352632',6);
/*!40000 ALTER TABLE `user_face_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `date_of_joining` date DEFAULT NULL,
  `fixed_location` varchar(255) DEFAULT NULL,
  `bio` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'pbkdf2_sha256$870000$d6Yw3mN6tleKbshH6CFf6v$en2KQPcVFORynDRAITeT+UIVpPhyqRYlOv2H95wIq7c=','2025-06-02 08:34:52.000000',1,'lochuynh','','','lochuynh@gmail.com',1,1,'2025-04-03 16:44:28.000000','avatars/admin_BX0UIWq.png','0342063017','Employee','BOD','Active',NULL,'16.0752324,108.1523430',NULL),(2,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 10:00:00.000000',1,'admin','System','Admin','admin@humanityos.com',1,1,'2024-01-01 09:00:00.000000','avatars/admin.png','012345133434','Administrator','BOD','Active','2024-01-01','16.0751009,108.1519032',NULL),(3,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 09:30:00.000000',0,'PhanTanPhat','John','Doe','phantanphat@humanityos.com',1,1,'2024-01-15 09:00:00.000000','avatars/user_3I0hTM5.jpeg','012335464','Project Manager','IT','Active','2024-01-15','16.0751654,108.1524101',NULL),(4,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-02 17:45:00.000000',0,'Loilevan','Alice','Smith','loile@humanityos.com',1,1,'2024-02-01 09:00:00.000000','avatars/user.jpeg','09942532452','Team Lead','IT','Active','2024-02-01','16.0753274,108.1522036',NULL),(5,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 08:15:00.000000',0,'Sontranvan','Bob','Johnson','sontranvan@humanityos.com',1,1,'2024-02-15 09:00:00.000000','avatars/male2.png','0912341343','Senior Developer','IT','Active','2024-02-15','21.0278000,105.8342000',NULL),(6,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-01 16:30:00.000000',0,'Maithithao','Carol','Wilson','Maithithao@humanityos.com',1,1,'2024-03-01 09:00:00.000000','avatars/userfemale.jpeg','0123413413','Developer','QC','Active','2024-03-01','21.0278000,105.8342000',NULL),(7,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 10:20:00.000000',0,'TranVanThai','David','Lee','Thaitranvan@humanityos.com',1,1,'2024-03-15 09:00:00.000000','avatars/user_Z2zuIvn.jpeg','0923434654','Developer','IT','Active','2024-03-15','21.0278000,105.8342000',NULL),(8,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-03-30 14:10:00.000000',0,'NguyenThiThanh','Eva','Miller','thanhnguyenthi@humanityos.com',1,1,'2024-01-10 09:00:00.000000','avatars/userfemale2_j41tnB1.png','02345234597','HR Manager','HR','Active','2024-01-10','16.0749839,108.1521821',NULL),(9,'pbkdf2_sha256$870000$Sif4RCyv6qaBM58hW4z5gz$IckX0FgJFHznlLabfZioFwUTeS73UiSZ6kU2B77AFz4=','2025-06-02 08:33:52.000000',0,'lochuynh2','Lộc','Huỳnh','lochuynh03012003@gmail.com',1,1,'2025-04-03 17:04:23.000000','avatars/z3114906916031_93e78542eec3ab11c40bc4a219c83273.jpg','0342063017','Employee','IT','Active','2024-02-16','16.0768124,108.1605451','Bug creater '),(10,'pbkdf2_sha256$720000$abc$hashed_password',NULL,0,'nguyenhoa','Hoa','Nguyễn','nguyenhoa@humanityos.com',1,1,'2025-03-01 08:00:00.000000','avatars/userfemale2.png','0901234571','Employee','QC','Active','2025-03-01','16.0750870,108.1517100','Backend Developer'),(11,'pbkdf2_sha256$720000$abc$hashed_password',NULL,0,'lethithao','Thảo','Lê','lethithao@humanityos.com',1,1,'2025-03-01 08:00:00.000000','avatars/userfemale2_2SYX1qX.png','0901234572','Employee','Design','Active','2025-03-01','16.0752107,108.1520534','UI Designer');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_users_id_group_id_83a49e68_uniq` (`users_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_users_id_1e682706_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

LOCK TABLES `users_groups` WRITE;
/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
INSERT INTO `users_groups` VALUES (1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,4),(6,6,4),(7,7,4);
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_users_id_permission_id_d7a00931_uniq` (`users_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_users_id_e1ed60a2_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

LOCK TABLES `users_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-02 10:18:31
