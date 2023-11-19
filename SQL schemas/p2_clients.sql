CREATE TABLE `p1_clients` (
  `client_id` varchar(4) NOT NULL,
  `company` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `industry` varchar(45) DEFAULT NULL,
  `note` text,
  `ci_name` varchar(45) DEFAULT NULL,
  `ci_phone` varchar(45) DEFAULT NULL,
  `ci_email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
