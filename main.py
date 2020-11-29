import requests
import json
import logging
from getpass import getpass
from beautifultable import BeautifulTable

base_url = "http://localhost:5000"
logged_in = False
user_details = None
cookies = {}
LOG_FILENAME='applicaiton.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def register():
    logging.info("Registering new user")
    email = input("Enter email ")
    fname = input("Enter first name ")
    lname = input("Enter last name ")
    password = getpass("Enter password ")
    user_type = "regular"

    data = {
        "email": email,
        "first_name": fname,
        "last_name": lname,
        "password": password,
        "type": user_type
    }

    url = base_url + "/register"

    r = requests.post(url, data=json.dumps(data))

    if r.status_code == 200:
        print("User registered. Please login!!!")
        return
    else:
        resp = json.loads(r.text)
        print("Error:", resp['error'])

def login():
    print("-------------------")
    print("Enter Email and Password")
    email = input("Enter Email ")
    password = getpass("Enter Password ")

    data = {
        "email": email,
        "password": password
    }

    url = base_url + "/login"
    
    r = requests.post(url, data=json.dumps(data))
    if r.status_code == 401:
        print("Authentication Failed. Please try again")
        return None, None
    elif r.status_code == 200:
        print("Logged in successfully")
        logging.info("User with email " + email + "logged in successfully")
        headers = r.headers
        cookies = headers['Set-Cookie']
        return json.loads(r.text), cookies

def get_all_companies():
    logging.info("Getting all companies")
    url = base_url + "/companies"
    r = requests.get(url, cookies=cookies)

    if r.status_code == 200:
        data = json.loads(r.text)
        table = BeautifulTable()
        
        for item in data:
            table.rows.append([item['id'], item['name'], item['code_name'], item['about'], item['address'], item['total_stocks']])

        table.columns.header = ["ID", "Name", "Code Name", "About", "Address", "Total Stocks"]
        print(table)
    else:
        print("Error while getting the companies")

def get_company_by_id():
    company_id = input("Enter company ID ")
    logging.info("Getting company with ID " + str(company_id))
    url = base_url + "/company/" + company_id
    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        data = json.loads(r.text)
        url = base_url + "/company/{}/stock".format(company_id)
        r = requests.get(url, cookies=cookies)
        print("-------------------")
        for key, value in data.items():
            print(key, ":", value)

        if r.status_code == 200:
            stock_data = json.loads(r.text)
            for key, value in stock_data.items():
                print(key, ":", value)
    else:
        print("Error while getting the companies")

def get_company_by_code():
    company_code = input("Enter company code ")
    url = base_url + "/company/code/" + company_code
    logging.info("Getting company with code " + str(company_code))
    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        data = json.loads(r.text)
        company_id = data['id']
        url = base_url + "/company/{}/stock".format(company_id)
        r = requests.get(url, cookies=cookies)
        print("-------------------")
        for key, value in data.items():
            print(key, ":", value)

        if r.status_code == 200:
            stock_data = json.loads(r.text)
            for key, value in stock_data.items():
                print(key, ":", value)
    else:
        print("Error while getting the companies")

