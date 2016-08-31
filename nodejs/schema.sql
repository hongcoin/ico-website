CREATE TABLE `contract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(45) DEFAULT NULL,
  `contract_name` varchar(45) DEFAULT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `abi_definition` longtext,
  `creation_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
