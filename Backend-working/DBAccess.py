# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:22:12 2023

@author: Tony
"""

from pymongo import MongoClient

user = "t-btay"
passw = "jgAXBgHB6RNcGCP5"
connection_string = f"mongodb+srv://{user}:{passw}@cluster0.mfbl8ws.mongodb.net/?retryWrites=true&w=majority"



cluster = MongoClient(connection_string)
database = cluster["TestDB"]
collection = database["TestColl"]

post = {"_id":0, "name":"DBTestName", "score": 5}

collection.insert_one(post)

cluster.close()