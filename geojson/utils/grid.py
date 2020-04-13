#! /usr/bin/python3
# -- coding: utf-8 --
from pymongo import MongoClient
import gridfs
import json

if __name__ == '__main__':
    name = "12_REGIÓN_DE_MAGALLANES_Y_DE_LA_ANTÁRTICA_CHILENA.json"
    db = MongoClient().comunas
    fs = gridfs.GridFS(db)
    with open(name, 'rb') as jsonfile:
        json_data = json.load(jsonfile)
#        a = fs.put(jsonfile)
    most_recent_three = fs.find().sort("uploadDate", -1).limit(1)
    fs.get(name)
#    a = fs.exists(filename=name)
    print(name)
    ff = fs.find_one(name)
    print(ff)
#    print(fs.get(ff))
