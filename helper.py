from dbConnection import DBConnection

def get_user_wallet(id):
    db = DBConnection()
    wallet_query = "select * from wallet where owner={}".format(id)

    db.cursor.execute(wallet_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    wallet = {
        'id': data[0],
        'owner': data[1],
        'wallet_amount': data[2]
    }
    
    return wallet

def get_wallet_by_id(id):
    db = DBConnection()
    wallet_query = "select * from wallet where id={}".format(id)

    db.cursor.execute(wallet_query)
    data = db.cursor.fetchone()

    if not data:
        return 

    wallet = {
        'id': data[0],
        'owner': data[1],
        'wallet_amount': data[2]
    }
    
    return wallet