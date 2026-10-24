-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: scas_db
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `scas_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `scas_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `scas_db`;

--
-- Table structure for table `scas_attendance`
--

DROP TABLE IF EXISTS `scas_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `scas_attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`),
  CONSTRAINT `scas_attendance_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_attendance`
--

LOCK TABLES `scas_attendance` WRITE;
/*!40000 ALTER TABLE `scas_attendance` DISABLE KEYS */;
INSERT INTO `scas_attendance` VALUES (1,1,1,'2026-09-25','Present'),(2,2,1,'2026-09-25','Absent'),(3,1,2,'2026-09-25','Present'),(4,2,2,'2026-09-25','Present'),(5,1,1,'2026-09-24','Present'),(6,2,1,'2026-09-24','Present'),(7,1,2,'2026-09-24','Absent'),(8,2,2,'2026-09-24','Present'),(9,1,1,'2026-09-23','Present'),(10,2,1,'2026-09-23','Present'),(11,1,2,'2026-09-23','Present'),(12,2,2,'2026-09-23','Present'),(13,1,1,'2026-09-22','Present'),(14,2,1,'2026-09-22','Absent'),(15,1,2,'2026-09-22','Present'),(16,2,2,'2026-09-22','Present'),(17,1,1,'2026-09-21','Present'),(18,2,1,'2026-09-21','Present'),(19,1,2,'2026-09-21','Present'),(20,2,2,'2026-09-21','Present'),(21,1,1,'2026-09-18','Present'),(22,2,1,'2026-09-18','Present'),(23,1,2,'2026-09-18','Present'),(24,2,2,'2026-09-18','Present'),(25,1,1,'2026-09-17','Present'),(26,2,1,'2026-09-17','Present'),(27,1,2,'2026-09-17','Present'),(28,2,2,'2026-09-17','Present'),(29,1,1,'2026-09-16','Present'),(30,2,1,'2026-09-16','Absent'),(31,1,2,'2026-09-16','Absent'),(32,2,2,'2026-09-16','Present'),(33,1,1,'2026-09-15','Present'),(34,2,1,'2026-09-15','Present'),(35,1,2,'2026-09-15','Present'),(36,2,2,'2026-09-15','Present'),(37,1,1,'2026-09-14','Present'),(38,2,1,'2026-09-14','Present'),(39,1,2,'2026-09-14','Present'),(40,2,2,'2026-09-14','Present');
/*!40000 ALTER TABLE `scas_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_batches`
--

DROP TABLE IF EXISTS `scas_batches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_batches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `course_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `scas_batches_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `scas_courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_batches`
--

