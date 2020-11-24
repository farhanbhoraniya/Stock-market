from flask import Flask, request

from user import users
from wallet import wallet
from company import company
# from test import testprint

from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(users)
app.register_blueprint(wallet)
app.register_blueprint(company)
# app.register_blueprint(testprint)
app.run(debug=True)
