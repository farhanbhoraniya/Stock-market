import json
from flask import Blueprint, request, session, jsonify
from dbConnection import DBConnection
from helper import get_stock_by_id

price_history = Blueprint('price_history', __name__)

@price_history.route("/stock/<id>/price_history")
def get_price_history(id):
    if not session.get('logged_in'):
        return {'error': 'Authentication failed'}, 401

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    stock = get_stock_by_id(id)

    if not stock:
        return {"error": 'Stock does not exists'}, 404

    price_history_query = "select datetime, price from price_history where stock={} ORDER BY datetime desc".format(id)

    db = DBConnection()
    db.cursor.execute(price_history_query)
    data = db.cursor.fetchall()

    response = []

    for item in data:
        temp = {}
        temp['datetime'] = item[0]
        temp['price'] = item[1]

        response.append(temp)

    return jsonify(response)
