# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:22:12 2023

@author: Tony
"""

from pymongo import MongoClient
import certifi
 

user = "t-btay"
passw = "jgAXBgHB6RNcGCP5"
ca = certifi.where()
connection_string = f"mongodb+srv://{user}:{passw}@cluster0?ssl=true&ssl_cert_reqs=CERT_NONE.mfbl8ws.mongodb.net/?retryWrites=true&w=majority"


###############################################################################

#functions

def ping_db_server(db):
    print("pinging...")
    db.admin.command("ping")
    print("Connection successful")

###############################################################################


cluster = MongoClient(connection_string, tlsCAFile = ca)
ping_db_server(cluster)
database = cluster["TestDB"]
collection = database["TestColl"]

post1 = {"_id":0, "name":"tony", "score": 5}
post2 = {"_id":1, "name":"dan", "score": 4}#lol

#collection.update_one({"name":"jim"},{"$inc":{"hats":1}})

post_count = collection.count_documents({})
print(f"posts: {post_count} \n")

results = collection.find({})
for i in results:
    print(i)
print("finished")

cluster.close()