def admin_company_operations():
    
    while True:
        print("-------------------")
        print("Admin operations for company")
        print("1. Get all companies")
        print("2. Get company by ID")
        print("3. Get company by code")
        print("4. Create compnay")
        print("5. Update compnay")
        print("0. Go back")
        input_value = input("Select option ")

        if input_value == "1":
            get_all_companies()   
        elif input_value == "2":
            get_company_by_id()
        elif input_value == "3":
            get_company_by_code()
        elif input_value == "4":
            print("-------------------")
            name = input("Company Name ")
            code = input("Unique company code ")
            total_stocks = 0
            address = input("Address of a company ")
            about = input("About company")
            logging.info("Creating company with name " + name)
            if not total_stocks:
                total_stocks = 0
            else:
                try:
                    total_stocks = int(total_stocks)
                except Exception as e:
                    print("Invalid input value")
                    logging.error(e)
                    continue
            data = {
                'name': name,
                'about': about,
                'address': address,
                'total_stocks': total_stocks,
                'code': code
            }

            url = base_url + "/company"
            r = requests.post(url, data=json.dumps(data), cookies=cookies)
            data = json.loads(r.text)
            if r.status_code == 200:
                print("Company created")
            else:
                print("Error", data.get('error'))             
        elif input_value == "5":
            print("-------------------")
            id = input("Company ID ")
            name = input("Company Name ")
            total_stocks = input("Total stokcs of a company ")
            address = input("Address of a company ")
            about = input("About company")
            logging.info("Updating the company with ID " + str(id))
            try:
                id = int(id)
            except Exception as e:
                print("Invalid ID")
                logging.error(e)
                continue

            if total_stocks == '':
                total_stocks = None
            else:
                try:
                    total_stocks = int(total_stocks)
                except Exception as e:
                    print("Invalid input value")
                    logging.error(e)
                    continue

            data = {}
            if name:
                data['name'] = name

            if about:
                data['about'] = about

            if address:
                data['address'] = address

            if total_stocks is not None:
                data['total_stocks'] = total_stocks

            url = base_url + "/company/" + str(id)
            
            r = requests.put(url, data=json.dumps(data), cookies=cookies)            
            data = json.loads(r.text)

            if r.status_code == 200:
                print("Company updated")
            else:
                print("Error", data.get('error'))
        elif input_value == "0":
            break
        else:
            print("Invalid value")
            continue

def get_all_stocks():
    logging.info("Getting all stocks")
    url = base_url + "/stocks"
    r = requests.get(url, cookies=cookies)
    
    if r.status_code == 200:
        data = json.loads(r.text)
        table = BeautifulTable()
        
        for item in data:
            table.rows.append([item['id'], item['company'], item['name'], item['code_name'], item['current_price'], item['available_stocks'], item['total_stocks'], item['about'], item['address']])

        table.columns.header = ["ID", "Company ID", "Name", "Code Name", "Current Price", "Avilable Stocks", "Total Stocks", "About", "Address"]
        print(table)
    else:
        print("Error while getting the stocks")

def get_stock_by_id():
    stock_id = input("Enter stock ID ")
    url = base_url + "/stock/" + stock_id
    logging.info("Getting stock with ID " + str(stock_id))
    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        data = json.loads(r.text)
        print("-------------------")
        for key, value in data.items():
            print(key, ":", value)

    else:
        print("Error while getting the stock")

def get_company_stock():
    company_id = input("Enter company ID ")
    url = base_url + "/company/{}/stock".format(company_id)
    logging.info("Getting stock of company " + str(company_id))
    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        data = json.loads(r.text)
        print("-------------------")
        for key, value in data.items():
            print(key, ":", value)

    else:
        print("Error while getting the company stock")
    pass

