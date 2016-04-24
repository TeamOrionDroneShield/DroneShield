import sqlite3

class Submit:
    def __init__(self, user_id=None, type=None):
        self._uid  = user_id
        self._type = type
        self._lat  = None
        self._lng  = None
        self._rad  = None
        self._des  = None
        self._lvl  = None

    def setPosition(self, latitude, longitude, radius=None):
        self._lat = latitude
        self._lng = longitude
        self._rad = radius

    def setDescription(self, level, description):
        self._lvl = level
        self._des = description

    def authorized(self):
        conn = sqlite3.connect("./socialdb.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM User WHERE ID = :userid''', {"userid": self._uid})
        conn.commit()
        if len(c.fetchall()) == 1:
            return True
        else:
            return False

    def settingDB(self):
        query = "INSERT INTO SUBMISSIONS(USER_ID, TYPE, LEVEL, LAT, LNG, RADIUS, DESCRIPTION) VALUES (?, ?, ?, ?, ?, ?, ?)"
        con = sqlite3.connect(r"./dronedb.db")
        cur = con.cursor()

        params = (self._uid, self._type, self._lvl, self._lat, self._lng, self._rad, self._des)
        cur.execute(query, params)
        con.commit()
        con.close()

    def searchingDB(self, lat, lng):
        self._sub_dict = dict()
        query = "SELECT * FROM OBSTACLES"
        con = sqlite3.connect(r"./dronedb.db")
        cur = con.cursor()
        cur.execute(query)

        counter = 0
        for sub in cur.fetchall():
            sub_lat = float(sub[1])
            sub_lng = float(sub[2])
            lat = float(lat)
            lng = float(lng)
            if (abs(sub_lat - lat) <= 1.0) and (abs(sub_lng - lng) <= 1.0):
                sub_dict = dict()
                sub_dict['lat']   = sub_lat
                sub_dict['lng']   = sub_lng
                sub_dict['rad']   = sub[3]
                sub_dict['des']   = sub[4]
                sub_dict['city']  = sub[5]
                sub_dict['ctry']  = sub[6]

                self._sub_dict[counter] = sub_dict
                counter += 1
        con.close()
        return list(self._sub_dict.values())