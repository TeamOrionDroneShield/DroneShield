import sqlite3,json


def nfzones(city):
    #The db path has to be fixed in order to work under different Operating Systems
    conn = sqlite3.connect("C:\\Users\\Federico\\PycharmProjects\\drone_server\\drone_shield_server\\dronedb.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM NFZONE WHERE CITY = :city''', {"city":city})
    conn.commit()
    data = dict()
    nfzones = []
    data['data'] = nfzones
    for elem in c.fetchall():
        elem_data = dict()
        elem_data['shape'] = elem[1]
        elem_data['lat'] = elem[2]
        elem_data['lng'] = elem[3]
        elem_data['radius'] = elem[4]
        elem_data['begin_at'] = elem[5]
        elem_data['end_at'] = elem[6]
        elem_data['name'] = elem[7]
        elem_data['city'] = elem[8]
        elem_data['level'] = elem[9]
        nfzones.append(elem_data)
    conn.close()
    return str(json.dumps(data))