def admin_stock_operations():
    while True:
        print("-------------------")
        print("Admin operations for stock")
        print("1. Get all stock")
        print("2. Get stock by ID")
        print("3. Get company stock")
        print("4. Create stock")
        print("5. Update stock by id")
        print("6. Update stock by company")
        print("0. Go back")
        input_value = input("Select option ")

        if input_value == "1":
            get_all_stocks()
        elif input_value == "2":
            get_stock_by_id()
        elif input_value == "3":
            get_company_stock()
        elif input_value == "4":
            print("-------------------")
            company = input("Enter company ID ")
            current_price = input("Enter current price ")
            available_stocks = input("Enter available stocks ")
            logging.info("Getting company with ID " + str(company))
            try:
                company = int(company)
            except Exception as e:
                print("Invalid value")
                logging.error(e)
                continue

            if not current_price:
                current_price = 0
            else:
                try:
                    current_price = int(current_price)
                except Exception as e:
                    print("Invalid value")
                    logging.error(e)
                    continue

            if not available_stocks:
                available_stocks = 0
            else:
                try:
                    available_stocks = int(available_stocks)
                except Exception as e:
                    print("Invalid value")
                    logging.error(e)
                    continue

            data = {
                "company": company,
                "current_price": current_price,
                "available_stocks": available_stocks
            }

            url = base_url + "/stock"

            r = requests.post(url, data=json.dumps(data), cookies=cookies)

            if r.status_code == 200:
                print("Stock created")
            else:
                data = json.loads(r.text)
                print("Error:", data['error'])
            
        elif input_value == "5":
            
            stock_id = input("Enter stock ID ")
            print("-------------------")
            print("Select field to update")
            print("1. Update available stocks")
            print("2. Update current price")
            print("0. Go back")

            stock_input = input("Select option ")

            if stock_input == "1":
                logging.info("Updating available stocks for stock " + str(stock_id))
                available_stocks = input("Available stocks ")

                try:
                    available_stocks = int(available_stocks)
                except Exception as e:
                    print("Invalid value")
                    logging.error(e)
                    continue
                
                data = {
                    "available_stocks": available_stocks
                }

                url = base_url + "/stock/" + stock_id

                r = requests.put(url, data=json.dumps(data), cookies=cookies)

                if r.status_code == 200:
                    print("Stock updated")
                else:
                    data = json.loads(r.text)
                    print("Error:", data['error'])

            elif stock_input == "2":
                logging.info("Updating current price for stock " + str(stock_id))
                current_price = input("Current price ")

                try:
                    current_price = int(current_price)
                except Exception as e:
                    print("Invalid value")
                    logging.error(e)
                    continue
                
                data = {
                    "current_price": current_price
                }

                url = base_url + "/stock/" + stock_id

                r = requests.put(url, data=json.dumps(data), cookies=cookies)

                if r.status_code == 200:
                    print("Stock updated")
                else:
                    data = json.loads(r.text)
                    print("Error:", data['error'])
            elif stock_input == "0":
                pass
            else:
                print("Invalid option")
            
        elif input_value == "6":
            company_id = input("Enter company ID ")
            print("-------------------")
            print("Select field to update")
            print("1. Update available stocks")
            print("2. Update current price")
            print("0. Go back")

            stock_input = input("Select option ")

            if stock_input == "1":
                logging.info("Updating available stocks for company " + str(company_id))
                available_stocks = input("Available stocks ")

                try:
                    available_stocks = int(available_stocks)
                except Exception as e:
                    print("Invalid value")
                    logging.error(e)
                    continue
                
                data = {
                    "available_stocks": available_stocks
                }

                url = base_url + "/company/{}/stock".format(company_id)

                r = requests.put(url, data=json.dumps(data), cookies=cookies)

                if r.status_code == 200:
                    print("Stock updated")
                else:
                    data = json.loads(r.text)
                    print("Error:", data['error'])

            elif stock_input == "2":
                logging.info("Updating current price for company " + str(company_id))
                current_price = input("Current price ")

                try:
                    current_price = int(current_price)
                except Exception as e:
                    print("Invalid value")
                    logging.error(e)
                    continue
                
                data = {
                    "current_price": current_price
                }

                url = base_url + "/company/{}/stock".format(company_id)

                r = requests.put(url, data=json.dumps(data), cookies=cookies)

                if r.status_code == 200:
                    print("Stock updated")
                else:
                    data = json.loads(r.text)
                    print("Error:", data['error'])
            elif stock_input == "0":
                pass
            else:
                print("Invalid option")
        elif input_value == "0":
            break
        else:
            print("Invalid value")
            continue

def user_company_operatios():
    while True:
        print("-------------------")
        print("User operations for company")
        print("1. Get all companies")
        print("2. Get company by ID")
        print("3. Get company by code")
        print("0. Go back")
        input_value = input("Select option ")

        if input_value == "1":
            get_all_companies()   
        elif input_value == "2":
            get_company_by_id()
        elif input_value == "3":
            get_company_by_code()
        elif input_value == "0":
            break
        else:
            print("Invalid value")
            continue

