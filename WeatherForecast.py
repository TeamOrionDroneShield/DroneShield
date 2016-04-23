import json

import requests


def forecast_retrieval(latitude,longitude):
    r = requests.get('https://api.forecast.io/forecast/d968c76b162ac59de4c57cdbdcfbe83b/' + latitude + ',' + longitude)
    return r.text
