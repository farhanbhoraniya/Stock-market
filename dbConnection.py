import mysql.connector
import config

class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)

@Singleton
class DBConnection(object):

    def __init__(self):
        self.conn = mysql.connector.connect(user=config.MYSQL_USERNAME, password=config.MYSQL_PASSWORD, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
        self.cursor = self.conn.cursor()
