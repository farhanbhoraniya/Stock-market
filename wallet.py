import json
from flask import Blueprint, request, session
from dbConnection import DBConnection
from helper import get_user_wallet, get_wallet_by_id

wallet = Blueprint('wallet', __name__)

@wallet.route('/wallet', methods=['POST'])
def create_wallet():
    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400
    user = request_body.get('user')
    
    if not user:
        return {'error': 'User ID is required'}, 400

    if not session['logged_in'] or session['user']["id"] != user:
        return {'error': 'Authentication failed'}, 401

    wallet_amount = 0

    wallet = get_user_wallet(user)

    if wallet:
        return {'error': 'Wallet for user already exists'}, 400

    wallet_create_query = """insert into wallet (owner, wallet_amount) VALUES ('{}', '{}')""".format(user, wallet_amount)

    db = DBConnection()
    try:
        db.cursor.execute(wallet_create_query)
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        print(e)
        return {"error": "Error while creating the wallet for user"}, 500

    wallet = get_user_wallet(user)

    return wallet

@wallet.route('/wallet/<id>', methods=['GET'])
def get_wallet(id):

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    wallet = get_wallet_by_id(id)

    if not wallet:
        return {'error': 'Wallet does not exists'}, 404

    if not session['logged_in'] or session['user']["id"] != wallet['owner']:
        return {'error': 'Authentication failed'}, 401

    return wallet

@wallet.route('/wallet/<id>', methods=['PUT'])
def update_wallet(id):

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    wallet = get_wallet_by_id(id)

    if not wallet:
        return {'error': 'Wallet does not exists'}, 404

    if not session['logged_in'] or session['user']["id"] != wallet['owner']:
        return {'error': 'Authentication failed'}, 401

    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400

    wallet_amount = request_body.get('wallet_amount')

    if wallet_amount is None:
        return {'error': 'Missing required field'}, 400

    wallet_update_query = """update wallet set wallet_amount={} where id={}""".format(wallet_amount, id)

    db = DBConnection()
    try:
        db.cursor.execute(wallet_update_query)
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        print(e)
        return {"error": "Error while updating the wallet for user"}, 500

    wallet = get_wallet_by_id(id)
    return wallet
