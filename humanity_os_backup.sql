-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: humanity_os
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

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
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add users',6,'add_users'),(22,'Can change users',6,'change_users'),(23,'Can delete users',6,'delete_users'),(24,'Can view users',6,'view_users'),(25,'Can add check in check out',7,'add_checkincheckout'),(26,'Can change check in check out',7,'change_checkincheckout'),(27,'Can delete check in check out',7,'delete_checkincheckout'),(28,'Can view check in check out',7,'view_checkincheckout'),(29,'Can add team members',8,'add_teammembers'),(30,'Can change team members',8,'change_teammembers'),(31,'Can delete team members',8,'delete_teammembers'),(32,'Can view team members',8,'view_teammembers'),(33,'Can add teams',9,'add_teams'),(34,'Can change teams',9,'change_teams'),(35,'Can delete teams',9,'delete_teams'),(36,'Can view teams',9,'view_teams'),(37,'Can add projects',10,'add_projects'),(38,'Can change projects',10,'change_projects'),(39,'Can delete projects',10,'delete_projects'),(40,'Can view projects',10,'view_projects'),(41,'Can add task assignments',11,'add_taskassignments'),(42,'Can change task assignments',11,'change_taskassignments'),(43,'Can delete task assignments',11,'delete_taskassignments'),(44,'Can view task assignments',11,'view_taskassignments'),(45,'Can add tasks',12,'add_tasks'),(46,'Can change tasks',12,'change_tasks'),(47,'Can delete tasks',12,'delete_tasks'),(48,'Can view tasks',12,'view_tasks'),(49,'Can add time entries',13,'add_timeentries'),(50,'Can change time entries',13,'change_timeentries'),(51,'Can delete time entries',13,'delete_timeentries'),(52,'Can view time entries',13,'view_timeentries'),(53,'Can add form questions',14,'add_formquestions'),(54,'Can change form questions',14,'change_formquestions'),(55,'Can delete form questions',14,'delete_formquestions'),(56,'Can view form questions',14,'view_formquestions'),(57,'Can add form responses',15,'add_formresponses'),(58,'Can change form responses',15,'change_formresponses'),(59,'Can delete form responses',15,'delete_formresponses'),(60,'Can view form responses',15,'view_formresponses'),(61,'Can add forms',16,'add_forms'),(62,'Can change forms',16,'change_forms'),(63,'Can delete forms',16,'delete_forms'),(64,'Can view forms',16,'view_forms'),(65,'Can add employee kp is',17,'add_employeekpis'),(66,'Can change employee kp is',17,'change_employeekpis'),(67,'Can delete employee kp is',17,'delete_employeekpis'),(68,'Can view employee kp is',17,'view_employeekpis'),(69,'Can add kp is',18,'add_kpis'),(70,'Can change kp is',18,'change_kpis'),(71,'Can delete kp is',18,'delete_kpis'),(72,'Can view kp is',18,'view_kpis'),(73,'Can add team project membership',19,'add_teamprojectmembership'),(74,'Can change team project membership',19,'change_teamprojectmembership'),(75,'Can delete team project membership',19,'delete_teamprojectmembership'),(76,'Can view team project membership',19,'view_teamprojectmembership'),(77,'Can add goals',20,'add_goals'),(78,'Can change goals',20,'change_goals'),(79,'Can delete goals',20,'delete_goals'),(80,'Can view goals',20,'view_goals'),(81,'Can add deadline extension request',21,'add_deadlineextensionrequest'),(82,'Can change deadline extension request',21,'change_deadlineextensionrequest'),(83,'Can delete deadline extension request',21,'delete_deadlineextensionrequest'),(84,'Can view deadline extension request',21,'view_deadlineextensionrequest'),(85,'Can add user face image',22,'add_userfaceimage'),(86,'Can change user face image',22,'change_userfaceimage'),(87,'Can delete user face image',22,'delete_userfaceimage'),(88,'Can view user face image',22,'view_userfaceimage');
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
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checkin_checkout`
--

LOCK TABLES `checkin_checkout` WRITE;
/*!40000 ALTER TABLE `checkin_checkout` DISABLE KEYS */;
INSERT INTO `checkin_checkout` VALUES (59,'2025-05-13 07:56:19.000000','2025-05-13 18:56:40.000000','checkin_images/checkin_lochuynh2_2025-05-13_1747104979.jpg','checkout_images/checkout_lochuynh2_2025-05-13_1747105000.jpg','2025-05-13',9,'16.0514567,108.2244186','16.0514567,108.2244186',1,1),(60,'2025-05-12 06:00:00.000000','2025-05-12 18:00:00.000000','checkin_images/Photo_from_2025-05-06_22-42-31.579917.jpeg','checkout_images/Photo_from_2025-05-06_22-42-27.066309.jpeg','2025-05-12',9,'16.0610909,108.172527','16.0610909,108.172527',1,1),(61,'2025-05-11 06:00:00.000000','2025-05-11 18:00:00.000000','checkin_images/Photo_from_2025-05-11_14-46-52.319794.jpeg','checkout_images/checkin_lochuynh2_2025-05-13_1747102526.jpg','2025-05-11',9,'16.0765337,108.1608241','16.0765337,108.1608241',1,1),(62,'2025-05-10 06:00:00.000000','2025-05-13 18:00:00.000000','checkin_images/Photo_from_2025-05-11_14-46-56_zqnpXyL.381557.jpeg','checkout_images/checkin_lochuynh2_2025-05-13_1747099642.jpg','2025-05-10',9,'16.0770582,108.1369375','16.0770582,108.1369375',1,1);
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
  CONSTRAINT `deadline_extension_requests_requested_by_id_28feab40_fk_users_id` FOREIGN KEY (`requested_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `deadline_extension_requests_task_id_ecbd46d3_fk_tasks_id` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deadline_extension_requests`
--

LOCK TABLES `deadline_extension_requests` WRITE;
/*!40000 ALTER TABLE `deadline_extension_requests` DISABLE KEYS */;
INSERT INTO `deadline_extension_requests` VALUES (1,'2025-04-19 00:00:00.000000','Pending','Đau ốm','2025-04-17 17:51:35.646764',9,10),(2,'2025-04-26 00:00:00.000000','Pending','Task lớn','2025-04-21 16:41:38.932985',9,3),(3,'2025-04-25 00:00:00.000000','Pending','Task khó','2025-04-21 16:48:07.502154',9,3),(4,'2025-04-26 00:00:00.000000','Pending','Task khó','2025-04-24 14:51:01.371068',9,8),(5,'2025-04-26 00:00:00.000000','Pending','Task khó','2025-04-24 15:06:31.917208',9,18);
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
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-04-03 17:04:23.565456','9','lochuynh2',1,'[{\"added\": {}}]',6,1),(2,'2025-04-03 17:04:30.523598','9','lochuynh2',2,'[]',6,1),(3,'2025-04-03 17:08:03.329419','6','Employee Survey - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(4,'2025-04-03 17:08:10.418172','5','API Rate Limiting - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(5,'2025-04-03 17:08:14.788730','4','Mobile Navigation - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(6,'2025-04-03 17:08:18.992385','3','Profile Page UI - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',11,1),(7,'2025-04-03 17:08:35.847684','6','lochuynh2 - API Rate Limiting (2024-04-03 13:00:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(8,'2025-04-03 17:08:41.508856','4','lochuynh2 - Implement Auth API (2024-04-02 14:00:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(9,'2025-04-03 17:08:58.757340','2','lochuynh2 - Design Login Page (2024-04-01 13:30:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(10,'2025-04-03 17:09:04.219206','1','lochuynh2 - Design Login Page (2024-04-01 09:00:00+00:00)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',13,1),(11,'2025-04-03 17:09:35.548623','7','Frontend Team - lochuynh2',1,'[{\"added\": {}}]',8,1),(12,'2025-04-03 17:09:41.446815','4','Backend Team - lochuynh2',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',8,1),(13,'2025-04-03 17:10:14.874719','6','lochuynh2 -> asmith (Employee Satisfaction)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',15,1),(14,'2025-04-03 17:10:19.340035','4','bjohnson -> lochuynh2 (Peer Feedback)',2,'[{\"changed\": {\"fields\": [\"Target user\"]}}]',15,1),(15,'2025-04-03 17:10:27.799472','1','lochuynh2 -> lochuynh (Performance Review)',2,'[{\"changed\": {\"fields\": [\"User\", \"Target user\"]}}]',15,1),(16,'2025-04-03 17:14:01.106418','9','lochuynh2 - Employee Satisfaction (Annual)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',17,1),(17,'2025-04-03 17:14:05.306597','7','lochuynh2 - Code Quality (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',17,1),(18,'2025-04-03 17:14:11.202604','5','lochuynh2 - Task Completion (Quarterly)',2,'[{\"changed\": {\"fields\": [\"User\", \"Evaluation\"]}}]',17,1),(19,'2025-04-03 17:14:15.428983','2','lochuynh2 - Task Completion (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\", \"Evaluation\"]}}]',17,1),(20,'2025-04-03 17:14:20.390616','1','lochuynh2 - Code Quality (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\", \"Evaluation\"]}}]',17,1),(21,'2025-04-14 17:12:51.558591','9','lochuynh2 - 2025-04-14',3,'',7,1),(22,'2025-04-15 17:11:20.161237','8','lochuynh2 - Task Completion (Monthly)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',17,1),(23,'2025-04-15 17:11:33.936359','5','lochuynh2 -> cwilson (Peer Feedback)',2,'[{\"changed\": {\"fields\": [\"User\"]}}]',15,1),(24,'2025-04-15 17:11:50.207150','6','Employee Survey - lochuynh2',2,'[]',11,1),(25,'2025-05-04 13:28:10.867396','8','lochuynh2 - Task Completion (Monthly)',3,'',17,1),(26,'2025-05-04 13:28:25.461512','7','lochuynh2 - Code Quality (Monthly)',3,'',17,1),(27,'2025-05-04 13:28:38.048806','5','lochuynh2 - Task Completion (Quarterly)',3,'',17,1),(28,'2025-05-04 13:28:50.644671','1','lochuynh2 - Code Quality (Monthly)',3,'',17,1),(29,'2025-05-04 13:29:31.399803','2','lochuynh2 - Task Completion (Monthly)',3,'',17,1),(30,'2025-05-06 16:25:45.609018','10','Face image for lochuynh2',3,'',22,1),(31,'2025-05-06 16:25:45.609045','9','Face image for lochuynh2',3,'',22,1),(32,'2025-05-06 16:25:45.609058','8','Face image for lochuynh2',3,'',22,1),(33,'2025-05-06 16:25:45.609067','7','Face image for lochuynh2',3,'',22,1),(34,'2025-05-06 16:25:45.609075','6','Face image for admin',3,'',22,1),(35,'2025-05-06 16:25:45.609084','5','Face image for admin',3,'',22,1),(36,'2025-05-06 16:25:45.609093','4','Face image for admin',3,'',22,1),(37,'2025-05-06 16:25:45.609100','3','Face image for admin',3,'',22,1),(38,'2025-05-06 16:26:13.416697','30','lochuynh2 - 2025-05-06',3,'',7,1),(39,'2025-05-06 16:26:13.416747','29','lochuynh2 - 2025-05-06',3,'',7,1),(40,'2025-05-06 16:26:13.416781','28','lochuynh2 - 2025-05-06',3,'',7,1),(41,'2025-05-06 16:26:13.416801','27','lochuynh2 - 2025-05-06',3,'',7,1),(42,'2025-05-06 16:26:13.416824','26','lochuynh2 - 2025-05-05',3,'',7,1),(43,'2025-05-06 16:26:13.416843','25','lochuynh2 - 2025-05-04',3,'',7,1),(44,'2025-05-06 16:26:13.416864','24','lochuynh2 - 2025-04-27',3,'',7,1),(45,'2025-05-06 16:26:13.416881','23','lochuynh2 - 2025-04-24',3,'',7,1),(46,'2025-05-06 16:26:13.416897','22','lochuynh2 - 2025-04-21',3,'',7,1),(47,'2025-05-06 16:26:13.416913','21','lochuynh2 - 2025-04-17',3,'',7,1),(48,'2025-05-06 16:26:13.416930','20','asmith - 2025-04-15',3,'',7,1),(49,'2025-05-06 16:26:13.416946','19','jdoe - 2025-04-16',3,'',7,1),(50,'2025-05-06 16:26:13.416964','18','lethithao - 2025-04-16',3,'',7,1),(51,'2025-05-06 16:26:13.416980','17','nguyenhoa - 2025-04-16',3,'',7,1),(52,'2025-05-06 16:26:13.416995','16','lochuynh2 - 2025-04-13',3,'',7,1),(53,'2025-05-06 16:26:13.417010','15','lochuynh2 - 2025-04-14',3,'',7,1),(54,'2025-05-06 16:26:13.417025','14','lochuynh2 - 2025-04-15',3,'',7,1),(55,'2025-05-06 16:26:13.417041','13','lochuynh2 - 2025-04-16',3,'',7,1),(56,'2025-05-06 16:26:13.417056','12','lochuynh2 - 2025-04-16',3,'',7,1),(57,'2025-05-06 16:26:13.417070','11','lochuynh2 - 2025-04-15',3,'',7,1),(58,'2025-05-06 16:26:13.417085','10','lochuynh2 - 2025-04-14',3,'',7,1),(59,'2025-05-06 16:26:13.417103','8','lochuynh2 - 2025-04-13',3,'',7,1),(60,'2025-05-06 16:26:13.417118','7','lochuynh2 - 2025-04-13',3,'',7,1),(61,'2025-05-06 16:26:13.417142','6','cwilson - 2024-04-03',3,'',7,1),(62,'2025-05-06 16:26:13.417158','5','asmith - 2024-04-03',3,'',7,1),(63,'2025-05-06 16:26:13.417174','4','cwilson - 2024-04-02',3,'',7,1),(64,'2025-05-06 16:26:13.417192','3','asmith - 2024-04-02',3,'',7,1),(65,'2025-05-06 16:26:13.417208','2','cwilson - 2024-04-01',3,'',7,1),(66,'2025-05-06 16:26:13.417223','1','asmith - 2024-04-01',3,'',7,1),(67,'2025-05-06 16:43:56.908268','36','lochuynh2 - 2025-05-06',3,'',7,1),(68,'2025-05-06 16:43:56.908315','35','lochuynh2 - 2025-05-06',3,'',7,1),(69,'2025-05-06 16:43:56.908340','34','lochuynh2 - 2025-05-06',3,'',7,1),(70,'2025-05-06 16:43:56.908363','33','lochuynh2 - 2025-05-06',3,'',7,1),(71,'2025-05-06 16:43:56.908384','32','lochuynh2 - 2025-05-06',3,'',7,1),(72,'2025-05-06 17:16:53.764867','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(73,'2025-05-06 17:17:15.938011','38','lochuynh2 - 2025-05-06',3,'',7,1),(74,'2025-05-06 17:17:15.938058','37','lochuynh2 - 2025-05-06',3,'',7,1),(75,'2025-05-11 07:31:04.284918','42','lochuynh2 - 2025-05-11',3,'',7,1),(76,'2025-05-11 07:31:04.284993','41','lochuynh2 - 2025-05-11',3,'',7,1),(77,'2025-05-11 07:31:04.285027','40','lochuynh2 - 2025-05-06',3,'',7,1),(78,'2025-05-11 07:31:04.285056','39','lochuynh2 - 2025-05-06',3,'',7,1),(79,'2025-05-11 07:44:17.404574','44','lochuynh2 - 2025-05-11',3,'',7,1),(80,'2025-05-11 07:44:17.404607','43','lochuynh2 - 2025-05-11',3,'',7,1),(81,'2025-05-11 07:46:24.733642','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(82,'2025-05-11 07:47:05.802806','46','lochuynh2 - 2025-05-11',3,'',7,1),(83,'2025-05-11 07:47:21.708680','14','Face image for lochuynh2',3,'',22,1),(84,'2025-05-11 07:47:21.708704','13','Face image for lochuynh2',3,'',22,1),(85,'2025-05-11 07:47:21.708714','12','Face image for lochuynh2',3,'',22,1),(86,'2025-05-11 07:47:21.708722','11','Face image for lochuynh2',3,'',22,1),(87,'2025-05-11 07:48:39.149320','47','lochuynh2 - 2025-05-11',3,'',7,1),(88,'2025-05-12 15:05:45.534563','51','lochuynh2 - 2025-05-12',3,'',7,1),(89,'2025-05-12 15:05:45.534609','50','lochuynh2 - 2025-05-11',3,'',7,1),(90,'2025-05-13 02:06:24.433384','54','lochuynh2 - 2025-05-13',3,'',7,1),(91,'2025-05-13 02:06:24.433472','53','lochuynh2 - 2025-05-13',3,'',7,1),(92,'2025-05-13 02:06:24.433503','52','lochuynh2 - 2025-05-12',3,'',7,1),(93,'2025-05-13 02:15:15.936160','56','lochuynh2 - 2025-05-13',3,'',7,1),(94,'2025-05-13 02:15:15.936205','55','lochuynh2 - 2025-05-13',3,'',7,1),(95,'2025-05-13 02:52:07.883256','57','lochuynh2 - 2025-05-13',3,'',7,1),(96,'2025-05-13 02:52:32.949612','17','Face image for lochuynh2',3,'',22,1),(97,'2025-05-13 02:52:32.949642','16','Face image for lochuynh2',3,'',22,1),(98,'2025-05-13 02:52:32.949655','15','Face image for lochuynh2',3,'',22,1),(99,'2025-05-13 02:55:07.205545','9','lochuynh2',2,'[{\"changed\": {\"fields\": [\"Fixed location\"]}}]',6,1),(100,'2025-05-13 02:55:25.513991','58','lochuynh2 - 2025-05-13',3,'',7,1),(101,'2025-05-13 02:55:56.699558','19','Face image for lochuynh2',3,'',22,1),(102,'2025-05-13 03:23:06.763288','59','lochuynh2 - 2025-05-13',2,'[{\"changed\": {\"fields\": [\"Checkin time\", \"Checkout time\"]}}]',7,1),(103,'2025-05-13 03:25:04.460571','60','lochuynh2 - 2025-05-12',1,'[{\"added\": {}}]',7,1),(104,'2025-05-13 03:25:24.876855','60','lochuynh2 - 2025-05-12',2,'[{\"changed\": {\"fields\": [\"Checkin image\", \"Checkout image\"]}}]',7,1),(105,'2025-05-13 03:26:35.758691','61','lochuynh2 - 2025-05-11',1,'[{\"added\": {}}]',7,1),(106,'2025-05-13 03:27:34.243682','62','lochuynh2 - 2025-05-10',1,'[{\"added\": {}}]',7,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(8,'companies','teammembers'),(9,'companies','teams'),(4,'contenttypes','contenttype'),(14,'evaluations','formquestions'),(15,'evaluations','formresponses'),(16,'evaluations','forms'),(17,'kpis','employeekpis'),(18,'kpis','kpis'),(21,'projects','deadlineextensionrequest'),(10,'projects','projects'),(11,'projects','taskassignments'),(12,'projects','tasks'),(19,'projects','teamprojectmembership'),(13,'projects','timeentries'),(5,'sessions','session'),(7,'users','checkincheckout'),(20,'users','goals'),(22,'users','userfaceimage'),(6,'users','users');
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
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-03 16:42:58.514719'),(2,'contenttypes','0002_remove_content_type_name','2025-04-03 16:42:58.586994'),(3,'auth','0001_initial','2025-04-03 16:42:58.822401'),(4,'auth','0002_alter_permission_name_max_length','2025-04-03 16:42:58.874733'),(5,'auth','0003_alter_user_email_max_length','2025-04-03 16:42:58.879567'),(6,'auth','0004_alter_user_username_opts','2025-04-03 16:42:58.884213'),(7,'auth','0005_alter_user_last_login_null','2025-04-03 16:42:58.888562'),(8,'auth','0006_require_contenttypes_0002','2025-04-03 16:42:58.892022'),(9,'auth','0007_alter_validators_add_error_messages','2025-04-03 16:42:58.896574'),(10,'auth','0008_alter_user_username_max_length','2025-04-03 16:42:58.902523'),(11,'auth','0009_alter_user_last_name_max_length','2025-04-03 16:42:58.908374'),(12,'auth','0010_alter_group_name_max_length','2025-04-03 16:42:58.920381'),(13,'auth','0011_update_proxy_permissions','2025-04-03 16:42:58.926738'),(14,'auth','0012_alter_user_first_name_max_length','2025-04-03 16:42:58.931520'),(15,'users','0001_initial','2025-04-03 16:42:59.329655'),(16,'admin','0001_initial','2025-04-03 16:42:59.447389'),(17,'admin','0002_logentry_remove_auto_add','2025-04-03 16:42:59.454191'),(18,'admin','0003_logentry_add_action_flag_choices','2025-04-03 16:42:59.460970'),(19,'companies','0001_initial','2025-04-03 16:42:59.497142'),(20,'companies','0002_initial','2025-04-03 16:42:59.678994'),(21,'evaluations','0001_initial','2025-04-03 16:42:59.733445'),(22,'evaluations','0002_initial','2025-04-03 16:42:59.947349'),(23,'kpis','0001_initial','2025-04-03 16:42:59.982069'),(24,'kpis','0002_initial','2025-04-03 16:43:00.090318'),(25,'projects','0001_initial','2025-04-03 16:43:00.160287'),(26,'projects','0002_initial','2025-04-03 16:43:00.535039'),(27,'sessions','0001_initial','2025-04-03 16:43:00.568152'),(28,'projects','0003_tasks_is_tracking_tasks_total_time_and_more','2025-04-03 17:42:09.713938'),(29,'users','0002_remove_users_goal_achieved_percentage_and_more','2025-04-07 15:08:17.286273'),(30,'companies','0002_auto_20250407_1550','2025-04-07 15:50:47.323798'),(31,'users','0003_checkincheckout_checkin_location_and_more','2025-04-14 15:52:57.908698'),(32,'users','0004_users_fixed_location','2025-04-14 16:05:53.583579'),(33,'users','0005_users_bio','2025-04-15 14:53:05.896695'),(34,'projects','0004_tasks_notes_alter_tasks_difficulty_and_more','2025-04-17 16:47:13.596815'),(35,'projects','0005_alter_tasks_difficulty','2025-04-17 16:49:13.169538'),(36,'projects','0006_taskassignments_estimated_time_tasks_completed_date_and_more','2025-04-24 15:34:30.197741'),(37,'projects','0007_taskassignments_status','2025-04-24 16:47:07.925918'),(38,'projects','0008_alter_deadlineextensionrequest_requested_deadline_and_more','2025-04-27 02:39:07.574192'),(39,'kpis','0003_kpis_employeekpis_changes','2025-04-27 03:20:44.602956'),(40,'kpis','0004_rename_employee_kpis_user_start_date_idx_employee_kp_user_id_2ebafc_idx_and_more','2025-05-04 13:51:58.202861'),(41,'kpis','0005_rename_employee_kpis_user_start_date_idx_employee_kp_user_id_2ebafc_idx_and_more','2025-05-05 15:17:05.062985'),(42,'users','0006_userfaceimage_checkincheckout_is_valid_checkin_and_more','2025-05-06 16:18:00.028839'),(43,'users','0007_remove_goals_table','2025-05-11 09:06:31.465534'),(44,'users','0008_alter_checkincheckout_options_and_more_fixed','2025-05-11 09:13:22.144257'),(45,'users','0008_alter_checkincheckout_options_and_more','2025-05-11 09:18:21.868523');
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
INSERT INTO `django_session` VALUES ('bbjwqb7r10xuh8jmovwxrjszlyqipof0','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uE0BP:1B6mfkJpkgeeoIJVQNqlfjYMj_gE-g3Lnjw0cH7FhrU','2025-05-25 06:29:07.943494'),('f4pa2ypj8otst8u1iaphssuqmacfsqxc','.eJxVTEsOwiAQvQtrQ4oMIC7d9wxk6EylaiAp7cp499Kki7p5ef-vCLguKayV5zCRuAsvLmcv4vDmvAf0wvwscih5maco94o80ir7Qvx5HN2_g4Q1tbVxoG_R4ahYNxI7D0CRFXlN3japgZwFbGCMQQQcrw7RM1iw1Cnx2wDfrDev:1uBwza:0aPdIYbGvNwTrW2uD84iGeayVnodJmr_VmX3w5Qhszs','2025-05-19 14:40:26.026700'),('luaseydapmy8gj863jljj4v19tzstz5f','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uEeP8:UEITJyFgzaqjdVc6ImlH3oUkK9gP-mB89ZpceL6fkTI','2025-05-27 01:25:58.294813'),('se4gs8th7363u2hqxif1wykkd4b9a66a','.eJxVjEEOwiAQRe_C2hBoB5i6dO8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnEWWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLa-P0vBzu30GhXr41OdCRIo1G4WDQOpiSVjha5dTEmJ01GQicShYg6GByZLI4UuAwZEzi_QHBSzem:1uEUia:S4duw5OPodjNUpijo_eCx217IELY_TOAmx8SR_xClVA','2025-05-26 15:05:24.128586'),('veht0r95ntc0wxytydhqktby6ijlyl17','.eJxVTEsOwiAQvQtrQ4oMIC7d9wxk6EylaiAp7cp499Kki7p5ef-vCLguKayV5zCRuAsvLmcv4vDmvAf0wvwscih5maco94o80ir7Qvx5HN2_g4Q1tbVxoG_R4ahYNxI7D0CRFXlN3japgZwFbGCMQQQcrw7RM1iw1Cnx2wDfrDev:1uBa2b:VkcCoF9AKBIf-M6dOJ1UWHaURZmUIcnD3eUS5XOZ5hI','2025-05-18 14:10:01.324284'),('wp7tho0kymc1cox4q1mlwbqeleqkdpg8','.eJxVTEsOwiAQvQtrQ4oMIC7d9wxk6EylaiAp7cp499Kki7p5ef-vCLguKayV5zCRuAsvLmcv4vDmvAf0wvwscih5maco94o80ir7Qvx5HN2_g4Q1tbVxoG_R4ahYNxI7D0CRFXlN3japgZwFbGCMQQQcrw7RM1iw1Cnx2wDfrDev:1uEUgI:ljB1p-tdpZTkGE-UHw15QyuYa-ss7gCDvxWwBUD76cA','2025-05-26 15:03:02.400468'),('zsk1gvq8f11exq9yqca5fo6p4z0pcsxw','.eJxVjMsOwiAQRf-FtSGFkZdL934DAWaQqoGktCvjv0uTLnR7zrn3zXzY1uK3ToufkV2YY6dfFkN6Ut0FPkK9N55aXZc58j3hh-381pBe16P9Oyihl7EO4LTUIhNEMjGDRpo0nsEOLFCIOAKpcFJkrDIJUlQZg5MOdEKwkn2-4yE3sw:1u4Ml3:pPCBfkL0_54C5U904sDtzNuoDxrgwOPCxLeq9YhAL4Q','2025-04-28 16:34:05.048151');
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
INSERT INTO `employee_kpis` VALUES (3,5,7,'Monthly','Needs Improvement',4,3,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(4,85,80,'Quarterly','Good',5,1,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(6,8,6,'Quarterly','Excellent',5,3,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(9,90,NULL,'Monthly','Not Achieved',9,4,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(10,90,85,'Monthly','Partially Achieved',9,1,94.44444444444444,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(11,95,0,'Monthly','Not Achieved',9,2,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(12,200,180,'Monthly','Partially Achieved',9,6,90,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(13,1000,950,'Monthly','Partially Achieved',9,7,95,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(14,4,3,'Monthly','Partially Achieved',9,8,75,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(15,5,0,'Monthly','Not Achieved',9,3,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(16,200,190,'Monthly','Achieved',10,6,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(17,1000,900,'Monthly','Not Achieved',11,7,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(18,90,88,'Monthly','Achieved',3,1,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(19,95,92,'Monthly','Achieved',4,2,0,'2025-04-27 03:20:44.341389','2025-05-27 03:20:43.877419'),(20,10,8,'Monthly','Partially Achieved',9,9,80,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(21,160,150,'Monthly','Partially Achieved',9,10,93.75,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(22,5,4,'Monthly','Achieved',9,11,80,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(23,10,9,'Monthly','Achieved',9,12,90,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000'),(24,100,95,'Monthly','Achieved',9,13,95,'2025-05-01 00:00:00.000000','2025-05-31 00:00:00.000000');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form_questions`
--

