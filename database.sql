CREATE DATABASE IF NOT EXISTS `scas_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `scas_db`;

SET FOREIGN_KEY_CHECKS = 0;

-- Table structure for table `users`
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL UNIQUE,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(120) NOT NULL UNIQUE,
  `role` varchar(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `courses`
CREATE TABLE IF NOT EXISTS `courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL UNIQUE,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `batches`
CREATE TABLE IF NOT EXISTS `batches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `course_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `batches_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `faculty_profiles`
CREATE TABLE IF NOT EXISTS `faculty_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `department` varchar(100) NOT NULL,
  `designation` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `faculty_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `student_profiles`
CREATE TABLE IF NOT EXISTS `student_profiles` (
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
  CONSTRAINT `student_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `student_profiles_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `batches` (`id`) ON DELETE CASCADE,
  CONSTRAINT `student_profiles_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `subjects`
CREATE TABLE IF NOT EXISTS `subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL UNIQUE,
  `course_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `subjects_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  CONSTRAINT `subjects_ibfk_2` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `schedules`
CREATE TABLE IF NOT EXISTS `schedules` (
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
  CONSTRAINT `schedules_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE,
  CONSTRAINT `schedules_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `batches` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `attendance`
CREATE TABLE IF NOT EXISTS `attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `marks`
CREATE TABLE IF NOT EXISTS `marks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `exam_type` varchar(30) NOT NULL,
  `marks_obtained` float NOT NULL,
  `max_marks` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `marks_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `marks_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table `fee_payments`
CREATE TABLE IF NOT EXISTS `fee_payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `receipt_no` varchar(50) DEFAULT NULL UNIQUE,
  `transaction_id` varchar(50) DEFAULT NULL UNIQUE,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `fee_payments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student_profiles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table `users`
INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (1, 'admin', 'scrypt:32768:8:1$NuSeobOsFsSs5AVx$0ba095fe24fa6689aa84f188c8c8825fcf7fe3af29d59db2e9c871a9421b22c0d940d6086f74e20854d1d58b77369cf0b11b73be274b8dd65d318425a3c0e6ad', 'admin@college.edu', 'admin', 'Dean System Administrator', '2026-08-01 16:28:47.542634');
INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (2, 'dr_sharma', 'scrypt:32768:8:1$yfnLSsKDa3hxbOTU$f9c9f36a38d9bfa323fc0600fb206def4f39da525376e239b78339aba7ab2cea7bc5d070a3791a2e281f095a6dac0000a7132c1bfc0d11656b09e2fc541e4c5c', 'r.sharma@college.edu', 'faculty', 'Dr. Chandrkant  Patel', '2026-08-01 16:28:47.542634');
INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (3, 'prof_verma', 'scrypt:32768:8:1$KjtdE0iqEp0fh2KT$8a852db8fa86ca5c8c0815bc83d27cf1e57923a98e681a4d60eaee5009e4b6bf4ab405b1de8d2939f36924fe79e08a06671f73293aaaf91dc9d5b8224fe0ea18', 'a.verma@college.edu', 'faculty', 'Prof. Amit Verma', '2026-08-01 16:28:47.542634');
INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (4, 'alice', 'scrypt:32768:8:1$hnbAEfr0qYgcK3Yb$ed6bb2ef73cdaeb1cb934e2548feb1f60dc4c8be47462e3ecdb748750f2a896292410915ab209564430b2a72c92da67a6bce7e98c56abc9372c155b19b4f1b19', 'alice.c@student.edu', 'student', 'Alice Cooper', '2026-08-01 16:28:48.144452');
INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (5, 'bob', 'scrypt:32768:8:1$hOolMK0qrX4hZ0tg$fdd2c063ea2151a40b0fca311f7a0062177c6c8bc939cc54d9deb8f297f325b2f938259d5aeeb0f69f4f7b66f8235bc49e50a28d168f44f522ebe4ff49e50f78', 'bob.m@student.edu', 'student', 'Bob Marley', '2026-08-01 16:28:48.144452');
INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `role`, `name`, `created_at`) VALUES (6, 'charlie', 'scrypt:32768:8:1$y4p2rIj3mSVTpdOw$a6f0df575033c79d5c350510dcaf0547c299fa154155b4e20a62e4baad118a450230fae960cb31317b5fea0be12c2b82c668f88415b7184e49e283b1f76d3100', 'charlie.p@student.edu', 'student', 'Charlie Puth', '2026-08-01 16:28:48.144452');

-- Dumping data for table `courses`
INSERT INTO `courses` (`id`, `name`, `code`, `description`) VALUES (1, 'Master of Computer Applications', 'MCA', 'Post-graduate program in Computer Applications and Software Engineering.');
INSERT INTO `courses` (`id`, `name`, `code`, `description`) VALUES (2, 'Bachelor of Technology', 'BTECH', 'Undergraduate engineering studies program.');

-- Dumping data for table `batches`
INSERT INTO `batches` (`id`, `name`, `course_id`, `year`) VALUES (1, 'MCA 2024-2026', 1, 2026);
INSERT INTO `batches` (`id`, `name`, `course_id`, `year`) VALUES (2, 'BTech 2023-2027', 2, 2027);

-- Dumping data for table `faculty_profiles`
INSERT INTO `faculty_profiles` (`id`, `user_id`, `department`, `designation`) VALUES (1, 2, 'Computer Applications', 'Professor & HOD');
INSERT INTO `faculty_profiles` (`id`, `user_id`, `department`, `designation`) VALUES (2, 3, 'Computer Applications', 'Assistant Professor');

-- Dumping data for table `student_profiles`
INSERT INTO `student_profiles` (`id`, `user_id`, `roll_no`, `batch_id`, `course_id`, `phone`) VALUES (1, 4, 'MCA24001', 1, 1, '9876543210');
INSERT INTO `student_profiles` (`id`, `user_id`, `roll_no`, `batch_id`, `course_id`, `phone`) VALUES (2, 5, 'MCA24002', 1, 1, '8765432109');
INSERT INTO `student_profiles` (`id`, `user_id`, `roll_no`, `batch_id`, `course_id`, `phone`) VALUES (3, 6, 'MCA24003', 1, 1, '7654321098');

-- Dumping data for table `subjects`
INSERT INTO `subjects` (`id`, `name`, `code`, `course_id`, `faculty_id`) VALUES (1, 'Python Web Development', 'MCA-101', 1, 2);
INSERT INTO `subjects` (`id`, `name`, `code`, `course_id`, `faculty_id`) VALUES (2, 'Machine Learning & Analytics', 'MCA-102', 1, 2);
INSERT INTO `subjects` (`id`, `name`, `code`, `course_id`, `faculty_id`) VALUES (3, 'Advanced Database Systems', 'MCA-103', 1, 3);

-- Dumping data for table `schedules`
INSERT INTO `schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (1, 1, 1, 'Monday', '10:00 AM', '12:00 PM', 'Lab 3');
INSERT INTO `schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (2, 2, 1, 'Tuesday', '09:00 AM', '11:00 AM', 'L-201');
INSERT INTO `schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (3, 3, 1, 'Wednesday', '10:00 AM', '12:00 PM', 'L-102');
INSERT INTO `schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (4, 1, 1, 'Thursday', '02:00 PM', '04:00 PM', 'Lab 3');
INSERT INTO `schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (5, 2, 1, 'Thursday', '11:00 AM', '01:00 PM', 'L-201');
INSERT INTO `schedules` (`id`, `subject_id`, `batch_id`, `day_of_week`, `start_time`, `end_time`, `room`) VALUES (6, 3, 1, 'Friday', '09:00 AM', '11:00 AM', 'L-102');

