from flask import Flask, request
import json

from WeatherForecast import forecast_retrieval
from login import login_control
from NoFly import NoFlyClient
from posts_retrieval import posts_retrieving

app = Flask(__name__)


@app.route('/forecast', methods=['GET','POST'])
def entry_point():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    return forecast_retrieval(latitude, longitude)

@app.route('/login')
def login():
    username = 'ugo'# request.args.get("username")
    password = 'mario' #request.args.get("password")
    return login_control(username,password)

@app.route('/')
def post_retrieve():
    return posts_retrieving()

@app.route('/nfz', methods=['POST', 'GET'])
def returnNFZ():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    NFC = NoFlyClient("https://flysafe-api.dji.com/api/release_limitarea.json")

    nfz_data = dict()
    nfz_final_list = []
    nfz_data["data"] = nfz_final_list

    nfz_list = NFC.searchingDB(lat, lng)
    for nfz in nfz_list:
        nfz_d = dict()
        nfz_d["name"]    = nfz._name
        nfz_d["city"]    = nfz._city
        nfz_d["lat"]     = nfz._latitude
        nfz_d["lng"]     = nfz._longitude
        nfz_d["radius"]  = nfz._radius
        nfz_d["level"]   = nfz._level
        nfz_final_list.append(nfz_d)

    return str(json.dumps(nfz_data))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555)