LOCK TABLES `form_questions` WRITE;
/*!40000 ALTER TABLE `form_questions` DISABLE KEYS */;
INSERT INTO `form_questions` VALUES (1,'Đánh giá khả năng hợp tác của đồng nghiệp',1,'rating',5),(2,'Điểm mạnh của đồng nghiệp là gì?',1,'text',NULL),(3,'Hiệu suất làm việc của nhân viên?',2,'rating',5),(4,'Khu vực cần cải thiện?',2,'text',NULL),(5,'Mức độ hỗ trợ từ team?',3,'rating',5),(6,'Gợi ý cải thiện teamwork?',3,'text',NULL),(8,'Bạn đánh giá thế nào về tinh thần hợp tác của đồng nghiệp?',1,'rating',5),(9,'Ý kiến đóng góp cho đồng nghiệp?',1,'text',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forms`
--

LOCK TABLES `forms` WRITE;
/*!40000 ALTER TABLE `forms` DISABLE KEYS */;
INSERT INTO `forms` VALUES (1,'Peer Feedback Q1 2025','peer','Quarterly','2025-06-30 23:59:59','open'),(2,'Performance Review Q1 2025','review','Quarterly','2025-06-30 23:59:59','open'),(3,'Team Feedback May 2025','feedback','Monthly','2025-05-31 23:59:59','open'),(5,'Peer Review Tháng 5','peer','monthly','2025-05-31 00:00:00','open');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kpis`
--

LOCK TABLES `kpis` WRITE;
/*!40000 ALTER TABLE `kpis` DISABLE KEYS */;
INSERT INTO `kpis` VALUES (1,'Code Quality','Measure of code quality based on static analysis','Quantitative',1,'score',1),(2,'Task Completion','Percentage of tasks completed on time','Quantitative',1,'score',1),(3,'Bug Rate','Number of bugs per 1000 lines of code','Quantitative',2,'bugs',1),(4,'Employee Satisfaction','Score from employee satisfaction surveys','Quantitative',1,'percent',1),(5,'Feature Delivery','Number of features delivered per sprint','Quantitative',2,'features',1),(6,'API Response Time','Average response time of API endpoints.','Quantitative',3,'ms',1),(7,'User Engagement','Number of active users interacting with the app.','Quantitative',2,'users',1),(8,'Deployment Frequency','Number of deployments per month.','Quantitative',1,'deployments',1),(9,'Số lượng task hoàn thành','Số lượng task hoàn thành trong tháng','Quantitative',1,'task',1),(10,'Số giờ làm việc','Tổng số giờ làm việc thực tế','Quantitative',2,'hour',1),(11,'Thái độ làm việc','Đánh giá thái độ làm việc của nhân viên','Qualitative',1,'score',1),(12,'Chất lượng code','Đánh giá chất lượng code qua review','Quality',3,'score',1),(13,'Hiệu suất xử lý task','Tỷ lệ hoàn thành task đúng hạn','Efficiency',2,'%',1);
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
INSERT INTO `projects` VALUES (1,'Customer Portal','New customer self-service portal','2024-01-20 00:00:00.000000','2024-06-30 00:00:00.000000',2),(2,'Mobile App','Company mobile application','2024-02-01 00:00:00.000000','2024-08-15 00:00:00.000000',2),(3,'API Gateway','Centralized API management system','2024-03-01 00:00:00.000000','2024-07-31 00:00:00.000000',3),(4,'Employee Engagement','Programs to improve employee satisfaction','2024-01-01 00:00:00.000000','2024-12-31 00:00:00.000000',7),(5,'Inventory Management System','Develop a system for tracking inventory and stock levels.','2025-04-01 00:00:00.000000','2025-07-31 00:00:00.000000',2),(6,'Customer Support Chatbot','Build an AI-powered chatbot for customer support.','2025-04-10 00:00:00.000000','2025-06-30 00:00:00.000000',2),(7,'Website Redesign','Thiết kế lại giao diện website','2025-05-01 00:00:00.000000','2025-08-01 00:00:00.000000',9),(8,'CRM System','Xây dựng hệ thống quản lý khách hàng','2025-06-01 00:00:00.000000','2025-12-01 00:00:00.000000',9);
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_assignments_task_id_user_id_013197e5_uniq` (`task_id`,`user_id`),
  KEY `task_assignments_user_id_8237dbae_fk_users_id` (`user_id`),
  CONSTRAINT `task_assignments_task_id_dbef494b_fk_tasks_id` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `task_assignments_user_id_8237dbae_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_assignments`
--

LOCK TABLES `task_assignments` WRITE;
/*!40000 ALTER TABLE `task_assignments` DISABLE KEYS */;
INSERT INTO `task_assignments` VALUES (1,4,1,NULL,'To-do'),(2,6,2,NULL,'To-do'),(3,9,3,NULL,'To-do'),(4,9,4,NULL,'To-do'),(5,9,5,NULL,'To-do'),(6,9,6,NULL,'Completed'),(7,9,7,NULL,'To-do'),(8,9,8,4,'To-do'),(9,9,9,NULL,'To-do'),(10,9,10,NULL,'In progress'),(11,9,11,NULL,'To-do'),(12,9,12,NULL,'To-do'),(13,9,14,NULL,'To-do'),(14,9,15,NULL,'To-do'),(15,9,16,NULL,'To-do'),(16,9,17,NULL,'To-do'),(17,9,18,NULL,'Completed'),(18,9,20,NULL,'To-do'),(19,3,7,NULL,'To-do'),(20,10,8,NULL,'To-do'),(21,4,9,NULL,'To-do'),(22,11,10,NULL,'To-do'),(23,5,13,NULL,'To-do'),(24,10,14,NULL,'To-do'),(25,10,15,NULL,'To-do'),(26,11,19,NULL,'To-do'),(27,11,21,NULL,'To-do'),(28,9,22,10,'To-do'),(29,9,23,15,'To-do'),(30,9,24,12,'To-do'),(31,9,25,8,'To-do');
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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Design Login Page','Create UI for login page with responsive design','2024-04-15 00:00:00.000000','In Progress','Medium',8,'https://github.com/humanityos/customer-portal/pull/12',1,0,33.5,NULL,NULL,'2024-04-01 00:00:00.000000'),(2,'Implement Auth API','Develop authentication API endpoints','2024-04-10 00:00:00.000000','Completed','High',12,'https://github.com/humanityos/customer-portal/pull/8',1,0,0,NULL,NULL,NULL),(3,'Profile Page UI','Design user profile page','2024-04-20 00:00:00.000000','Not Started','Easy',5,'https://github.com/loochuynhh/humanity_os/issues/10',1,0,0,'àgasg',NULL,NULL),(4,'Mobile Navigation','Implement navigation for mobile app','2024-05-01 00:00:00.000000','Late','Medium',10,'https://github.com/humanityos/mobile-app/pull/3',2,1,0,NULL,NULL,'2024-04-03 10:00:00.000000'),(5,'API Rate Limiting','Implement rate limiting for API gateway','2024-04-30 00:00:00.000000','Completed','High',15,'https://github.com/humanityos/api-gateway/pull/5',3,0,30.683333333333334,NULL,NULL,'2024-04-03 13:00:00.000000'),(6,'Employee Survey','Conduct Q2 employee satisfaction survey','2024-06-30 00:00:00.000000','Completed','Low',20,NULL,4,0,33.3,NULL,'2025-04-24 00:00:00.000000','2025-04-21 15:37:00.000000'),(7,'Implement User Dashboard','Create dashboard for user account management.','2025-04-20 00:00:00.000000','Late','Medium',10,NULL,1,0,3,NULL,NULL,'2025-04-16 08:00:00.000000'),(8,'Add Two-Factor Authentication 2','Integrate 2FA for user login.','2025-04-25 00:00:00.000000','Completed','Medium',6,'https://github.com/loochuynhh/humanity_os/issues/10',1,0,34.016666666666666,'Task mới có vẻ khó hơn task cũ',NULL,'2025-04-16 01:04:00.000000'),(9,'Push Notification System','Implement push notifications for app.','2025-04-22 00:00:00.000000','To-do','Medium',8,NULL,2,0,4,NULL,NULL,'2025-04-14 14:00:00.000000'),(10,'Offline Mode Support','Add offline mode for app.','2025-04-30 00:00:00.000000','In progress','High',15,NULL,2,0,48.8,NULL,NULL,'2025-04-15 09:00:00.000000'),(11,'API Documentation','Write Swagger documentation for APIs.','2025-04-18 00:00:00.000000','Late','Low',5,NULL,3,0,30.533333333333335,NULL,NULL,'2025-04-14 09:00:00.000000'),(12,'Rate Limiting Optimization','Optimize rate limiting for high traffic.','2025-04-28 00:00:00.000000','In progress','High',10,NULL,3,0,4,NULL,NULL,'2025-04-13 09:00:00.000000'),(13,'Survey Analysis Tool','Build tool to analyze survey results.','2025-04-25 00:00:00.000000','To-do','Medium',8,NULL,4,0,0,NULL,NULL,NULL),(14,'Stock Tracking API','Develop API for real-time stock tracking.','2025-04-20 00:00:00.000000','To-do','Medium',10,NULL,5,0,3,NULL,NULL,'2025-04-15 09:00:00.000000'),(15,'Inventory Dashboard','Create dashboard for inventory overview.','2025-04-30 00:00:00.000000','In progress','Medium',12,NULL,5,0,11.000902313055555,NULL,NULL,'2025-04-12 09:00:00.000000'),(16,'Barcode Scanner Integration','Integrate barcode scanner for stock entry.','2025-05-05 00:00:00.000000','To-do','Easy',15,'https://github.com/loochuynhh/humanity_os/issues/10',5,0,13.016666666666667,'',NULL,'2025-04-27 02:51:00.000000'),(17,'Stock Alert System','Implement alerts for low stock levels.','2025-04-25 00:00:00.000000','To-do','Medium',7,NULL,5,0,0,NULL,NULL,NULL),(18,'Chatbot NLP Model','Train NLP model for chatbot responses.','2025-04-22 00:00:00.000000','Completed','High',20,NULL,6,0,9,NULL,'2025-04-24 00:00:00.000000','2025-04-11 08:00:00.000000'),(19,'Chatbot UI','Design UI for chatbot integration.','2025-04-28 00:00:00.000000','To-do','Medium',8,NULL,6,0,0,NULL,NULL,NULL),(20,'Integration with CRM','Integrate chatbot with CRM system.','2025-05-01 00:00:00.000000','To-do','High',12,NULL,6,0,0,NULL,NULL,NULL),(21,'Chatbot Testing','Perform end-to-end testing for chatbot.','2025-05-10 00:00:00.000000','To-do','Medium',10,NULL,6,0,0,NULL,NULL,NULL),(22,'Thiết kế trang chủ','Thiết kế UI/UX cho trang chủ','2025-05-15 00:00:00.000000','To-do','Medium',10,NULL,7,0,3,NULL,NULL,'2025-05-02 09:00:00.000000'),(23,'Tối ưu tốc độ tải trang','Cải thiện tốc độ tải trang web','2025-06-01 00:00:00.000000','To-do','Hard',15,'https://github.com/loochuynhh/humanity_os/issues/10',7,0,4,'',NULL,'2025-05-03 13:00:00.000000'),(24,'Tạo module khách hàng','Xây dựng module quản lý khách hàng','2025-06-15 00:00:00.000000','To-do','Medium',12,'https://github.com/loochuynhh/humanity_os/issues/10',8,0,2,'',NULL,'2025-06-02 09:00:00.000000'),(25,'Tích hợp email marketing','Tích hợp chức năng gửi email marketing','2025-07-01 00:00:00.000000','To-do','Easy',8,'https://github.com/loochuynhh/humanity_os/issues/10',8,0,4,'',NULL,'2025-06-05 14:00:00.000000');
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `team_project_memberships_project_id_user_id_126ee7ca_uniq` (`project_id`,`user_id`),
  KEY `team_project_memberships_user_id_b2a800f3_fk_users_id` (`user_id`),
  CONSTRAINT `team_project_memberships_project_id_c6bb2041_fk_projects_id` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `team_project_memberships_user_id_b2a800f3_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team_project_memberships`
--

LOCK TABLES `team_project_memberships` WRITE;
/*!40000 ALTER TABLE `team_project_memberships` DISABLE KEYS */;
INSERT INTO `team_project_memberships` VALUES (1,'2025-03-15 00:00:00.000000',1,9),(2,'2025-04-01 00:00:00.000000',2,9),(3,'2025-03-20 00:00:00.000000',3,9),(4,'2025-04-01 00:00:00.000000',5,9),(5,'2025-04-01 00:00:00.000000',5,10),(6,'2025-04-01 00:00:00.000000',5,2),(7,'2025-04-10 00:00:00.000000',6,9),(8,'2025-04-10 00:00:00.000000',6,11),(9,'2025-04-10 00:00:00.000000',6,2),(10,'2025-03-15 00:00:00.000000',1,3),(11,'2025-04-01 00:00:00.000000',2,4),(12,'2025-03-20 00:00:00.000000',3,5);
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
  `task_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `duration` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `time_entries_task_id_9120f577_fk_tasks_id` (`task_id`),
  KEY `time_entries_user_id_9ab39a69_fk_users_id` (`user_id`),
  CONSTRAINT `time_entries_task_id_9120f577_fk_tasks_id` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `time_entries_user_id_9ab39a69_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_entries`
--

LOCK TABLES `time_entries` WRITE;
/*!40000 ALTER TABLE `time_entries` DISABLE KEYS */;
INSERT INTO `time_entries` VALUES (1,'2024-04-01 09:00:00.000000','2024-04-01 12:30:00.000000',1,9,NULL),(2,'2024-04-23 13:30:00.000000','2024-04-24 23:00:00.000000',1,9,33.5),(3,'2024-04-02 09:15:00.000000','2024-04-02 11:45:00.000000',2,6,NULL),(4,'2024-04-02 14:00:00.000000','2024-04-02 17:30:00.000000',2,9,NULL),(5,'2024-04-03 10:00:00.000000','2024-04-03 12:00:00.000000',4,4,NULL),(6,'2024-04-03 13:00:00.000000','2024-04-04 17:41:00.000000',5,9,28.683333333333334),(7,'2025-04-16 08:00:00.000000','2025-04-16 11:00:00.000000',8,9,3),(8,'2025-04-16 13:00:00.000000','2025-04-16 15:00:00.000000',12,9,2),(9,'2025-04-16 09:00:00.000000','2025-04-16 13:00:00.000000',15,9,4),(10,'2025-04-15 08:00:00.000000','2025-04-15 13:00:00.000000',18,9,5),(11,'2025-04-15 14:00:00.000000','2025-04-15 16:00:00.000000',5,9,2),(12,'2025-04-14 09:00:00.000000','2025-04-14 13:30:00.000000',11,9,4.5),(13,'2025-04-14 14:00:00.000000','2025-04-14 16:00:00.000000',9,9,2),(14,'2025-04-16 01:04:00.000000','2025-04-17 05:05:00.000000',8,9,28.016666666666666),(15,'2025-04-12 09:00:00.000000','2025-04-12 12:00:00.000000',15,9,3),(16,'2025-04-11 08:00:00.000000','2025-04-11 12:00:00.000000',18,9,4),(17,'2025-04-16 08:00:00.000000','2025-04-16 11:00:00.000000',8,10,3),(18,'2025-04-15 09:00:00.000000','2025-04-15 12:00:00.000000',14,10,3),(19,'2025-04-16 08:00:00.000000','2025-04-16 10:00:00.000000',19,11,2),(20,'2025-04-15 09:00:00.000000','2025-04-15 12:00:00.000000',10,11,3),(21,'2025-04-16 08:00:00.000000','2025-04-16 11:00:00.000000',7,3,3),(22,'2025-04-15 08:00:00.000000','2025-04-15 10:00:00.000000',9,4,2),(23,'2025-04-16 09:00:00.000000','2025-04-16 11:00:00.000000',13,5,2),(24,'2025-04-14 08:00:00.000000','2025-04-14 12:00:00.000000',15,10,4),(25,'2025-04-14 09:00:00.000000','2025-04-14 11:00:00.000000',19,11,2),(26,'2025-04-13 09:00:00.000000','2025-04-13 11:00:00.000000',12,9,2),(27,'2025-04-17 17:41:05.479449','2025-04-17 17:41:08.727776',15,9,0.0009023130555555556),(28,'2025-04-19 17:47:00.000000','2025-04-20 19:49:00.000000',11,9,26.033333333333335),(29,'2025-04-18 17:49:00.000000','2025-04-20 15:37:00.000000',10,9,45.8),(30,'2025-04-21 15:37:00.000000','2025-04-23 00:55:00.000000',6,9,33.3),(31,'2025-04-27 02:51:00.000000','2025-04-27 15:52:00.000000',16,9,13.016666666666667),(32,'2025-05-04 07:47:09.034966',NULL,4,9,NULL),(33,'2025-05-02 09:00:00.000000','2025-05-02 12:00:00.000000',22,9,3),(34,'2025-05-03 13:00:00.000000','2025-05-03 17:00:00.000000',23,9,4),(35,'2025-06-02 09:00:00.000000','2025-06-02 11:00:00.000000',24,9,2),(36,'2025-06-05 14:00:00.000000','2025-06-05 18:00:00.000000',25,9,4);
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_face_images`
--

LOCK TABLES `user_face_images` WRITE;
/*!40000 ALTER TABLE `user_face_images` DISABLE KEYS */;
INSERT INTO `user_face_images` VALUES (18,'face_images/Photo_from_2025-05-11_14-46-56.381557.jpeg','2025-05-11 07:47:51.535213',9),(20,'face_images/Photo_from_2025-05-11_14-46-49_1h1xvj7.975635.jpeg','2025-05-13 02:53:19.270630',9),(21,'face_images/Photo_from_2025-05-11_14-46-49_kjXhXdz.975635.jpeg','2025-05-13 02:53:27.421460',9),(22,'face_images/checkin_lochuynh2_2025-05-13_1747102526.jpg','2025-05-13 02:53:40.414752',9),(23,'face_images/checkin_lochuynh2_2025-05-13_1747102005_8x0bZSe.jpg','2025-05-13 02:53:47.321307',9),(24,'face_images/checkin_lochuynh2_2025-05-12_1747062207.jpg','2025-05-13 02:53:55.807615',9),(25,'face_images/checkin_lochuynh2_2025-05-13_1747099642.jpg','2025-05-13 02:54:02.948161',9),(26,'face_images/checkin_lochuynh2_2025-05-12_1747062364.jpg','2025-05-13 02:54:10.947019',9),(27,'face_images/Photo_from_2025-05-13_09-55-36.471145.jpeg','2025-05-13 02:56:09.456998',9),(28,'face_images/Photo_from_2025-05-11_14-46-56_EArmSkd.381557.jpeg','2025-05-13 06:22:35.598192',9);
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
INSERT INTO `users` VALUES (1,'pbkdf2_sha256$870000$d6Yw3mN6tleKbshH6CFf6v$en2KQPcVFORynDRAITeT+UIVpPhyqRYlOv2H95wIq7c=','2025-05-13 01:25:58.291763',1,'lochuynh','','','lochuynh@gmail.com',1,1,'2025-04-03 16:44:28.565953','',NULL,'Employee',NULL,'Active',NULL,NULL,NULL),(2,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 10:00:00.000000',1,'admin','System','Admin','admin@humanityos.com',1,1,'2024-01-01 09:00:00.000000','avatars/admin.jpg','+1234567890','Administrator','IT','Active','2024-01-01',NULL,NULL),(3,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 09:30:00.000000',0,'jdoe','John','Doe','jdoe@humanityos.com',1,1,'2024-01-15 09:00:00.000000','avatars/jdoe.jpg','+1987654321','Project Manager','Development','Active','2024-01-15',NULL,NULL),(4,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-02 17:45:00.000000',0,'asmith','Alice','Smith','asmith@humanityos.com',1,1,'2024-02-01 09:00:00.000000','avatars/asmith.jpg','+1122334455','Team Lead','Development','Active','2024-02-01',NULL,NULL),(5,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 08:15:00.000000',0,'bjohnson','Bob','Johnson','bjohnson@humanityos.com',0,1,'2024-02-15 09:00:00.000000','avatars/bjohnson.jpg','+1555666777','Senior Developer','Development','Active','2024-02-15',NULL,NULL),(6,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-01 16:30:00.000000',0,'cwilson','Carol','Wilson','cwilson@humanityos.com',0,1,'2024-03-01 09:00:00.000000','avatars/cwilson.jpg','+1444333222','Developer','Development','Active','2024-03-01',NULL,NULL),(7,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-04-03 10:20:00.000000',0,'dlee','David','Lee','dlee@humanityos.com',0,1,'2024-03-15 09:00:00.000000','avatars/dlee.jpg','+1666777888','Developer','Development','Active','2024-03-15',NULL,NULL),(8,'pbkdf2_sha256$600000$N2gFq3Z4X6k8Q1wP9rL7tT$9mZR5cV2bY7xW1nK3pD8qS0oU4iE6lH9jG5fM=','2025-03-30 14:10:00.000000',0,'emiller','Eva','Miller','emiller@humanityos.com',1,1,'2024-01-10 09:00:00.000000','avatars/emiller.jpg','+1777888999','HR Manager','Human Resources','Active','2024-01-10',NULL,NULL),(9,'pbkdf2_sha256$870000$kQYWvrkpUfX7syiBBlg99a$5nBwmwYS+ZYnApRdUVTzMV242gk4M2JeE49VkJFh0Tc=','2025-05-12 15:03:02.000000',0,'lochuynh2','Lộc','Huỳnh','lochuynh03012003@gmail.com',0,1,'2025-04-03 17:04:23.000000','avatars/3b4.png','0342063017','Employee','Dev ruby  rails','Active','2024-02-16','16.0514567,108.22442','Bug creater '),(10,'pbkdf2_sha256$720000$abc$hashed_password',NULL,0,'nguyenhoa','Hoa','Nguyễn','nguyenhoa@humanityos.com',0,1,'2025-03-01 08:00:00.000000',NULL,'0901234571','Employee','Development','Active','2025-03-01','Hanoi','Backend Developer'),(11,'pbkdf2_sha256$720000$abc$hashed_password',NULL,0,'lethithao','Thảo','Lê','lethithao@humanityos.com',0,1,'2025-03-01 08:00:00.000000',NULL,'0901234572','Employee','Design','Active','2025-03-01','Hanoi','UI Designer');
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

-- Dump completed on 2025-05-13 22:18:24
