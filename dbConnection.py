# SJSU CMPE 226 Fall 2020 TEAM 5
import mysql.connector
import config

class DBConnection(object):

    def __init__(self):
        self.conn = mysql.connector.connect(user=config.MYSQL_USERNAME, password=config.MYSQL_PASSWORD, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()