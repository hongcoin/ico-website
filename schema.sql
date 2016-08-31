CREATE TABLE `ico_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `record_datetime` DATETIME NULL,
  `balance_total_eth` DOUBLE NULL,
  `balance_main_eth` DOUBLE NULL,
  `balance_mgmtfee_eth` DOUBLE NULL,
  `balance_extra_eth` DOUBLE NULL,
  `current_tier` INT NULL,
  `token_available_current_tier` INT NULL,
  `total_tokens_issued` VARCHAR(45) NULL,
  `bounty_issued` INT NULL,
  PRIMARY KEY (`id`));
