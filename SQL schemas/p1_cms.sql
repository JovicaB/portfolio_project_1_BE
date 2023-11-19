CREATE TABLE `p1_cms` (
  `project_id` varchar(4) NOT NULL,
  `candidate_id` varchar(4) NOT NULL,
  `note` text CHARACTER SET utf8 DEFAULT NULL,
  `status_accepted` varchar(1) CHARACTER SET utf8 DEFAULT NULL,
  `status_reserve` varchar(1) CHARACTER SET utf8 DEFAULT NULL,
  `status_rejected` varchar(1) CHARACTER SET utf8 DEFAULT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
