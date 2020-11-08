import json
import re
import bcrypt
from flask import Blueprint, request, session
from dbConnection import DBConnection

users = Blueprint('users', __name__)

@users.route('/register', methods=["GET", "POST"])
def register():
    session['logged_in'] = False
    request_body = json.loads(request.data)

    email = request_body.get('email')
    if not email:
        return {"error": "Email is required"}
    db = DBConnection.Instance()
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
        return {"error": "Error while registring the user"}, 400

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

    db = DBConnection.Instance()
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

# @users.route('/test', methods=['GET'])
# def test2():
#     print(session)
#     try:

#         if session['logged_in']:
#             print(session['user'])
#             return "Authorized"
#     except:
#         pass

#     return "Unauthorized", 401