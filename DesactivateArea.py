from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb+srv://corentin_database:<password>@cluster0.ypoozbz.mongodb.net/?retryWrites=true&w=majority")
db = client.test
datas = db.datas
stations = db.stations 


userLongitude = float(input("What is your longitude ?"))
userLatitude = float(input("What is your latitude ?"))
radiusDistance = float(input("Enter the distance in meters."))
db.stations.create_index([("geo","2dsphere")])

near_stations= stations.find({"geo":  {"$near": 
                                    {"$geometry":
                                     {"type": "Point", "coordinates": [float(userLatitude), float(userLongitude)]},
                                         "$maxDistance" : 1000}}})


for elm in near_stations: 
  print(elm["name"])
  stations.update_one({"_id":elm["_id"]}, {"$set": {"status": False}},
                                  upsert = True)