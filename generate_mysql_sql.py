import sqlite3

def convert_sqlite_to_mysql():
    sqlite_conn = sqlite3.connect('database.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    sql_dump = []
    
    # Database initialization headers
    sql_dump.append("CREATE DATABASE IF NOT EXISTS `scas_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    sql_dump.append("USE `scas_db`;\n")
    sql_dump.append("SET FOREIGN_KEY_CHECKS = 0;\n")
    
    # List of tables to drop and create in correct relational order
    tables = [
        'scas_users', 'scas_courses', 'scas_batches', 'scas_faculty_profiles', 
        'scas_student_profiles', 'scas_subjects', 'scas_schedules', 'scas_attendance', 
        'scas_marks', 'scas_fee_payments'
    ]
    
    ddl_statements = {
        'scas_users': """
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_courses': """
DROP TABLE IF EXISTS `scas_courses`;
CREATE TABLE `scas_courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(20) NOT NULL UNIQUE,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_batches': """
DROP TABLE IF EXISTS `scas_batches`;
CREATE TABLE `scas_batches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `course_id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `scas_batches_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `scas_courses` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_faculty_profiles': """
DROP TABLE IF EXISTS `scas_faculty_profiles`;
CREATE TABLE `scas_faculty_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `department` varchar(100) NOT NULL,
  `designation` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `scas_faculty_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `scas_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_student_profiles': """
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_subjects': """
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_schedules': """
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_attendance': """
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_marks': """
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""",

        'scas_fee_payments': """
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
    }

    # Add DDLs
    for t in tables:
        sql_dump.append(f"-- Table structure for table `{t}`")
        sql_dump.append(ddl_statements[t].strip())
        sql_dump.append("")

    # Add DMLs (Inserts)
    for t in tables:
        sqlite_cursor.execute(f"SELECT * FROM {t}")
        rows = sqlite_cursor.fetchall()
        
        sqlite_cursor.execute(f"PRAGMA table_info({t})")
        cols = [col[1] for col in sqlite_cursor.fetchall()]
        
        if rows:
            sql_dump.append(f"-- Dumping data for table `{t}`")
            col_list_str = ", ".join([f"`{c}`" for c in cols])
            
            for row in rows:
                val_list = []
                for val in row:
                    if val is None:
                        val_list.append("NULL")
                    elif isinstance(val, str):
                        escaped_val = val.replace("'", "''")
                        val_list.append(f"'{escaped_val}'")
                    else:
                        val_list.append(str(val))
                        
                val_list_str = ", ".join(val_list)
                sql_dump.append(f"INSERT INTO `{t}` ({col_list_str}) VALUES ({val_list_str});")
            sql_dump.append("")

    sql_dump.append("SET FOREIGN_KEY_CHECKS = 1;")
    
    with open('database.sql', 'w', encoding='utf-8') as f:
        f.write("\n".join(sql_dump))
        
    print("Database conversion successful! database.sql recreated with prefixed tables.")
    sqlite_conn.close()

if __name__ == '__main__':
    convert_sqlite_to_mysql()
