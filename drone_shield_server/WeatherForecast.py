import json

import requests


def forecast_retrieval(latitude,longitude):
    r = requests.get('https://api.forecast.io/forecast/d968c76b162ac59de4c57cdbdcfbe83b/' + latitude + ',' + longitude)
    json_result = json.loads(r.text)
    json_final = dict()
    data = []
    json_final['currently'] = data
    data.append(json_result['currently'])
    return str(json.dumps(json_final))

