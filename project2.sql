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

-- Adding Foreign Key "stock" to price_history table
ALTER TABLE price_history
ADD CONSTRAINT FK_Pricehistory_Stock
FOREIGN KEY (stock) REFERENCES stock(id);

-- Adding Foreign Key "company" to the stock table
ALTER TABLE stock
ADD CONSTRAINT FK_Stock_Company
FOREIGN KEY (company) REFERENCES company(id);

-- Adding Foreign Key "stock" to the transactions table
ALTER TABLE transactions
ADD CONSTRAINT FK_Transactions_Stock
FOREIGN KEY (stock) REFERENCES stock(id);

-- Adding Foreign Key "user" to transactions table
ALTER TABLE transactions
ADD CONSTRAINT FK_Transactions_User
FOREIGN KEY (user) REFERENCES user(id);

-- Adding Foreign Key "Owner" to the wallet table
ALTER TABLE wallet
ADD CONSTRAINT FK_Wallet_User
FOREIGN KEY (owner) REFERENCES user(id);

-- Adding Foreign Key "wallet" to wallet_item table
ALTER TABLE wallet_item
ADD CONSTRAINT FK_Walletitem_Wallet
FOREIGN KEY (wallet) REFERENCES wallet(id);

-- Adding Foreign key "stock" to wallet_item table
ALTER TABLE wallet_item
ADD CONSTRAINT FK_Walletitem_Stock
FOREIGN KEY (stock) REFERENCES stock(id);

-- Stored procidure to update the stock price

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

DELIMITER //

-- stored procedure to buy stock
DROP PROCEDURE IF EXISTS buyStock;

CREATE PROCEDURE buyStock(IN stocksym VARCHAR(10), IN quantity INT, IN userID INT)
BEGIN

DECLARE stockID INT DEFAULT 0;
DECLARE stockPrice INT DEFAULT 0;
DECLARE walletamount INT DEFAULT 0;
DECLARE stockexists INT DEFAULT 0;
DECLARE walletID INT DEFAULT 0;

DECLARE exit handler for sqlexception ROLLBACK;
DECLARE exit handler for sqlwarning ROLLBACK;

START TRANSACTION;

-- select 'Starting procedure'; 
-- select stocksym;
-- select quantity;
-- select userID;

select S.id into stockID from stock S 
join company C 
ON S.company=C.id and C.code_name = stocksym;

-- select stockID;

select S.current_price INTO stockPrice
from stock S join company C ON S.company=C.id AND C.code_name= stocksym;

-- select stockPrice;

select wallet_amount INTO walletamount
from wallet 
where owner=userID;
-- select walletamount;

select id INTO walletID
from wallet 
where owner=userID;
-- select walletID;
 
select count(*) INTO stockexists from wallet_item
where stock= stockID AND wallet=walletID;
-- select stockexists;

IF walletamount < (stockPrice*quantity) THEN
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient Funds';
END IF;
-- select 'User has money';

insert INTO transactions (type,price,qty,date_time,amount,user,stock) 
values ("buy", stockPrice, quantity, CURRENT_TIMESTAMP(  ), (stockPrice*quantity), userID, stockID);
-- select 'Updated transactions';

Update wallet SET wallet_amount = (walletamount-(stockPrice*quantity))
where owner= userID;
-- select 'Updated wallet amount';

IF stockexists = 1 THEN
    -- select 'Stock Exists';
    update wallet_item W set W.quantity= (W.quantity+quantity)
    where stock=stockID AND wallet=walletID;
ELSE
    -- select 'Stock does not exist' ;
    insert INTO wallet_item (wallet,stock,quantity) values(walletID,stockID,quantity);
END IF;

Update stock SET available_stocks = (available_stocks-(quantity)) where id= stockID;
-- select 'Available stocks updated';

COMMIT;
-- select 'Procedure committed!';

END //

DELIMITER ;

-- stored procedure to sell stock

DELIMITER //
DROP PROCEDURE IF EXISTS sellStock;

CREATE PROCEDURE sellStock(stocksym VARCHAR(10), quantity INT, userID INT)
BEGIN

DECLARE stockID INT DEFAULT 0;
DECLARE stockPrice INT DEFAULT 0;
DECLARE walletamount INT DEFAULT 0;
DECLARE stockexists INT DEFAULT 0;
DECLARE walletID INT DEFAULT 0;
DECLARE holdingquantity INT DEFAULT 0;

DECLARE exit handler for sqlexception ROLLBACK;
DECLARE exit handler for sqlwarning ROLLBACK;

START TRANSACTION;
select S.id INTO stockID
from stock S join company C ON S.company=C.id AND C.code_name= stocksym;

-- select stockID;

select S.current_price INTO stockPrice
from stock S join company C ON S.company=C.id AND C.code_name= stocksym;

-- select stockPrice;

select wallet_amount INTO walletamount
from wallet 
where owner=userID;

-- select walletamount;

select id INTO walletID
from wallet 
where owner=userID;

-- select walletID;

select count(*) INTO stockexists from wallet_item
where stock= stockID AND wallet=walletID;

-- select stockexists;

IF stockexists = 1 THEN
    select wallet_item.quantity INTO holdingquantity from wallet_item where stock= stockID AND wallet=walletID;
ELSE 
    SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Stock not owned';
END IF;

-- select holdingquantity;
-- select quantity;

IF holdingquantity < quantity THEN
        SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Insufficient Stocks';
END IF;

insert INTO transactions (type,price,qty,date_time,amount,user,stock) 
values ("sell",stockPrice,quantity,CURRENT_TIMESTAMP(  ),(stockPrice*quantity), userID,stockID);

Update wallet SET wallet_amount = (walletamount+(stockPrice*quantity))
where owner= userID;

IF holdingquantity>quantity THEN
    update wallet_item W set W.quantity= (W.quantity-quantity) 
    where stock=stockID AND wallet=walletID;
ELSE 
    DELETE from wallet_item 
    where stock=stockID AND wallet=walletID;
END IF;

Update stock SET available_stocks = (available_stocks+(quantity))
where id= stockID;

COMMIT;
END //

DELIMITER ;

-- stored procedure to withdraw amount

DELIMITER //
DROP PROCEDURE IF EXISTS withdrawAmount;

CREATE PROCEDURE withdrawAmount(wdr_amt INT, userID INT)
BEGIN
DECLARE walletamount INT DEFAULT 0;

DECLARE exit handler for sqlexception ROLLBACK;
DECLARE exit handler for sqlwarning ROLLBACK;

START TRANSACTION;
select wallet_amount INTO walletamount
from wallet 
where owner=userID;

if walletamount < wdr_amt THEN
      SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Insufficient funds';
END IF;

Update wallet SET wallet_amount = (wallet_amount - wdr_amt) where owner= userID;
COMMIT;
END //

DELIMITER ;

-- stored procedure to depositc amount
DELIMITER //
DROP PROCEDURE IF EXISTS depositAmount;

CREATE PROCEDURE depositAmount(dep_amt INT, userID INT)
BEGIN

DECLARE exit handler for sqlexception ROLLBACK;
DECLARE exit handler for sqlwarning ROLLBACK;

START TRANSACTION;
Update wallet SET wallet_amount = (wallet_amount + dep_amt) where owner= userID;
COMMIT;
END //

DELIMITER ;
