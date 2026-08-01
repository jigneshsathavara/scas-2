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
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (1, 'admin', 'scrypt:32768:8:1$BcWVO6FlbG77lwRw$011b1d8be5d060a5f2c5d19c6f3a1ea8964eec615c92acd19af022326ee69234b2e21e16aed49358e81444b5a660951f5a89a6e0645e70565e02e8e0aa963d11', 'admin@college.edu', 'admin', 'Dean System Administrator', '2026-08-01 17:07:41.630734');
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (2, 'dr_sharma', 'scrypt:32768:8:1$WqUqD4ejtzqAjqxW$e3c1d7485a36e8ef1c27418f6f242c702daa993b37af6cedbd3fa106d43be52393971a3da7bf91225af2baa36b976e8824b2f402825633de8476d2835b1c6815', 'r.sharma@college.edu', 'faculty', 'Dr. Rajesh Sharma', '2026-08-01 17:07:41.630734');
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (3, 'prof_verma', 'scrypt:32768:8:1$63idEWV6zgnfbr9u$f7c9c9ce0ef1a6044813d0846e88cb2a255e0689a8dc3b817df4dd88598d6de0f900c4954edfc9b128d9314ebbdac50c703af02dd3e507ea8fa28fa985c4ee65', 'a.verma@college.edu', 'faculty', 'Prof. Amit Verma', '2026-08-01 17:07:41.630734');
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (4, 'alice', 'scrypt:32768:8:1$oSvDlSEEhM9AYz7a$4078dd417a764868970b3b6e760cd9bce4fa336427cc6c1bdd67acfc9c2e74c72e54834f479285aea46cd93c63bb3bb16febaa98f354b24629e73cfaba299964', 'alice.c@student.edu', 'student', 'Alice Cooper', '2026-08-01 17:07:42.245359');
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (5, 'bob', 'scrypt:32768:8:1$GY4HglMc36geLUD1$e3c56a813d07009d3b1f6204d285fac1d9409bb39a3dda75c5c942809a39aade4009263cbb6ffbfc3f8ee0215150f6187ff6f19627c4b18c1d839d694767ff73', 'bob.m@student.edu', 'student', 'Bob Marley', '2026-08-01 17:07:42.245359');
INSERT INTO `scas_users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (6, 'charlie', 'scrypt:32768:8:1$0utlsXyakTaa9NYn$09f2497fdb324153e853926872d7b5da0e26b6a3094e303fbe562898b3c14ca74d3ceca91e49d1013a16b31f43ee9758e6708c813aa4fd3c77be100209ed5325', 'charlie.p@student.edu', 'student', 'Charlie Puth', '2026-08-01 17:07:42.245359');

-- Dumping data for table `scas_courses`
INSERT INTO `scas_courses` (`id`, `name`, `code`, `description`) VALUES (1, 'Master of Computer Applications', 'MCA', 'Post-graduate program in Computer Applications and Software Engineering.');
INSERT INTO `scas_courses` (`id`, `name`, `code`, `description`) VALUES (2, 'Bachelor of Technology', 'BTECH', 'Undergraduate engineering studies program.');

-- Dumping data for table `scas_batches`
INSERT INTO `scas_batches` (`id`, `name`, `course_id`, `year`) VALUES (1, 'MCA 2024-2026', 1, 2026);
INSERT INTO `scas_batches` (`id`, `name`, `course_id`, `year`) VALUES (2, 'BTech 2023-2027', 2, 2027);

-- Dumping data for table `scas_faculty_profiles`
INSERT INTO `scas_faculty_profiles` (`id`, `user_id`, `department`, `designation`) VALUES (1, 2, 'Computer Applications', 'Professor & HOD');
INSERT INTO `scas_faculty_profiles` (`id`, `user_id`, `department`, `designation`) VALUES (2, 3, 'Computer Applications', 'Assistant Professor');

-- Dumping data for table `scas_student_profiles`
INSERT INTO `scas_student_profiles` (`id`, `user_id`, `roll_no`, `batch_id`, `course_id`, `phone`) VALUES (1, 4, 'MCA24001', 1, 1, '9876543210');
INSERT INTO `scas_student_profiles` (`id`, `user_id`, `roll_no`, `batch_id`, `course_id`, `phone`) VALUES (2, 5, 'MCA24002', 1, 1, '8765432109');
INSERT INTO `scas_student_profiles` (`id`, `user_id`, `roll_no`, `batch_id`, `course_id`, `phone`) VALUES (3, 6, 'MCA24003', 1, 1, '7654321098');

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

-- Dumping data for table `scas_attendance`
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (1, 1, 1, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (2, 2, 1, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (3, 3, 1, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (4, 1, 2, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (5, 2, 2, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (6, 3, 2, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (7, 1, 3, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (8, 2, 3, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (9, 3, 3, '2026-08-01', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (10, 1, 1, '2026-07-31', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (11, 2, 1, '2026-07-31', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (12, 3, 1, '2026-07-31', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (13, 1, 2, '2026-07-31', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (14, 2, 2, '2026-07-31', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (15, 3, 2, '2026-07-31', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (16, 1, 3, '2026-07-31', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (17, 2, 3, '2026-07-31', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (18, 3, 3, '2026-07-31', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (19, 1, 1, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (20, 2, 1, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (21, 3, 1, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (22, 1, 2, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (23, 2, 2, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (24, 3, 2, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (25, 1, 3, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (26, 2, 3, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (27, 3, 3, '2026-07-30', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (28, 1, 1, '2026-07-29', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (29, 2, 1, '2026-07-29', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (30, 3, 1, '2026-07-29', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (31, 1, 2, '2026-07-29', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (32, 2, 2, '2026-07-29', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (33, 3, 2, '2026-07-29', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (34, 1, 3, '2026-07-29', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (35, 2, 3, '2026-07-29', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (36, 3, 3, '2026-07-29', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (37, 1, 1, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (38, 2, 1, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (39, 3, 1, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (40, 1, 2, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (41, 2, 2, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (42, 3, 2, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (43, 1, 3, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (44, 2, 3, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (45, 3, 3, '2026-07-28', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (46, 1, 1, '2026-07-27', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (47, 2, 1, '2026-07-27', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (48, 3, 1, '2026-07-27', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (49, 1, 2, '2026-07-27', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (50, 2, 2, '2026-07-27', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (51, 3, 2, '2026-07-27', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (52, 1, 3, '2026-07-27', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (53, 2, 3, '2026-07-27', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (54, 3, 3, '2026-07-27', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (55, 1, 1, '2026-07-25', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (56, 2, 1, '2026-07-25', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (57, 3, 1, '2026-07-25', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (58, 1, 2, '2026-07-25', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (59, 2, 2, '2026-07-25', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (60, 3, 2, '2026-07-25', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (61, 1, 3, '2026-07-25', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (62, 2, 3, '2026-07-25', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (63, 3, 3, '2026-07-25', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (64, 1, 1, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (65, 2, 1, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (66, 3, 1, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (67, 1, 2, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (68, 2, 2, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (69, 3, 2, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (70, 1, 3, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (71, 2, 3, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (72, 3, 3, '2026-07-24', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (73, 1, 1, '2026-07-23', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (74, 2, 1, '2026-07-23', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (75, 3, 1, '2026-07-23', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (76, 1, 2, '2026-07-23', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (77, 2, 2, '2026-07-23', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (78, 3, 2, '2026-07-23', 'Absent');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (79, 1, 3, '2026-07-23', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (80, 2, 3, '2026-07-23', 'Present');
INSERT INTO `scas_attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (81, 3, 3, '2026-07-23', 'Absent');

