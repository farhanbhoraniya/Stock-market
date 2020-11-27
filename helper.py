from dbConnection import DBConnection

def get_user_wallet(id):
    db = DBConnection()
    wallet_query = "select * from wallet where owner={}".format(id)

    db.cursor.execute(wallet_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    wallet = {
        'id': data[0],
        'owner': data[1],
        'wallet_amount': data[2]
    }
    
    return wallet

def get_wallet_by_id(id):
    db = DBConnection()
    wallet_query = "select * from wallet where id={}".format(id)

    db.cursor.execute(wallet_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    wallet = {
        'id': data[0],
        'owner': data[1],
        'wallet_amount': data[2]
    }
    
    return wallet

def get_company_by_code(code):
    db = DBConnection()
    company_query = "select * from company where code_name='{}'".format(code)

    db.cursor.execute(company_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    company = {
        'id': data[0],
        'name': data[1],
        'code_name': data[2],
        'total_stocks': data[3],
        'address': data[4],
        'about': data[5]
    }

    return company

def get_company_by_id(id):
    db = DBConnection()
    company_query = "select * from company where id={}".format(id)

    db.cursor.execute(company_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    company = {
        'id': data[0],
        'name': data[1],
        'code_name': data[2],
        'total_stocks': data[3],
        'address': data[4],
        'about': data[5]
    }

    return company

def get_stock_by_id(id):
    db = DBConnection()
    stock_query = """select stock.id, current_price, available_stocks, 
    company.id as companyID, name, total_stocks, address, about, code_name from stock join company on stock.company=company.id 
    where stock.id={}""".format(id)

    db.cursor.execute(stock_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    stock = {
        "id": data[0],
        "current_price": data[1],
        "available_stocks": data[2],
        "company": data[3],
        "name": data[4],
        "total_stocks": data[5],
        "address": data[6],
        "about": data[7],
        "code_name": data[8]
    }

    return stock

def get_stock_by_company(id):
    db = DBConnection()
    stock_query = """select stock.id, current_price, available_stocks, 
    company.id as companyID, name, total_stocks, address, about, code_name from company join stock where stock.company='{}'""".format(id)

    db.cursor.execute(stock_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    stock = {
        "id": data[0],
        "current_price": data[1],
        "available_stocks": data[2],
        "company": data[3],
        "name": data[4],
        "total_stocks": data[5],
        "address": data[6],
        "about": data[7],
        "code_name": data[8]
    }

    return stock