def user_stock_operations():
    while True:
        print("-------------------")
        print("Admin operations for stock")
        print("1. Get all stock")
        print("2. Get stock by ID")
        print("3. Get company stock")
        print("4. Get stock price history")
        print("0. Go back")
        input_value = input("Select option ")

        if input_value == "1":
            get_all_stocks()
        elif input_value == "2":
            get_stock_by_id()
        elif input_value == "3":
            get_company_stock()
        elif input_value == "4":
            stock_id = input("Stock ID ")
            logging.info("Getting stock price history for stock " + str(stock_id))
            url = base_url + "/stock/{}/price_history".format(stock_id)
            r = requests.get(url, cookies=cookies)

            if r.status_code == 200:
                response = json.loads(r.text)

                table = BeautifulTable()
        
                for item in response:
                    table.rows.append([item['datetime'], item['price']])

                table.columns.header = ["Date Time", "Price"]
                print(table)
            else:
                print("Error while getting the price history")
        elif input_value == "0":
            break
        else:
            print("Invalid value")
            continue

def user_transactions():
    user_id = user_details['id']
    url = base_url + "/transactions/{}".format(user_id)
    r = requests.get(url, cookies=cookies)
    try:
        data = json.loads(r.text)
    except Exception as e:
        logging.error(e)
        print("Error while getting the transactions")
        return
    if r.status_code == 200:
        table = BeautifulTable()
        
        for item in data:
            table.rows.append([item['id'], item['date_time'], item['user'], item['type'], item['stock'], item['qty'], item['price'], item['amount']])

        table.columns.header = ["ID", "Date Time", "User", "Type", "Stock", "Quantity", "Price", "Amount"]
        print(table)
    else:
        print("Error", data['error'])

def user_wallet():
    while True:
        print("-------------------")
        print("1. Create wallet")
        print("2. Check user wallet balance")
        print("3. View user portfolio")
        print("4. Deposit amount")
        print("5. Withdraw amount")
        print("6. Buy stocks")
        print("7. Sell stocks")
        print("0. Go back")

        input_value = input("Select option ")
        if input_value == "1":
            user_id = user_details['id']
            url = base_url + '/wallet'
            data = {
                'user': user_id
            }

            r = requests.post(url, data=json.dumps(data), cookies=cookies)

            try:
                resp = json.loads(r.text)
            except Exception as e:
                print("Error while creating the wallet")
                logging.error(e)
                continue

            if r.status_code == 200:
                print("Wallet created")
            else:
                print("Error while creating the wallet")

        elif input_value == "2":
            user_id = user_details['id']
            url = base_url + "/user/{}/wallet".format(user_id)

            r = requests.get(url, cookies=cookies)
            try:
                data = json.loads(r.text)
            except Exception as e:
                logging.error(e)
                print("Error while checking the user wallet balace")
                continue
            
            if r.status_code == 200:
                print("Wallet balance:", data.get('wallet_amount'))
            else:
                logging.error('Error ' + data['error'])
                continue
        elif input_value == "3":
            user_id = user_details['id']
            url = base_url + "/portfolio/{}".format(user_id)

            r = requests.get(url, cookies=cookies)

            try:
                response = json.loads(r.text)
            except Exception as e:
                logging.error(e)
                print("Error while getting the portfolio")
                continue

            if r.status_code == 200:
                if len(response) < 0:
                    continue
                user = response[0]
                print("-------------------")
                print("User ID:", user['User ID'])
                print("User Name:", user['User Firstname'])
                print('Buying Power:', user['Buying Power'])

                table = BeautifulTable()
                data = response[1:]
                for item in data:
                    table.rows.append([item['Ticker'], item['Share Price'], item['No. of Shares owned'], item['Value of these shares']])

                table.columns.header = ["Ticker", "Share Price", 'No. of Shares owned', "Value of these shares"]
                print(table)
            else:
                print("Error ", response['error'])
            
            pass
        elif input_value == "4":
            user_id = user_details['id']
            try:
                deposit_amount = int(input("Enter amount to deposit "))
            except Exception as e:
                print("Invalid amount")
                logging.error(e)
                continue
            
            url = base_url + "/deposit"

            data = {
                "user": user_id,
                "deposit_amount": deposit_amount
            }

            r = requests.post(url, data=json.dumps(data), cookies=cookies)

            try:
                response = json.loads(r.text)
            except Exception as e:
                logging.error(e)
                print("Error while depositing the amount")
                continue

            if r.status_code == 200:
                print("Amount deposited")
            else:
                print("Error:", response['error'])
            
        elif input_value == "5":
            user_id = user_details['id']
            try:
                deposit_amount = int(input("Enter amount to withdraw "))
            except Exception as e:
                print("Invalid amount")
                logging.error(e)
                continue
            
            url = base_url + "/withdraw"

            data = {
                "user": user_id,
                "withdraw_amount": deposit_amount
            }

            r = requests.post(url, data=json.dumps(data), cookies=cookies)

            try:
                response = json.loads(r.text)
            except Exception as e:
                logging.error(e)
                print("Error while withdrawing the amount")
                continue

            if r.status_code == 200:
                print("Amount withdrawed")
            else:
                print("Error:", response['error'])
        
        elif input_value == "6":
            code_name = input("Code name of the stock you want to buy ")
            try:
                quantity = int(input("Quantity "))
            except Exception as e:
                logging.error(e)
                print("Invalid input")
                continue

            user_id = user_details['id']

            data = {
                'user': user_id,
                "stock_id": code_name,
                "quantity": quantity
            }

            url = base_url + "/buy"

            r = requests.post(url, data=json.dumps(data), cookies=cookies)

            try:
                response = json.loads(r.text)
            except Exception as e:
                logging.error(e)
                print("Error while buying the stocks")
                continue

            if r.status_code == 200:
                print("Stock bought successfully")
            else:
                print("Error", response['error'])
            
        elif input_value == "7":
            code_name = input("Code name of the stock you want to sell ")
            try:
                quantity = int(input("Quantity "))
            except Exception as e:
                logging.error(e)
                print("Invalid input")
                continue

            user_id = user_details['id']

            data = {
                'user': user_id,
                "stock_id": code_name,
                "quantity": quantity
            }

            url = base_url + "/sell"

            r = requests.post(url, data=json.dumps(data), cookies=cookies)

            try:
                response = json.loads(r.text)
            except Exception as e:
                logging.error(e)
                print("Error while selling the stocks")
                continue 
            print(response, r.status_code)
            if r.status_code == 200:
                print("Stock sold successfully")
            else:
                print("Error", response['error'])
        elif input_value == "0":
            break
        else:
            print("Invalid input")
            continue
