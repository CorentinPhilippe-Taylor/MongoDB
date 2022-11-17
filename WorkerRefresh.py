from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
import json
import dateutil.parser
import time

client = MongoClient("mongodb+srv://corentin_database:<password>@cluster0.ypoozbz.mongodb.net/?retryWrites=true&w=majority")
db = client.test

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


vlilles = get_vlille()

while True:
    print('update')
    vlilles = get_vlille()
    datas = [
        {
            "name": elem.get('fields', {}).get('nom'),
            "bike_availbale": elem.get('fields', {}).get('nbvelosdispo'),
            "stand_availbale": elem.get('fields', {}).get('nbplacesdispo'),
            "date": dateutil.parser.parse(elem.get('fields', {}).get('datemiseajour')),
            "station_id": elem.get('fields', {}).get('libelle'),
            "status": elem.get('fields', {}).get('etat') == "EN SERVICE"
        }
        for elem in vlilles
    ]
    
    for data in datas:
        db.datas.update_one({"station_id": data["station_id"]}, { "$set": data }, upsert=True)

    time.sleep(10)