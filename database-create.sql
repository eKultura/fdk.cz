SET NAMES utf8;
SET foreign_key_checks = 0;

SET NAMES utf8mb4;

CREATE TABLE `FDK_activity_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `user_action` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FDK_activity_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `FDK_users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_attachments` (
  `attachment_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) DEFAULT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_by` int(11) DEFAULT NULL,
  `uloaded_date` datetime DEFAULT NULL,
  PRIMARY KEY (`attachment_id`),
  KEY `task_id` (`task_id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `FDK_attachments_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `FDK_tasks` (`task_id`) ON DELETE CASCADE,
  CONSTRAINT `FDK_attachments_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `FDK_users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_categories` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `posted` datetime DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `task_id` (`task_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FDK_comments_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `FDK_tasks` (`task_id`) ON DELETE CASCADE,
  CONSTRAINT `FDK_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `FDK_users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_ip` (
  `ip_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `ip_range` varchar(255) NOT NULL,
  `created` datetime DEFAULT current_timestamp(),
  `permissions` enum('manage','delete') DEFAULT 'manage',
  PRIMARY KEY (`ip_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `FDK_ip_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_priorities` (
  `priority_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `priority_level` int(11) DEFAULT NULL,
  PRIMARY KEY (`priority_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_projects` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `public` tinyint(1) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_tags` (
  `tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_tasks` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `category` varchar(16) DEFAULT NULL,
  `priority_id` int(11) DEFAULT NULL,
  `priority` varchar(16) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `creator` varchar(50) DEFAULT NULL,
  `assigned` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  KEY `category_id` (`category_id`),
  KEY `priority_id` (`priority_id`),
  KEY `fk_parent_task` (`parent_id`),
  KEY `fk_project_task` (`project_id`),
  CONSTRAINT `FDK_Tasks_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `FDK_categories` (`category_id`) ON DELETE CASCADE,
  CONSTRAINT `FDK_Tasks_ibfk_2` FOREIGN KEY (`priority_id`) REFERENCES `FDK_priorities` (`priority_id`) ON DELETE SET NULL,
  CONSTRAINT `fk_parent_task` FOREIGN KEY (`parent_id`) REFERENCES `FDK_tasks` (`task_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_project_task` FOREIGN KEY (`project_id`) REFERENCES `FDK_projects` (`project_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_task_assignments` (
  `task_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `assigned_date` date DEFAULT NULL,
  PRIMARY KEY (`task_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `FDK_task_assignments_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `FDK_Tasks` (`task_id`) ON DELETE CASCADE,
  CONSTRAINT `FDK_task_assignments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `FDK_Users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_translations` (
  `translation_id` int(11) NOT NULL AUTO_INCREMENT,
  `ref_table` varchar(50) DEFAULT NULL,
  `ref_id` int(11) DEFAULT NULL,
  `lang_code` char(2) DEFAULT NULL,
  `field_name` varchar(50) DEFAULT NULL,
  `text` text DEFAULT NULL,
  PRIMARY KEY (`translation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `FDK_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 2024-05-08 06:26:16

