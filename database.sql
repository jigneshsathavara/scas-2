CREATE DATABASE IF NOT EXISTS `scas_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `scas_db`;

SET FOREIGN_KEY_CHECKS = 0;

-- Table structure for table `scas_users`
DROP TABLE IF EXISTS `scas_users`;
CREATE TABLE `scas_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL UNIQUE,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(120) NOT NULL UNIQUE,
  `role` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_courses`
DROP TABLE IF EXISTS `scas_courses`;
CREATE TABLE `scas_courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL UNIQUE,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_batches`
DROP TABLE IF EXISTS `scas_batches`;
CREATE TABLE `scas_batches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `course_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `scas_batches_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `scas_courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_faculty_profiles`
DROP TABLE IF EXISTS `scas_faculty_profiles`;
CREATE TABLE `scas_faculty_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `department` varchar(100) NOT NULL,
  `designation` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `scas_faculty_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `scas_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_student_profiles`
DROP TABLE IF EXISTS `scas_student_profiles`;
CREATE TABLE `scas_student_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `roll_no` varchar(30) NOT NULL UNIQUE,
  `batch_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `batch_id` (`batch_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `scas_student_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `scas_users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `scas_student_profiles_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `scas_batches` (`id`) ON DELETE CASCADE,
  CONSTRAINT `scas_student_profiles_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `scas_courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_subjects`
DROP TABLE IF EXISTS `scas_subjects`;
CREATE TABLE `scas_subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL UNIQUE,
  `course_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `scas_subjects_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `scas_courses` (`id`) ON DELETE CASCADE,
  CONSTRAINT `scas_subjects_ibfk_2` FOREIGN KEY (`faculty_id`) REFERENCES `scas_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_schedules`
DROP TABLE IF EXISTS `scas_schedules`;
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
  CONSTRAINT `scas_schedules_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`) ON DELETE CASCADE,
  CONSTRAINT `scas_schedules_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `scas_batches` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_attendance`
DROP TABLE IF EXISTS `scas_attendance`;
CREATE TABLE `scas_attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `scas_attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `scas_attendance_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_marks`
DROP TABLE IF EXISTS `scas_marks`;
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
  CONSTRAINT `scas_marks_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `scas_marks_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `scas_subjects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `scas_fee_payments`
DROP TABLE IF EXISTS `scas_fee_payments`;
CREATE TABLE `scas_fee_payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `receipt_no` varchar(50) DEFAULT NULL UNIQUE,
  `transaction_id` varchar(50) DEFAULT NULL UNIQUE,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `scas_fee_payments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `scas_student_profiles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Dumping data for tables

-- Dumping data for table `scas_users`
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (1, 'admin', 'scrypt:32768:8:1$NuSeobOsFsSs5AVx$0ba095fe24fa6689aa84f188c8c8825fcf7fe3af29d59db2e9c871a9421b22c0d940d6086f74e20854d1d58b77369cf0b11b73be274b8dd65d318425a3c0e6ad', 'admin@college.edu', 'admin', 'Dean System Administrator', '2026-08-01 16:28:47.542634');

-- Dumping data for table `scas_courses`
INSERT INTO `scas_courses` (`id`, `name`, `code`, `description`) VALUES (1, 'Master of Computer Applications', 'MCA', 'Post-graduate program in Computer Applications and Software Engineering.');
INSERT INTO `scas_courses` (`id`, `name`, `code`, `description`) VALUES (2, 'Bachelor of Technology', 'BTECH', 'Undergraduate engineering studies program.');

-- Dumping data for table `scas_batches`
INSERT INTO `scas_batches` (`id`, `name`, `course_id`, `year`) VALUES (1, 'MCA 2024-2026', 1, 2026);
INSERT INTO `scas_batches` (`id`, `name`, `course_id`, `year`) VALUES (2, 'BTech 2023-2027', 2, 2027);

-- Dumping data for table `scas_faculty_profiles`
-- No data in table `scas_faculty_profiles`

-- Dumping data for table `scas_student_profiles`
-- No data in table `scas_student_profiles`

-- Dumping data for table `scas_subjects`
-- No data in table `scas_subjects`

-- Dumping data for table `scas_schedules`
-- No data in table `scas_schedules`

-- Dumping data for table `scas_attendance`
-- No data in table `scas_attendance`

-- Dumping data for table `scas_marks`
-- No data in table `scas_marks`

-- Dumping data for table `scas_fee_payments`
-- No data in table `scas_fee_payments`

SET FOREIGN_KEY_CHECKS = 1;