from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb+srv://corentin_database:<password>@cluster0.ypoozbz.mongodb.net/?retryWrites=true&w=majority")
db = client.test
stations = db.stations
datas = db.datas

def delete_station_datas (name):

    uppercase_name=name.upper() 

    stations.delete_one( {"name":uppercase_name} )

    datas.delete_many( {"name":uppercase_name} )

delete_station_datas("BUISSON")