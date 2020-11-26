import json
from flask import Blueprint, request, session, jsonify
from dbConnection import DBConnection
from helper import get_stock_by_id, get_stock_by_company

stock = Blueprint('stock', __name__)

@stock.route('/stock', methods=['POST'])
def create_stock():
    if not session['logged_in'] or session['user']["type"] != "admin":
        return {'error': 'Authentication failed'}, 401
    
    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400
    
    company = request_body.get('company')

    if company is None:
        return {'error': 'Missing required field'}, 400

    current_price = request_body.get('current_price', 0)
    available_stocks = request_body.get('available_stocks', 0)

    stock = get_stock_by_company(company)

    if stock:
        return {'error': 'Company stock already exists'}, 400 

    stock_create_query = """insert into stock (company, current_price, available_stocks) VALUES
    ({company}, {current_price}, {available_stocks})""".format(company=company, current_price=current_price, 
                                                               available_stocks=available_stocks)

    db = DBConnection()
    try:
        db.cursor.execute(stock_create_query)
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        print(e)
        return {"error": "Error while creating the stock"}, 500

    stock = get_stock_by_company(company)

    return stock

@stock.route('/stocks', methods=['GET'])
def get_stocks():
    if not session['logged_in']:
        return {'error': 'Authentication failed'}, 401

    stock_query = "select * from stock"

    db = DBConnection()
    try:
        db.cursor.execute(stock_query)
        result = db.cursor.fetchall()
    except Exception as e:
        print(e)
        return {"error": "Error while getting the companies"}, 500

    response = []

    for item in result:
        temp = {
            "id": item[0],
            "company": item[1],
            "current_price": item[2],
            "available_stocks": item[3]
        }
        response.append(temp)

    return jsonify(response)

@stock.route('/stock/<id>', methods=['GET'])
def get_stock_id(id):
    if not session['logged_in']:
        return {'error': 'Authentication failed'}, 401

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    stock = get_stock_by_id(id)

    if not stock:
        return {'error': 'Stock does not exists'}, 404

    return stock

@stock.route('/stock/<id>', methods=['PUT'])
def update_stock_by_id(id):
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
    
    stock = get_stock_by_id(id)

    if not stock:
        return {'error': 'Stock does not exists'}, 404

    db = DBConnection()

    current_price = request_body.get('current_price')
    available_stocks = request_body.get('available_stocks')

    if not current_price and not available_stocks:
        return {'error': 'Missing required fields'}, 400

    if current_price and available_stocks:
        return {'error': 'You can update only one parameter at a time'}, 400

    if current_price:
        db.cursor.callproc("updatePrice", (id, current_price))
    else:
        update_query = "update stock set available_stocks={} where id={}".format(available_stocks, id)
        try:
            db.cursor.execute(update_query)
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            print(e)
            return {'error': "Error while updating the data"}, 500
    
    stock = get_stock_by_id(id)

    return stock