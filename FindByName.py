from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb+srv://corentin_database:<password>@cluster0.ypoozbz.mongodb.net/?retryWrites=true&w=majority")
db = client.test
stations = db.stations

def search(station):

    uppercase_station=station.upper() 
    
    list_stations = stations.find({"name": {"$regex":uppercase_station}})
  
    for elm in list_stations :
      print(elm)

search("Va")