LOCK TABLES `scas_batches` WRITE;
/*!40000 ALTER TABLE `scas_batches` DISABLE KEYS */;
INSERT INTO `scas_batches` VALUES (1,'MCA 2024-2026',1,2026);
/*!40000 ALTER TABLE `scas_batches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_courses`
--

DROP TABLE IF EXISTS `scas_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_courses`
--

LOCK TABLES `scas_courses` WRITE;
/*!40000 ALTER TABLE `scas_courses` DISABLE KEYS */;
INSERT INTO `scas_courses` VALUES (1,'Master of Computer Applications','MCA','Post-graduate program in Computer Applications and Software Engineering.');
/*!40000 ALTER TABLE `scas_courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_faculty_profiles`
--

DROP TABLE IF EXISTS `scas_faculty_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_faculty_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `department` varchar(100) NOT NULL,
  `designation` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `scas_faculty_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `scas_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_faculty_profiles`
--

LOCK TABLES `scas_faculty_profiles` WRITE;
/*!40000 ALTER TABLE `scas_faculty_profiles` DISABLE KEYS */;
INSERT INTO `scas_faculty_profiles` VALUES (1,2,'Computer Applications','Professor'),(2,3,'Computer Applications','Associate Professor');
/*!40000 ALTER TABLE `scas_faculty_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_fee_payments`
--

DROP TABLE IF EXISTS `scas_fee_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_fee_payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `receipt_no` varchar(50) DEFAULT NULL,
  `transaction_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `receipt_no` (`receipt_no`),
  UNIQUE KEY `transaction_id` (`transaction_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `scas_fee_payments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_fee_payments`
--

LOCK TABLES `scas_fee_payments` WRITE;
/*!40000 ALTER TABLE `scas_fee_payments` DISABLE KEYS */;
INSERT INTO `scas_fee_payments` VALUES (1,1,65000,'2026-09-28 14:48:40','Pending','REC-MCA24004-CSV',NULL),(2,2,65000,'2026-09-28 14:48:40','Paid','REC-MCA24005-CSV','TXN-984712-SUCCESS');
/*!40000 ALTER TABLE `scas_fee_payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_leave_applications`
--

DROP TABLE IF EXISTS `scas_leave_applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_leave_applications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `leave_type` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` text NOT NULL,
  `status` varchar(20) NOT NULL,
  `applied_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `scas_leave_applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `scas_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_leave_applications`
--

LOCK TABLES `scas_leave_applications` WRITE;
/*!40000 ALTER TABLE `scas_leave_applications` DISABLE KEYS */;
INSERT INTO `scas_leave_applications` VALUES (1,4,'Sick Leave','2026-09-30','2026-10-01','Medical appointment and dental procedure.','Pending','2026-09-28 14:48:40');
/*!40000 ALTER TABLE `scas_leave_applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_marks`
--

DROP TABLE IF EXISTS `scas_marks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_marks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `exam_type` varchar(30) NOT NULL,
  `marks_obtained` float NOT NULL,
  `max_marks` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `scas_marks_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`),
  CONSTRAINT `scas_marks_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_marks`
--

LOCK TABLES `scas_marks` WRITE;
/*!40000 ALTER TABLE `scas_marks` DISABLE KEYS */;
INSERT INTO `scas_marks` VALUES (1,1,1,'Midterm 1',26,30),(2,1,1,'Midterm 2',27.5,30),(3,1,1,'Final Exam',62,70),(4,1,1,'Assignment',19,20),(5,1,2,'Midterm 1',24,30),(6,1,2,'Midterm 2',25,30),(7,1,2,'Final Exam',58,70),(8,1,2,'Assignment',18,20),(9,2,1,'Midterm 1',28,30),(10,2,1,'Midterm 2',29,30),(11,2,1,'Final Exam',65,70),(12,2,1,'Assignment',20,20),(13,2,2,'Midterm 1',22,30),(14,2,2,'Midterm 2',23.5,30),(15,2,2,'Final Exam',54,70),(16,2,2,'Assignment',17,20);
/*!40000 ALTER TABLE `scas_marks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_results`
--

DROP TABLE IF EXISTS `scas_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `semester` int(11) NOT NULL,
  `marks_obtained` float NOT NULL,
  `max_marks` float NOT NULL,
  `credits` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `scas_results_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`),
  CONSTRAINT `scas_results_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_results`
--

LOCK TABLES `scas_results` WRITE;
/*!40000 ALTER TABLE `scas_results` DISABLE KEYS */;
INSERT INTO `scas_results` VALUES (1,1,1,1,88,100,4),(2,1,2,1,82,100,4),(3,2,1,1,92,100,4),(4,2,2,1,76,100,4);
/*!40000 ALTER TABLE `scas_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_schedules`
--

DROP TABLE IF EXISTS `scas_schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_schedules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` int(11) NOT NULL,
  `batch_id` int(11) NOT NULL,
  `day_of_week` varchar(20) NOT NULL,
  `start_time` varchar(10) NOT NULL,
  `end_time` varchar(10) NOT NULL,
  `room` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  KEY `batch_id` (`batch_id`),
  CONSTRAINT `scas_schedules_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`),
  CONSTRAINT `scas_schedules_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `scas_batches` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_schedules`
--

LOCK TABLES `scas_schedules` WRITE;
/*!40000 ALTER TABLE `scas_schedules` DISABLE KEYS */;
INSERT INTO `scas_schedules` VALUES (1,1,1,'Monday','09:00 AM','10:30 AM','Lab 3'),(2,2,1,'Monday','11:00 AM','12:30 PM','Room 204'),(3,1,1,'Wednesday','10:00 AM','11:30 AM','Lab 3'),(4,2,1,'Friday','02:00 PM','03:30 PM','Room 204');
/*!40000 ALTER TABLE `scas_schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_student_profiles`
--

DROP TABLE IF EXISTS `scas_student_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_student_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `roll_no` varchar(30) NOT NULL,
  `batch_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `roll_no` (`roll_no`),
  KEY `user_id` (`user_id`),
  KEY `batch_id` (`batch_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `scas_student_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `scas_users` (`id`),
  CONSTRAINT `scas_student_profiles_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `scas_batches` (`id`),
  CONSTRAINT `scas_student_profiles_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `scas_courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_student_profiles`
--

LOCK TABLES `scas_student_profiles` WRITE;
/*!40000 ALTER TABLE `scas_student_profiles` DISABLE KEYS */;
INSERT INTO `scas_student_profiles` VALUES (1,4,'MCA24004',1,1,'7016429311'),(2,5,'MCA24005',1,1,'9898510712');
/*!40000 ALTER TABLE `scas_student_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_subjects`
--

DROP TABLE IF EXISTS `scas_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL,
  `course_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `course_id` (`course_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `scas_subjects_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `scas_courses` (`id`),
  CONSTRAINT `scas_subjects_ibfk_2` FOREIGN KEY (`faculty_id`) REFERENCES `scas_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_subjects`
--

LOCK TABLES `scas_subjects` WRITE;
/*!40000 ALTER TABLE `scas_subjects` DISABLE KEYS */;
INSERT INTO `scas_subjects` VALUES (1,'Theory of Computation','MCA-104',1,2),(2,'Compiler Design','MCA-105',1,3);
/*!40000 ALTER TABLE `scas_subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_test_assessments`
--

DROP TABLE IF EXISTS `scas_test_assessments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_test_assessments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `unit_number` int(11) NOT NULL,
  `unit_title` varchar(200) NOT NULL,
  `test_type` varchar(20) NOT NULL,
  `score` float NOT NULL,
  `total_questions` int(11) DEFAULT NULL,
  `percentage` float NOT NULL,
  `mastery_level` varchar(50) DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `scas_test_assessments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`),
  CONSTRAINT `scas_test_assessments_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_test_assessments`
--

LOCK TABLES `scas_test_assessments` WRITE;
/*!40000 ALTER TABLE `scas_test_assessments` DISABLE KEYS */;
/*!40000 ALTER TABLE `scas_test_assessments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scas_users`
--

DROP TABLE IF EXISTS `scas_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scas_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(120) NOT NULL,
  `role` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scas_users`
--

LOCK TABLES `scas_users` WRITE;
/*!40000 ALTER TABLE `scas_users` DISABLE KEYS */;
INSERT INTO `scas_users` VALUES (1,'admin','scrypt:32768:8:1$udiYstkQox1vyjx5$052ca134092155668caa867a947e813fa5ae20f025148f8b513345dfd5a2ebf8917c06605ae7a69567f3818fdaa2fca97f3d9b22b92cec87d581dc9ec53b8291','admin@college.edu','admin','Dean System Administrator','2026-09-28 14:48:39'),(2,'cdpatel@college.edu','scrypt:32768:8:1$446noUWzXnjBqlzD$e0de66de6165de37e08b673a158e6bd3428d01ee221a0503a0229c37a8431e6f83e217e48e79bf2caed40ef1bb30b9fc15ca5614dc2bd8a04b8f83a2c8db2a70','cdpatel@college.edu','faculty','Dr. CD Patel','2026-09-28 14:48:39'),(3,'sanjaybhai@college.edu','scrypt:32768:8:1$KE6M9O5idb3GpjDw$de9192d6bd19b86baa33d3ab0aa0a6697def6ca2630e396683446c1f901f4e10dd58726a0c8ed4998009741e436633463fbd8a403f58f6885a29b50a3098b597','sanjaybhai@college.edu','faculty','Prof. sanjaybhai patel','2026-09-28 14:48:40'),(4,'goswami@college.edu','scrypt:32768:8:1$KeVPciYXhm0FyGfg$b5588987112b0b5ff3f11776643d5ace80eefa20e215fc9e3d4458ca3db257c06263ab2a3f6fdfd80b8e971d759545e67f244df4a6ad814545d24f9a185b82d5','goswami@college.edu','student','himanshu goswami','2026-09-28 14:48:40'),(5,'sathavara@college.edu','scrypt:32768:8:1$Iv0pFX5WB4LETL9Q$4c0dff9ed54b01bc7c211154b317467dc2e64f7fa231644e07d5def2622a6a6513485d022aaf8eaaddef974607287f410aecdebecf87325e2e849295ebd69d23','sathavara@college.edu','student','jignesh sathavara','2026-09-28 14:48:40');
/*!40000 ALTER TABLE `scas_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-28 20:19:24
