# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:22:12 2023

@author: Tony
"""

from pymongo import MongoClient
import certifi
import json
 

user = "t-btay"
passw = "jgAXBgHB6RNcGCP5"
ca = certifi.where()
connection_string = f"mongodb+srv://{user}:{passw}@cluster0?ssl=true&ssl_cert_reqs=CERT_NONE.mfbl8ws.mongodb.net/?retryWrites=true&w=majority"

data_str = ""
file_index = 0



###############################################################################

#functions

def ping_db_server(db):
    print("pinging...")
    db.admin.command("ping")
    print("Connection successful")
    
def get_json(file_name):
    with open(file_name, "r") as file:
        return file

###############################################################################


cluster = MongoClient(connection_string, tlsCAFile = ca)
ping_db_server(cluster)
database = cluster["TestDB"]
collection = database["TestColl"]

with open("savefile2.json", "r") as file:
    for data_read in file:
        data_str += data_read
    data = json.loads(data_str)
    #collection.delete_many({}) #CAUTION: DELETES ENTIRE DB
    collection.insert_one(data)


post_count = collection.count_documents({})
print(f"posts: {post_count} \n")

results = collection.find({})
for i in results:
    print(i)

print("finished")

cluster.close()
