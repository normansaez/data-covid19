#! /usr/bin/python3
# -- coding: utf-8 --
import glob
from pathlib import Path
import os
import json
import pymongo
import datetime
import pandas as pd

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://192.168.2.223:27017")
    nombre_bd = "contagios_valpo"
    collection = ""
    db = client[nombre_bd]
    path = Path('.').rglob('*.csv')
    for filename in path:
#        print(filename.name)
        collection = filename.name.rsplit('_csv')[0]
        print(collection)
        read_file = pd.read_csv(filename.name, encoding= 'unicode_escape')
        json_data = json.loads(read_file.to_json(orient="index"))

        col = db[collection]
        try:
            x = col.insert_one(json_data)
        except pymongo.errors.DocumentTooLarge:
            print("{}\n could not be inserted".format(name))
