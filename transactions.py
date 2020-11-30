# SJSU CMPE 226 Fall 2020 TEAM 5
import json
import re
import bcrypt
from flask import Blueprint, request, session, jsonify
from dbConnection import DBConnection
from helper import get_user_wallet, get_wallet_by_id

transactions = Blueprint('transactions', __name__)

@transactions.route('/buy', methods=["GET", "POST"])
def buy():

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400
    
    user = request_body.get('user')
    print(user)
    
    if not user:
        return {'error': 'User ID is required'}, 400

    if not session.get('logged_in') or session['user']["id"] != user:
        return {'error': 'Authentication failed'}, 401
    
    try:
        stock = request_body['stock_id']
        qty = request_body['quantity']
    except:
        print("Missing required field")
        return {"error": "Missing required field"}, 400    
    print(stock)
    print(qty)
    
    db = DBConnection()
    stock_exists_query = "select * from company where code_name='{}'".format(stock)

    db.cursor.execute(stock_exists_query)
    data = db.cursor.fetchone()
    if not data:
        return {"error": "Stock assigned to buy does not exist"}, 400

    try:
        db.cursor.callproc("buyStock", (stock,qty,user))
    except:
        return {"error": "Buying Failed"}, 400    
    
    return {"Success": "Buying Request Completed Successfully"}, 200

@transactions.route('/sell', methods=["GET", "POST"])
def sell():

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400
    
    user = request_body.get('user')
    print(user)
    
    if not user:
        return {'error': 'User ID is required'}, 400

    if not session.get('logged_in') or session['user']["id"] != user:
        return {'error': 'Authentication failed'}, 401
    
    try:
        stock = request_body['stock_id']
        qty = request_body['quantity']
    except:
        print("Missing required field")
        return {"error": "Missing required field"}, 400    
    print(stock)
    print(qty)
    
    db = DBConnection()
    stock_exists_query = "select * from company where code_name='{}'".format(stock)

    db.cursor.execute(stock_exists_query)
    data = db.cursor.fetchone()
    if not data:
        return {"error": "Stock assigned to sell does not exist"}, 400

    try:
        db.cursor.callproc("sellStock", (stock,qty,user))
    except:
        return {"error": "Selling Failed"}, 400    
    
    return {"Success": "Selling Request Completed Successfully "}, 200

@transactions.route('/deposit', methods=["GET", "POST"])
def deposit():

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400
    
    user = request_body.get('user')
    print(user)
    
    if not user:
        return {'error': 'User ID is required'}, 400

    if not session.get('logged_in') or session['user']["id"] != user:
        return {'error': 'Authentication failed'}, 401
    
    try:
        dep_amt = request_body.get('deposit_amount')
    except:
        print("Missing required field")
        return {"error": "Missing required field"}, 400    

    print(dep_amt)
    if dep_amt <= 0:
        return {"error": "Deposit at least 1 dollar"}, 400

    db = DBConnection()
    data = get_user_wallet(user)
    if not data:
        return {"error": "There's no wallet related to this User"}, 400

    try:
        db.cursor.callproc("depositAmount", (dep_amt,user))
    except:
        return {"error": "Deposit Failed"}, 400    
    
    return {"Success": "Deposit Request Completed Successfully "}, 200

@transactions.route('/withdraw', methods=["GET", "POST"])
def withdraw():

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400
    
    user = request_body.get('user')
    print(user)
    
    if not user:
        return {'error': 'User ID is required'}, 400

    if not session.get('logged_in') or session['user']["id"] != user:
        return {'error': 'Authentication failed'}, 401
    
    try:
        wdr_amt = request_body['withdraw_amount']
    except:
        print("Missing required field")
        return {"error": "Missing required field"}, 400    

    print(wdr_amt)
    if wdr_amt <= 0:
        return {"error": "withdraw at least 1 dollar"}, 400

    db = DBConnection()
    data = get_user_wallet(user)
    if not data:
        return {"error": "There's no wallet related to this User"}, 400

    try:
        db.cursor.callproc("withdrawAmount", (wdr_amt,user))
    except:
        return {"error": "Withdraw Failed"}, 400    
    
    return {"Success": "Withdraw Request Completed Successfully "}, 200

@transactions.route('/transactions/<id>', methods=['GET'])
def get_txns(id):
    if not session.get('logged_in'):
        return {'error': 'Authentication failed'}, 401

    try:
        uid = int(id)
    except:
        print("Invalid user ID")
        return {"error": "Invalid ID"}, 400
    
    txn_query = "select * from transactions where user={}".format(uid)
    
    db = DBConnection()
    try:
        db.cursor.execute(txn_query)
        result = db.cursor.fetchall()
    except Exception as e:
        print(e)
        return {"error": "Error while getting the transactions"}, 500

    response = []
    for item in result:
        temp = {
        "id"    : item[0], 
        "type"  : item[1],
        "price" : item[2],
        "qty"   : item[3],
        "date_time": item[4],
        "amount": item[5],
        "user"  : item[6],
        "stock" : item[7]
        }
        response.append(temp)

    return jsonify(response)

@transactions.route('/portfolio/<id>', methods=['GET'])
def get_portfolio(id):
    
    try:
        uid = int(id)
        # request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid ID'}, 400
        
    if not session.get('logged_in') or session['user']['id'] != uid:
        return {'error': 'Authentication failed'}, 401
    # uid = request_body.get('id')
    print(uid)
    
    # if not uid:
    #     return {'error': 'User ID is required'}, 400

    portfolio_query = "select * from all_portfolio where USERID={}".format(uid)
    
    db = DBConnection()
    try:
        db.cursor.execute(portfolio_query)
        result = db.cursor.fetchall()
    except Exception as e:
        print(e)
        return {"error": "Error while getting the portfolio"}, 500

    response = []    
    if len(result) > 0:
        u =  {"User ID"          : result[0][0],
             "User Firstname"   : result[0][1],
             "Buying Power"     : result[0][6]};
        response.append(u)

        for item in result:
            temp = {
            "Ticker" : item[2],
            "Share Price" : item[3],
            "No. of Shares owned": item[4],
            "Value of these shares": item[5]
            }
            response.append(temp)
    else:
        profile_query = "select * from all_profiles where USERID={}".format(uid)
        try:
            db.cursor.execute(profile_query)
            result = db.cursor.fetchone()
        except Exception as e:
            print(e)
            return {"error": "Error while getting the user profiles"}, 500
        u =  {"User ID"          : result[0], 
             "User Firstname"   : result[1],
             "Buying Power"     : result[2]};
        response.append(u)
        
    return jsonify(response)
    