-- # SJSU CMPE 226 Fall 2020 TEAM 5
-- Make sure to create 6 users using API before running this script because users needs the passord to be hashed.
-- SO we can not add them through queries.

use cmpe226p2; 

-- Insert 10 companies and their corresponding stock symbols. 
insert into company (name, code_name, total_stocks, address, about) values ('Tesla', 'TSLA', 10000000, 'Fremont CA', 'EV maker, Battery technology pioneer'); 
insert into company (name, code_name, total_stocks, address, about) values ('Alibaba', 'BABA', 20000000, 'Hangzhou, China', 'E-commerce, Retail, Technology and more');
insert into company (name, code_name, total_stocks, address, about) values ('Electronic Arts', 'EA', 30000000, 'Redwood City, CA', 'Online gaming'); 
insert into company (name, code_name, total_stocks, address, about) values ('L Brands', 'LB', 100000000, 'New York, NY', 'Fashion Apparel'); 
insert into company (name, code_name, total_stocks, address, about) values ('CVS Pharmacy', 'CVS', 100000000, 'Woonsocket, RI', 'Health care services, Pharmacy'); 
insert into company (name, code_name, total_stocks, address, about) values ('Google', 'GOOG', 100000000, 'Mountain View, CA', 'Advertising'); 
insert into company (name, code_name, total_stocks, address, about) values ('VM ware', 'VM', 200000000, 'Palo Alto, CA', 'Advertising'); 
insert into company (name, code_name, total_stocks, address, about) values ('Starbucks', 'SBUX', 200000000, 'Seattle, WA', 'Retail'); 
insert into company (name, code_name, total_stocks, address, about) values ('Ford', 'F', 200000000, 'Detroit, MI', 'Car manufacturer'); 
insert into company (name, code_name, total_stocks, address, about) values ('Apple', 'AAPL', 200000000, 'Cupertino, CA', 'Phone manufacturer'); 
select * from company; 

-- Insert 10 stocks data 
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='TSLA'), '10.00', 5000000); 
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='BABA'), '500.00', 20000000);  
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='EA'), '100.00', 30000000); 
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='LB'), '200.00', 5000000); 
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='CVS'), '10.00', 10000000); 
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='GOOG'), '90.00', 100000000); 
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='VM'), '100.00', 200000000);
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='SBUX'), '30.00', 200000000);
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='F'), '10.00', 200000000);
insert into stock (company, current_price, available_stocks) values ((select id from company where code_name='AAPL'), '200.00', 200000000);
select * from stock; 


-- Create wallets for all 6 users. 
select * from user; 
insert into wallet (owner, wallet_amount) values ((select id from user where user.id=1), 50000);
insert into wallet (owner, wallet_amount) values ((select id from user where user.id=2), 40000);
insert into wallet (owner, wallet_amount) values ((select id from user where user.id=3), 30000);
insert into wallet (owner, wallet_amount) values ((select id from user where user.id=4), 20000); 
insert into wallet (owner, wallet_amount) values ((select id from user where user.id=5), 10000); 
insert into wallet (owner, wallet_amount) values ((select id from user where user.id=6), 60000);
select * from wallet;  

-- a select statement before and after calling the procedure is to show the before and after states
select * from all_tickers where STOCKID=5; 
call updatePrice(5, 20); 
select * from price_history where stock=5;

select * from wallet where owner = 6; 
call depositAmount(20000, 6); 
select * from wallet where owner = 6; 
select * from transactions where user=6 and UPPER(type) = 'DEPOSIT' and amount = 20000; 

select * from wallet where owner = 6; 
call withdrawAmount(15000, 6); 
select * from wallet where owner = 6; 
select * from transactions where user=6 and UPPER(type) = 'WITHDRAW' and amount = 15000; 

-- For User ID 6, wallet ID is 6.  
select * from wallet_item where wallet = 6; 
select * from transactions where UPPER(type) = 'SELL' and user = 6 and qty = 9; 
call buyStock('AAPL', 9, 6); 
select * from wallet_item where wallet = 6; 
select * from transactions where UPPER(type) = 'SELL' and user = 6 and qty = 9; 

-- For User ID 6, wallet ID is 6.  
select * from wallet_item where wallet = 6; 
select * from transactions where UPPER(type) = 'SELL' and user = 6 and qty = 9; 
call sellStock('AAPL', 9, 6); 
select * from wallet_item where wallet = 6; 
select * from transactions where UPPER(type) = 'SELL' and user = 6 and qty = 9; 

-- Invoke a combination of buy, sell, deposit, withdraw, updatePrice procedures 
call depositAmount(20000, 6); 
call depositAmount(20000, 1); 
call updatePrice(2, 30); 
call buyStock('AAPL', 2, 6); 
call buyStock('GOOG', 3, 5); 
call updatePrice(5, 100);
call buyStock('LB', 4, 1); 
call depositAmount(20000, 5); 
call buyStock('EA', 1, 2); 
call buyStock('VM', 3, 3); 
call updatePrice(5, 5);
call depositAmount(20000, 4); 
call sellStock('EA', 1, 2); 
call sellStock('VM', 2, 3); 
call withdrawAmount(1000, 1); 
call updatePrice(7, 25);
call withdrawAmount(1500, 2); 
call withdrawAmount(3000, 1); 
call withdrawAmount(100, 3); 
call depositAmount(500, 4); 

select * from transactions;
