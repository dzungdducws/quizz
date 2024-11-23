-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping database structure for testdb
CREATE DATABASE IF NOT EXISTS `testdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `testdb`;

-- Dumping structure for table testdb.answer
CREATE TABLE IF NOT EXISTS `answer` (
  `answer_id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `answer_text` text NOT NULL,
  `is_correct` int(11) DEFAULT 0,
  PRIMARY KEY (`answer_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table testdb.answer: ~5 rows (approximately)
INSERT IGNORE INTO `answer` (`answer_id`, `question_id`, `answer_text`, `is_correct`) VALUES
	(1, 1, '4', 1),
	(2, 1, '5', 0),
	(3, 2, '4', 1),
	(4, 2, '5', 0),
	(5, 3, 'George Washington', 1);

-- Dumping structure for table testdb.question
CREATE TABLE IF NOT EXISTS `question` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `set_id` int(11) NOT NULL,
  `question_text` text NOT NULL,
  PRIMARY KEY (`question_id`),
  KEY `set_id` (`set_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`set_id`) REFERENCES `questionset` (`set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table testdb.question: ~5 rows (approximately)
INSERT IGNORE INTO `question` (`question_id`, `set_id`, `question_text`) VALUES
	(1, 1, 'What is 2 + 2?'),
	(2, 1, 'What is the square root of 16?'),
	(3, 2, 'Who was the first president of the USA?'),
	(4, 3, 'What is the chemical symbol for water?'),
	(5, 4, 'What is the capital of France?');

-- Dumping structure for table testdb.questionset
CREATE TABLE IF NOT EXISTS `questionset` (
  `set_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`set_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table testdb.questionset: ~7 rows (approximately)
INSERT IGNORE INTO `questionset` (`set_id`, `title`, `type`) VALUES
	(1, 'Math Questions', 'Multiple Choice'),
	(2, 'History Questions', 'True/False'),
	(3, 'Science Questions', 'Short Answer'),
	(4, 'Geography Questions', 'Multiple Choice'),
	(5, 'Literature Questions', 'True/False'),
	(6, 'test khong co gi', 'Multiple Choice'),
	(7, 'test co gi', 'test thoi'),
	(8, 'test', 'test thoi');

-- Dumping structure for table testdb.user
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table testdb.user: ~6 rows (approximately)
INSERT IGNORE INTO `user` (`user_id`, `username`, `email`, `password_hash`, `created_at`) VALUES
	(1, 'user1', 'user1@example.com', 'hashedpassword1', '0000-00-00 00:00:00'),
	(2, 'user2', 'user2@example.com', 'hashedpassword2', '0000-00-00 00:00:00'),
	(3, 'user3', 'user3@example.com', 'hashedpassword3', '0000-00-00 00:00:00'),
	(4, 'user4', 'user4@example.com', 'hashedpassword4', '0000-00-00 00:00:00'),
	(5, 'user5', 'user5@example.com', 'hashedpassword5', '0000-00-00 00:00:00'),
	(11, 'dzungdducws', 'dzungdducws@gmail.com', '$2b$12$O2y.N2I9mhu17eYCDHNv9ey32sxUyYO0CLBtt5zfTxcWs1gHqQbSG', '2024-11-23 10:22:21');

-- Dumping structure for table testdb.user_quest
CREATE TABLE IF NOT EXISTS `user_quest` (
  `user_quest_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `completed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_quest_id`),
  KEY `user_id` (`user_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `user_quest_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `user_quest_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `question` (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table testdb.user_quest: ~5 rows (approximately)
INSERT IGNORE INTO `user_quest` (`user_quest_id`, `user_id`, `question_id`, `status`, `completed_at`) VALUES
	(1, 1, 1, 1, '2024-12-11 17:00:00'),
	(2, 2, 2, 0, '2024-12-11 17:00:00'),
	(3, 3, 3, 1, '2024-12-11 17:00:00'),
	(4, 4, 4, 1, '2024-12-11 17:00:00'),
	(5, 5, 5, 0, '2024-12-11 17:00:00');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
