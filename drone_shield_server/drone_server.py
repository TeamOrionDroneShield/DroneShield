import json

from NoFly import NoFlyClient
from Submission import Submit
from WeatherForecast import forecast_retrieval
from flask import Flask, request
from login import login_control

from drone_shield_server.posts_retrieval import posts_retrieving

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

@app.route('/submit', methods=['POST', 'GET'])
def submission():
    uid = request.args.get('uid')
    type = request.args.get('type')
    lat  = request.args.get('lat')
    lng  = request.args.get('lng')
    rad  = request.args.get('rad')
    des  = request.args.get('des')
    lvl  = request.args.get('lvl')
    sub = Submit(uid, type)
    if not sub.authorized():
        return "NOT AUTHORIZED"

    sub.setPosition(lat, lng, rad)
    sub.setDescription(lvl, des)
    sub.settingDB()

    return "AUTHORIZED"

@app.route('/getobstacles', methods=['POST', 'GET'])
def getSubmission():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    SUB = Submit()

    sub_data = dict()
    sub_data['data'] = SUB.searchingDB(lat, lng)
    return str(json.dumps(sub_data))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555)
