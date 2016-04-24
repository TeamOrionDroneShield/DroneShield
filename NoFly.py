import sqlite3
import datetime
import requests
import json

class NoFlyZoneDB:
    def __init__(self):
        '''
        initializing the NoFlyZoneDB class with the parameters
        setted to None by default
        '''
        self._shape     = None
        self._latitude  = None
        self._longitude = None
        self._radius    = None
        self._beginat   = None
        self._endat     = None
        self._name      = None
        self._city      = None
        self._level     = None

class NoFlyZone:
    def __init__(self):
        '''
        initializing the NoFlyZone class with the parameters
        setted to None by default
        '''
        self._latitude  = None
        self._longitude = None
        self._radius    = None
        self._name      = None
        self._city      = None
        self._level     = None


class NoFlyClient:
    def __init__(self, source_url):
        """
        initializing the client to retrieve the no fly zones
        informations
        :return: None
        """
        self._source_url = source_url
        self._nfc_dict   = dict()

    def retrievingJSON(self):
        """
        retrieving the json from the source url for the fly zones
        complete informations list
        :return: the dictionary for all the no fly zone
        """
        # retrieving the JSON
        req = requests.get(self._source_url)
        json_raw = req.text
        json_nfz = json.loads(json_raw)
        # constructing the dictionary
        nfz_root = json_nfz["release_limits"]
        total_entries = 0
        for i in range (0, len(nfz_root)):
            new_nfz = NoFlyZoneDB()
            new_nfz._shape      = nfz_root[i]["shape"]
            new_nfz._latitude   = nfz_root[i]["lat"]
            new_nfz._longitude  = nfz_root[i]["lng"]
            new_nfz._radius     = nfz_root[i]["radius"]
            new_nfz._beginat    = datetime.datetime.fromtimestamp(int(nfz_root[i]["begin_at"])).strftime('%d-%m-%Y %H:%M:%S')
            new_nfz._endat      = datetime.datetime.fromtimestamp(int(nfz_root[i]["end_at"])).strftime('%d-%m-%Y %H:%M:%S')
            new_nfz._name       = nfz_root[i]["name"]
            new_nfz._city       = nfz_root[i]["city"]
            new_nfz._level      = nfz_root[i]["level"]

            total_entries += 1
            self._nfc_dict[i] = new_nfz

        return self._nfc_dict


    def settingDB(self):
        """
        inserting the no fly zones entries into the local database
        :return: boolean if it successfull or not
        """
        query = "INSERT INTO NFZONE(ID, SHAPE, LAT, LNG, RADIUS, BEGIN_AT, END_AT, NAME, CITY, LEVEL) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        con = sqlite3.connect(r"./dronedb.db")
        cur = con.cursor()
        # preparing list of tuples to execute the script
        nfz_list = []
        for key in self._nfc_dict.keys():
            nfz = self._nfc_dict[key]
            nfz_list.append((key, nfz._shape, nfz._latitude, nfz._longitude, nfz._radius, nfz._beginat, nfz._endat, nfz._name, nfz._city, nfz._level))
        # executing and committing the query iterating over the tuples
        cur.executemany(query, nfz_list)
        con.commit()
        return True


    def searchingDB(self, lat, lng):
        """
        retrieving the no fly zones from the db
        :return: the dictionary of all the no fly zones
        """
        self._nfc_dict = dict()
        query = "SELECT * FROM NFZONE"
        con = sqlite3.connect(r"./dronedb.db")
        cur = con.cursor()
        cur.execute(query)

        counter = 0
        for nfz in cur.fetchall():
            nfz_lat = float(nfz[2])
            nfz_lng = float(nfz[3])
            lat     = float(lat)
            lng     = float(lng)
            if (abs(nfz_lat - lat) <= 0.5) and (abs(nfz_lng - lng) <= 0.5):
                new_nfz = NoFlyZone()
                new_nfz._latitude  = nfz_lat
                new_nfz._longitude = nfz_lng
                new_nfz._radius    = nfz[4]
                new_nfz._name      = nfz[7]
                if new_nfz._name == "NULL":
                    new_nfz._name = "Not available"
                new_nfz._city      = nfz[8]
                if new_nfz._city == "NULL":
                    new_nfz._city = "Not available"
                new_nfz._level     = nfz[9]

                self._nfc_dict[counter] = new_nfz
                counter += 1
        con.close()
        return list(self._nfc_dict.values())

    def returnNFZ(self):
        """
        return all the no fly zones in JSON format
        :return: dictionary of all the no fly zones
        """



if __name__ == "__main__":
    NFC = NoFlyClient("https://flysafe-api.dji.com/api/release_limitarea.json")
    NFC.searchingDB(41.8925682,12.4896667)
