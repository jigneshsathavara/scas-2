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

-- Dumping data for table `scas_users`
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (1, 'admin', 'scrypt:32768:8:1$auSGMTaQnFZLdoP3$672dcb3bee729e5b6a1234d0afbb1787c521a6016bf26820d511a197f19ab8b2efffa7cdfa18350c18dacef6b67b200aa0967a04a4cace0ecf388c90a57bf2e0', 'admin@college.edu', 'admin', 'Dean System Administrator', '2026-08-04 16:37:06.395113');
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (2, 'dr_sharma', 'scrypt:32768:8:1$0O1QPIXubBf2zE27$0e28ae9e65dd61067d7591cf2ad4666afeb569295bfe2f66f343201c8d014851e81bf876065a778c39a79a0ded4061bf6cb782f1238eecb808bcda91e34c7191', 'r.sharma@college.edu', 'faculty', 'Dr. Rajesh Sharma', '2026-08-04 16:37:06.395113');
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (3, 'prof_verma', 'scrypt:32768:8:1$XpdLLhafmLcLRUie$0789188425565e4f9819b116992034922c3367a0c628a9e6e40606ad588356dfc994530d205282e0f8a97afdb505a3e92162f7f555b664d25b63d74335962f0c', 'a.verma@college.edu', 'faculty', 'Prof. Amit Verma', '2026-08-04 16:37:06.395113');

-- Dumping data for table `scas_courses`
INSERT INTO `scas_courses` (`id`, `name`, `code`, `description`) VALUES (1, 'Master of Computer Applications', 'MCA', 'Post-graduate program in Computer Applications and Software Engineering.');
INSERT INTO `scas_courses` (`id`, `name`, `code`, `description`) VALUES (2, 'Bachelor of Technology', 'BTECH', 'Undergraduate engineering studies program.');

-- Dumping data for table `scas_batches`
INSERT INTO `scas_batches` (`id`, `name`, `course_id`, `year`) VALUES (1, 'MCA 2024-2026', 1, 2026);
INSERT INTO `scas_batches` (`id`, `name`, `course_id`, `year`) VALUES (2, 'BTech 2023-2027', 2, 2027);

-- Dumping data for table `scas_faculty_profiles`
INSERT INTO `scas_faculty_profiles` (`id`, `user_id`, `department`, `designation`) VALUES (1, 2, 'Computer Applications', 'Professor & HOD');
INSERT INTO `scas_faculty_profiles` (`id`, `user_id`, `department`, `designation`) VALUES (2, 3, 'Computer Applications', 'Assistant Professor');

-- Dumping data for table `scas_subjects`
INSERT INTO `scas_subjects` (`id`, `name`, `code`, `course_id`, `faculty_id`) VALUES (1, 'Python Web Development', 'MCA-101', 1, 2);
INSERT INTO `scas_subjects` (`id`, `name`, `code`, `course_id`, `faculty_id`) VALUES (2, 'Machine Learning & Analytics', 'MCA-102', 1, 2);
INSERT INTO `scas_subjects` (`id`, `name`, `code`, `course_id`, `faculty_id`) VALUES (3, 'Advanced Database Systems', 'MCA-103', 1, 3);

-- Dumping data for table `scas_schedules`
INSERT INTO `scas_schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (1, 1, 1, 'Monday', '10:00 AM', '12:00 PM', 'Lab 3');
INSERT INTO `scas_schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (2, 2, 1, 'Tuesday', '09:00 AM', '11:00 AM', 'L-201');
INSERT INTO `scas_schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (3, 3, 1, 'Wednesday', '10:00 AM', '12:00 PM', 'L-102');
INSERT INTO `scas_schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (4, 1, 1, 'Thursday', '02:00 PM', '04:00 PM', 'Lab 3');
INSERT INTO `scas_schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (5, 2, 1, 'Thursday', '11:00 AM', '01:00 PM', 'L-201');
INSERT INTO `scas_schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (6, 3, 1, 'Friday', '09:00 AM', '11:00 AM', 'L-102');

SET FOREIGN_KEY_CHECKS = 1;