-- Dumping data for table `attendance`
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (1, 1, 1, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (2, 2, 1, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (3, 3, 1, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (4, 1, 2, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (5, 2, 2, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (6, 3, 2, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (7, 1, 3, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (8, 2, 3, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (9, 3, 3, '2026-08-01', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (10, 1, 1, '2026-07-31', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (11, 2, 1, '2026-07-31', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (12, 3, 1, '2026-07-31', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (13, 1, 2, '2026-07-31', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (14, 2, 2, '2026-07-31', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (15, 3, 2, '2026-07-31', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (16, 1, 3, '2026-07-31', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (17, 2, 3, '2026-07-31', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (18, 3, 3, '2026-07-31', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (19, 1, 1, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (20, 2, 1, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (21, 3, 1, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (22, 1, 2, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (23, 2, 2, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (24, 3, 2, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (25, 1, 3, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (26, 2, 3, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (27, 3, 3, '2026-07-30', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (28, 1, 1, '2026-07-29', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (29, 2, 1, '2026-07-29', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (30, 3, 1, '2026-07-29', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (31, 1, 2, '2026-07-29', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (32, 2, 2, '2026-07-29', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (33, 3, 2, '2026-07-29', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (34, 1, 3, '2026-07-29', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (35, 2, 3, '2026-07-29', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (36, 3, 3, '2026-07-29', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (37, 1, 1, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (38, 2, 1, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (39, 3, 1, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (40, 1, 2, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (41, 2, 2, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (42, 3, 2, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (43, 1, 3, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (44, 2, 3, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (45, 3, 3, '2026-07-28', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (46, 1, 1, '2026-07-27', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (47, 2, 1, '2026-07-27', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (48, 3, 1, '2026-07-27', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (49, 1, 2, '2026-07-27', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (50, 2, 2, '2026-07-27', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (51, 3, 2, '2026-07-27', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (52, 1, 3, '2026-07-27', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (53, 2, 3, '2026-07-27', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (54, 3, 3, '2026-07-27', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (55, 1, 1, '2026-07-25', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (56, 2, 1, '2026-07-25', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (57, 3, 1, '2026-07-25', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (58, 1, 2, '2026-07-25', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (59, 2, 2, '2026-07-25', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (60, 3, 2, '2026-07-25', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (61, 1, 3, '2026-07-25', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (62, 2, 3, '2026-07-25', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (63, 3, 3, '2026-07-25', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (64, 1, 1, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (65, 2, 1, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (66, 3, 1, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (67, 1, 2, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (68, 2, 2, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (69, 3, 2, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (70, 1, 3, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (71, 2, 3, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (72, 3, 3, '2026-07-24', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (73, 1, 1, '2026-07-23', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (74, 2, 1, '2026-07-23', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (75, 3, 1, '2026-07-23', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (76, 1, 2, '2026-07-23', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (77, 2, 2, '2026-07-23', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (78, 3, 2, '2026-07-23', 'Absent');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (79, 1, 3, '2026-07-23', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (80, 2, 3, '2026-07-23', 'Present');
INSERT INTO `attendance` (`id`, `student_id`, `subject_id`, `date`, `status`) VALUES (81, 3, 3, '2026-07-23', 'Absent');

-- Dumping data for table `marks`
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (1, 1, 1, 'Midterm 1', 27.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (2, 2, 1, 'Midterm 1', 20.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (3, 3, 1, 'Midterm 1', 11.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (4, 1, 1, 'Midterm 2', 28.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (5, 2, 1, 'Midterm 2', 18.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (6, 3, 1, 'Midterm 2', 12.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (7, 1, 1, 'Final Exam', 94.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (8, 2, 1, 'Final Exam', 73.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (9, 3, 1, 'Final Exam', 42.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (10, 1, 2, 'Midterm 1', 27.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (11, 2, 2, 'Midterm 1', 20.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (12, 3, 2, 'Midterm 1', 11.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (13, 1, 2, 'Midterm 2', 28.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (14, 2, 2, 'Midterm 2', 18.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (15, 3, 2, 'Midterm 2', 12.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (16, 1, 2, 'Final Exam', 94.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (17, 2, 2, 'Final Exam', 73.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (18, 3, 2, 'Final Exam', 42.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (19, 1, 3, 'Midterm 1', 27.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (20, 2, 3, 'Midterm 1', 20.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (21, 3, 3, 'Midterm 1', 11.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (22, 1, 3, 'Midterm 2', 28.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (23, 2, 3, 'Midterm 2', 18.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (24, 3, 3, 'Midterm 2', 12.0, 30.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (25, 1, 3, 'Final Exam', 94.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (26, 2, 3, 'Final Exam', 73.0, 100.0);
INSERT INTO `marks` (`id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `max_marks`) VALUES (27, 3, 3, 'Final Exam', 42.0, 100.0);

-- Dumping data for table `fee_payments`
INSERT INTO `fee_payments` (`id`, `student_id`, `amount`, `payment_date`, `status`, `receipt_no`, `transaction_id`) VALUES (1, 1, 65000.0, '2026-07-12 21:58:48.172865', 'Paid', 'REC-MCA24001-9034', 'TXN-ALICECOOPER7842');
INSERT INTO `fee_payments` (`id`, `student_id`, `amount`, `payment_date`, `status`, `receipt_no`, `transaction_id`) VALUES (2, 2, 65000.0, '2026-07-14 21:58:48.172865', 'Paid', 'REC-MCA24002-4211', 'TXN-BOBMARLEY1094');
INSERT INTO `fee_payments` (`id`, `student_id`, `amount`, `payment_date`, `status`, `receipt_no`, `transaction_id`) VALUES (3, 3, 65000.0, '2026-08-01 16:28:48.186682', 'Pending', 'REC-MCA24003-DEF', NULL);

SET FOREIGN_KEY_CHECKS = 1;