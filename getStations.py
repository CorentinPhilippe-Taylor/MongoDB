from pymongo.mongo_client import MongoClient
import requests
import json

client = MongoClient("mongodb+srv://corentin_database:<password>@cluster0.ypoozbz.mongodb.net/?retryWrites=true&w=majority")
db = client.test

def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

vlilles = get_vlille()
vlillesToInsert = []
for vlib in vlilles:
    vlillesToInsert.append({
        "name": vlib["fields"]["nom"],
        "city": vlib["fields"]["commune"],
        "size": vlib["fields"]["nbvelosdispo"] + vlib["fields"]["nbplacesdispo"],
        "geo": vlib["geometry"],
        "TPE ": vlib["fields"]["type"] != "SANS TPE",
        "status": vlib["fields"]["etat"] == "EN SERVICE",
        "last update": vlib["record_timestamp"] })

try: 
    db.stations.insert_many(vlillesToInsert, ordered=False)
except:
    print("fail to connect")
    pass