def logout():
    global cookies
    global logged_in

    url = base_url + "/logout"
    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        print("Logged out!!!")
        logged_in = False

while True:

    if not logged_in:
        print("-------------------")
        print("Welcome to stock market")
        print("Please Register or Login")
        print("1. To Register")
        print("2. To Login")
        print("0. Exit")
        
        input_value = input("Select option ")

        if input_value == str(1):
            register()
        elif input_value == str(2):
            user_details, cookie = login()
            if user_details is not None:
                logged_in = True
                cookies['session'] = cookie.split('=')[1]
            
        elif input_value == str(0):
            # infoLog.close()
            # logger.removeHandler(infoLog)
            break
        else:
            print("Invalid input")
            continue
    else:
        if user_details['type'] == "admin":
            print("-------------------")
            print("You are logged in as an admin")
            print("1. Company")
            print("2. Stock")
            print("0. Log out")
            input_value = input("Select option ")

            if input_value == str(1):
                admin_company_operations()
            elif input_value == str(2):
                admin_stock_operations()
            elif input_value == str(0):
                logout()
            else:
                print("Invalid input")
                continue
        else:
            print("-------------------")
            print("You are logged in as a normal user")
            print("1. Company")
            print("2. Stock")
            print("3. User Transactions")
            print("4. User Wallet")
            print("0. Log out")
            input_value = input("Select option ")
            
            if input_value == str(1):
                user_company_operatios()
            elif input_value == str(2):
                user_stock_operations()
            elif input_value == str(3):
                user_transactions()
            elif input_value == str(4):
                user_wallet()
            elif input_value == str(0):
                logout()
            else:
                print("Invalid input")
                continue