-- Dumping data for table `scas_marks`
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (1, 1, 1, 'Midterm 1', 27.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (2, 2, 1, 'Midterm 1', 20.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (3, 3, 1, 'Midterm 1', 11.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (4, 1, 1, 'Midterm 2', 28.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (5, 2, 1, 'Midterm 2', 18.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (6, 3, 1, 'Midterm 2', 12.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (7, 1, 1, 'Final Exam', 94.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (8, 2, 1, 'Final Exam', 73.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (9, 3, 1, 'Final Exam', 42.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (10, 1, 2, 'Midterm 1', 27.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (11, 2, 2, 'Midterm 1', 20.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (12, 3, 2, 'Midterm 1', 11.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (13, 1, 2, 'Midterm 2', 28.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (14, 2, 2, 'Midterm 2', 18.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (15, 3, 2, 'Midterm 2', 12.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (16, 1, 2, 'Final Exam', 94.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (17, 2, 2, 'Final Exam', 73.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (18, 3, 2, 'Final Exam', 42.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (19, 1, 3, 'Midterm 1', 27.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (20, 2, 3, 'Midterm 1', 20.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (21, 3, 3, 'Midterm 1', 11.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (22, 1, 3, 'Midterm 2', 28.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (23, 2, 3, 'Midterm 2', 18.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (24, 3, 3, 'Midterm 2', 12.0, 30.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (25, 1, 3, 'Final Exam', 94.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (26, 2, 3, 'Final Exam', 73.0, 100.0);
INSERT INTO `scas_marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (27, 3, 3, 'Final Exam', 42.0, 100.0);

-- Dumping data for table `scas_fee_payments`
INSERT INTO `scas_fee_payments` (`id`, `student_id`, `amount`, `payment_date`, `status`, `receipt_no`, `transaction_id`) VALUES (1, 1, 65000.0, '2026-07-12 22:37:42.261391', 'Paid', 'REC-MCA24001-9034', 'TXN-ALICECOOPER7842');
INSERT INTO `scas_fee_payments` (`id`, `student_id`, `amount`, `payment_date`, `status`, `receipt_no`, `transaction_id`) VALUES (2, 2, 65000.0, '2026-07-14 22:37:42.261391', 'Paid', 'REC-MCA24002-4211', 'TXN-BOBMARLEY1094');
INSERT INTO `scas_fee_payments` (`id`, `student_id`, `amount`, `payment_date`, `status`, `receipt_no`, `transaction_id`) VALUES (3, 3, 65000.0, '2026-08-01 17:07:42.273662', 'Pending', 'REC-MCA24003-DEF', NULL);

SET FOREIGN_KEY_CHECKS = 1;