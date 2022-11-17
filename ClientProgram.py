from pymongo import MongoClient


client = MongoClient("mongodb+srv://corentin_database:<password>@cluster0.ypoozbz.mongodb.net/?retryWrites=true&w=majority")
db = client.test
datas = db.datas
stations = db.stations 


userLongitude = float(input("What is your longitude ?"))
userLatitude = float(input("What is your latitude ?"))
db.stations.create_index([("geo","2dsphere")])

near_stations= stations.find({"geo":  {"$near": 
                                    {"$geometry":
                                     {"type": "Point", "coordinates": [float(userLatitude), float(userLongitude)]}}}})[0]


print(near_stations["name"])