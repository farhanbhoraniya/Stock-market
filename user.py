# SJSU CMPE 226 Fall 2020 TEAM 5
import json
import re
import bcrypt
from flask import Blueprint, request, session
from dbConnection import DBConnection
from helper import get_user_wallet

users = Blueprint('users', __name__)

@users.route('/register', methods=["GET", "POST"])
def register():
    session['logged_in'] = False
    
    try:
        request_body = json.loads(request.data)
    except:
        return {"error": 'Invalid request body'}, 400

    email = request_body.get('email')
    if not email:
        return {"error": "Email is required"}, 400
    db = DBConnection()
    email_exists_query = "select * from user where email='{}'".format(email)

    db.cursor.execute(email_exists_query)
    data = db.cursor.fetchone()
    if data:
        return {"error": "Email is already registered"}, 400
    
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return {"error": "Invalid email"}, 400

    try:
        fname = request_body['first_name']
        lname = request_body['last_name']
        password = request_body['password']
        user_type = request_body['type']
    except:
        print("Missing required field")
        return {"error": "Missing required field"}, 400
    
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    print(password)
    insert_query = """insert into user(fname, lname, email, password, type) 
                      values('{}', '{}', '{}', "{}", '{}')""".format(fname, lname, email, password, user_type)
    
    try:
        db.cursor.execute(insert_query)
        db.conn.commit()
    except Exception as e:
        db.conn.rollback()
        print(e)
        return {"error": "Error while registring the user"}, 500

    retrieve_query = "select id, fname, lname, email, type from user where email='{}'".format(email)
    db.cursor.execute(retrieve_query)
    user_data = db.cursor.fetchone()

    user_data_json = {}
    user_data_json['id'] = user_data[0]
    user_data_json['fname'] = user_data[1]
    user_data_json['lname'] = user_data[2]
    user_data_json['email'] = user_data[3]
    user_data_json['type'] = user_data[4]

    return user_data_json

@users.route('/login', methods=['POST'])
def login():
    try:
        request_body = json.loads(request.data)
    except:
        return {"error": "Invalid request body"}, 400

    try:
        email = request_body['email']
        password = request_body['password']
    except:
        print("Missing required field")
        return {"error": "Missing required field"}, 400

    db = DBConnection()
    email_exists_query = "select * from user where email='{}'".format(email)

    db.cursor.execute(email_exists_query)
    data = db.cursor.fetchone()

    if not data:
        return {'error': 'Invalid email or password'}, 401

    stored_pwd = data[4]
    if not bcrypt.checkpw(password.encode('utf-8'), stored_pwd.encode('utf-8')):
        print("Invalid password")
        return {'error': "Authentication failed"}, 401

    session['logged_in'] = True
    
    response = {
        "id": data[0],
        "fname": data[1],
        "lname": data[2],
        "email": data[3],
        "type": data[5]
    }
    session['user'] = response
    
    return response

@users.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in')
    session.pop('user')
    return {}

@users.route('/user/<id>')
def get_user(id):
    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400

    if not session.get('logged_in') or session['user']["id"] != id:
        return {'error': 'Authentication failed'}, 401

    db = DBConnection()
    user_query = "select * from user where id={}".format(id)
    db.cursor.execute(user_query)
    data = db.cursor.fetchone()

    if not data:
        return {'error': 'User does not exists'}, 404

    print(data)
    response = {
        "id": data[0],
        "fname": data[1],
        "lname": data[2],
        "email": data[3],
        "type": data[5]
    }

    return response

@users.route('/user/<id>/wallet')
def get_wallet(id):

    try:
        id = int(id)
    except:
        print("Invalid ID")
        return {"error": "Invalid ID"}, 400
    
    if not session.get('logged_in') or session['user']["id"] != id:
        return {'error': 'Authentication failed'}, 401
        
    wallet = get_user_wallet(id)

    if not wallet:
        return {'error': 'Wallet for user does not exists'}, 400
    
    return wallet
