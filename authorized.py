import sqlite3


def authorized(userid):
    conn = sqlite3.connect("C:\\Users\\Federico\\PycharmProjects\\drone_server\\socialdb.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM User WHERE ID = :userid''',{"userid":userid})
    conn.commit()
    if len(c.fetchall()) == 1:
        return True
    else:
        return False