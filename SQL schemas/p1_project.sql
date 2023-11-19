CREATE TABLE `p1_projects` (
  `project_id` varchar(4) DEFAULT NULL,
  `client` varchar(45) DEFAULT NULL,
  `project_name` varchar(45) DEFAULT NULL,
  `job_position` varchar(45) DEFAULT NULL,
  `number_employees` int DEFAULT NULL,
  `note` text DEFAULT NULL,
  `compensation` int DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
