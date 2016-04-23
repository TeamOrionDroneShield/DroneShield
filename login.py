import sqlite3
import hashlib
import json


def login_control(username, password):
    conn = sqlite3.connect("C:\\Users\\Federico\\PycharmProjects\\drone_server\\socialdb.db")
    c = conn.cursor()
    m = hashlib.sha512(username.encode())
    c.execute('''SELECT ID FROM Password p WHERE SHA512 = :pwd AND SHA512_USR = :sha_usr''',
              {"pwd": 'ewf', "sha_usr": 'qewq'})
    conn.commit()
    data = c.fetchone()
    check = len(data) == 1 
    conn.close()
    response = dict()
    response['status'] = 1 if check == True else 0
    result = json.dumps(response)
    print(result)
    return str(result)
