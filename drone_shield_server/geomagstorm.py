import requests, json


def geomagstorm():
    r = requests.get('http://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt')
    rows = r.text.split('\n')
    results = []

    for row in rows:
        riga = row.split(' ')
        if ('Mid/' in riga[0] or 'High/' in riga[0]):
            results.append(riga)

    results = results[:len(results)-6]
    p = []
    for elem in results:
        po = []
        for el in elem:
            if el != '':
              po.append(el)
        p.append(po)

    risultati = dict()
    risultati['data'] = p

    print(str(json.dumps(risultati)))

geomagstorm()