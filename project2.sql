CREATE TABLE `cmpe226p2`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(60) NULL,
  `type` VARCHAR(10) NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `cmpe226p2`.`wallet` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `owner` INT NULL,
  `wallet_amount` FLOAT NULL DEFAULT 0,
  PRIMARY KEY (`id`));

CREATE TABLE `cmpe226p2`.`wallet_item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `wallet` INT NULL,
  `stock` INT NULL,
  `quantity` INT NULL DEFAULT 0,
  PRIMARY KEY (`id`));

CREATE TABLE `cmpe226p2`.`stock` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company` INT NULL UNIQUE,
  `current_price` FLOAT NULL,
  `available_stocks` INT NULL DEFAULT 0,
  PRIMARY KEY (`id`));

CREATE TABLE `cmpe226p2`.`company` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `code_name` VARCHAR(10) NULL UNIQUE,
  `total_stocks` INT NULL DEFAULT 0,
  `address` VARCHAR(100) NULL,
  `about` VARCHAR(256) NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `cmpe226p2`.`price_history` (
  `stock` INT NOT NULL,
  `datetime` DATETIME NOT NULL,
  `price` FLOAT NULL DEFAULT 0);

CREATE TABLE `cmpe226p2`.`transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(10) NULL,
  `price` FLOAT NULL,
  `qty` INT NULL,
  `date_time` DATETIME NULL,
  `amount` FLOAT NULL,
  `user` INT NULL,
  `stock` INT NULL,
  PRIMARY KEY (`id`));

DELIMITER //

CREATE PROCEDURE updatePrice(stockId INT, price FLOAT)
BEGIN
DECLARE exit handler for sqlexception ROLLBACK;
DECLARE exit handler for sqlwarning ROLLBACK;

START TRANSACTION;
update stock set current_price=price where id=stockId;
insert into price_history values(stockId, CURRENT_TIMESTAMP(  ), price);
COMMIT;
END //

DELIMITER ;