import requests
import json
from getpass import getpass
from beautifultable import BeautifulTable

base_url = "http://localhost:5000"
logged_in = False
user_details = None
cookies = {}

def register():
    pass

def login():
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
        headers = r.headers
        cookies = headers['Set-Cookie']
        return json.loads(r.text), cookies

def get_all_companies():
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
    url = base_url + "/company/" + company_id
    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        data = json.loads(r.text)
        url = base_url + "/company/{}/stock".format(company_id)
        r = requests.get(url, cookies=cookies)
        
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
    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        data = json.loads(r.text)
        company_id = data['id']
        url = base_url + "/company/{}/stock".format(company_id)
        r = requests.get(url, cookies=cookies)
        
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
            name = input("Company Name ")
            code = input("Unique company code ")
            total_stocks = input("Total stokcs of a company ")
            address = input("Address of a company ")
            about = input("About company")

            if not total_stocks:
                total_stocks = 0
            else:
                try:
                    total_stocks = int(total_stocks)
                except:
                    print("Invalid input value")
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
            id = input("Company ID ")
            name = input("Company Name ")
            total_stocks = input("Total stokcs of a company ")
            address = input("Address of a company ")
            about = input("About company")

            try:
                id = int(id)
            except:
                print("Invalid ID")
                continue

            if not total_stocks:
                total_stocks = None
            else:
                try:
                    total_stocks = int(total_stocks)
                except:
                    print("Invalid input value")
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

            url = base_url + "/company/" + id
            r = requests.post(url, data=json.dumps(data), cookies=cookies)
            data = json.loads(r.text)
            if r.status_code == 200:
                print("Company created")
            else:
                print("Error", data.get('error'))
        elif input_value == "0":
            break
        else:
            print("Invalid value")
            continue

def admin_stock_operations():
    pass

def user_profile():
    pass

def user_company_operatios():
    while True:
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
    pass

def user_transactions():
    pass

def user_wallet():
    pass

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
        print("Welcome to stock market")
        print("Please Register or Login")
        print("1. To Register")
        print("2. To Login")
        
        input_value = input("Select option ")

        if input_value == str(1):
            register()
        elif input_value == str(2):
            user_details, cookie = login()
            if user_details is not None:
                logged_in = True
                cookies['session'] = cookie.split('=')[1]
            # print(cookies)
        else:
            print("Invalid input")
            continue
    else:
        if user_details['type'] == "admin":
            print("You are logged in as an admin")
            print("1. Company")
            print("2. Stock")
            print("3. Update Profile")
            print("4. Log out")
            input_value = input("Select option ")

            if input_value == str(1):
                admin_company_operations()
            elif input_value == str(2):
                admin_stock_operations()
            elif input_value == str(3):
                user_profile()
            elif input_value == str(4):
                logout()
            else:
                print("Invalid input")
                continue
        else:
            print("You are logged in as a normal user")
            print("1. Company")
            print("2. Stock")
            print("3. User Transactions")
            print("4. User Wallet")
            print("5. Update Profile")
            print("6. Log out")
            input_value = input("Select option ")
            
            if input_value == str(1):
                user_company_operatios()
            elif input_value == str(2):
                user_stock_operations()
            elif input_value == str(3):
                user_transactions()
            elif input_value == str(4):
                user_wallet()
            elif input_value == str(5):
                user_profile()
            elif input_value == str(6):
                logout()
            else:
                print("Invalid input")
                continue

