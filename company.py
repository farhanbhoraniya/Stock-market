import json
from flask import Blueprint, request, session, jsonify
from dbConnection import DBConnection
from helper import get_company_by_code, get_company_by_id, get_stock_by_company

company = Blueprint('company', __name__)

@company.route('/company', methods=['POST'])
def create_company():
    
    if not session['logged_in'] or session['user']["type"] != "admin":
        return {'error': 'Authentication failed'}, 401

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400

    name = request_body.get('name')
    code_name = request_body.get('code')

    if name is None or code_name is None:
        return {'error': 'Missing required field'}, 400

    company = get_company_by_code(code_name)

    if company:
        return {'error': 'Company code already used'}, 400

    total_stocks = request_body.get('total_stocks', 0)
    address = request_body.get('address', '')
    about = request_body.get('about', '')

    company_create_query = """insert into company (name, code_name, total_stocks, address, about) 
                            VALUES ('{name}', '{code_name}', {total_stocks}, '{address}', '{about}')""".format(name=name, 
                                                                                                        code_name=code_name, 
                                                                                                        total_stocks=total_stocks, 
                                                                                                        address=address, 
                                                                                                        about=about)

    db = DBConnection()
    try:
        db.cursor.execute(company_create_query)
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        print(e)
        return {"error": "Error while creating the company"}, 500

    company = get_company_by_code(code_name)

    return company

@company.route('/companies', methods=['GET'])
def get_companies():
    
    company_query = "select * from company"
    
    if not session['logged_in']:
        return {'error': 'Authentication failed'}, 401

    db = DBConnection()
    try:
        db.cursor.execute(company_query)
        result = db.cursor.fetchall()
    except Exception as e:
        print(e)
        return {"error": "Error while getting the companies"}, 500

    response = []

    for item in result:
        temp = {
            "id": item[0],
            "name": item[1],
            "code_name": item[2],
            "total_stocks": item[3],
            "address": item[4],
            "about": item[5]
        }
        response.append(temp)

    return jsonify(response)

@company.route('/company/<id>', methods=['GET'])
def get_company_id(id):                                                                                                 
    
    if not session['logged_in']:
        return {'error': 'Authentication failed'}, 401
    
    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    company = get_company_by_id(id)

    if not company:
        return {'error': 'Company does not exists'}, 404

    return company

@company.route('/company/code/<code>', methods=['GET'])
def get_company_code(code):                                                                                                 
    
    if not session['logged_in']:
        return {'error': 'Authentication failed'}, 401

    company = get_company_by_code(code)

    if not company:
        return {'error': 'Company does not exists'}, 404

    return company

@company.route('/company/<id>', methods=['PUT'])
def update_company(id):

    if not session['logged_in'] or session['user']["type"] != "admin":
        return {'error': 'Authentication failed'}, 401

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    company = get_company_by_id(id)

    if not company:
        return {'error': 'Company does not exists'}, 404

    update_string = ''

    if request_body.get('name'):
        update_string += "name='{}'".format(request_body['name'])
        

    if request_body.get('total_stocks'):
        update_string += "total_stocks={}".format(request_body['total_stocks'])

    if request_body.get('address'):
        if update_string:
            update_string += ", "
        update_string += "address='{}'".format(request_body['address'])

    if request_body.get('about'):
        if update_string:
            update_string += ", "
        update_string += "about='{}'".format(request_body['about'])

    if not update_string:
        return company
    else:
        update_string += ' '

    update_query = """Update company set {update} where id={id}""".format(update=update_string, id=id)
    print(update_query)
    db = DBConnection()
    try:
        db.cursor.execute(update_query)
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        print(e)
        return {"error": "Error while updating the company"}, 500

    company = get_company_by_id(id)

    return company

@company.route('/company/<id>/stock', methods=['GET'])
def get_company_stocks(id):
    if not session['logged_in']:
        return {'error': 'Authentication failed'}, 401

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    stock = get_stock_by_company(id)

    if not stock:
        return {'error': 'Stock does not exists'}, 404

    return stock

@company.route('/company/<id>/stock', methods=['PUT'])
def update_company_stocks(id):
    if not session['logged_in'] or session['user']["type"] != "admin":
        return {'error': 'Authentication failed'}, 401

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400
    
    stock = get_stock_by_company(id)

    if not stock:
        return {'error': 'Stock does not exists'}, 404
    stockId = stock['id']
    db = DBConnection()

    current_price = request_body.get('current_price')
    available_stocks = request_body.get('available_stocks')

    if not current_price and not available_stocks:
        return {'error': 'Missing required fields'}, 400

    if current_price and available_stocks:
        return {'error': 'You can update only one parameter at a time'}, 400

    if current_price:
        db.cursor.callproc("updatePrice", (stockId, current_price))
    else:
        update_query = "update stock set available_stocks={} where id={}".format(available_stocks, stockId)
        try:
            db.cursor.execute(update_query)
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            print(e)
            return {'error': "Error while updating the data"}, 500
    
    stock = get_stock_by_company(id)

    return stock
