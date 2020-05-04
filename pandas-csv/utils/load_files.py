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
    extension = 'xlsx' 
    nombre_bd = 'SOCHIMIUPS'
#    collection = "activos_comunas_dia_marzo"
    db = client[nombre_bd]
    path = Path('.').rglob('*.{}'.format(extension))
    for filename in path:
#        print(filename.name)
        collection = filename.name.rsplit('.{}'.format(extension))[0]
        print(collection)
#        read_file = pd.read_csv(filename.name, encoding= 'unicode_escape')
        read_file = pd.read_excel(filename.name, encoding= 'unicode_escape')
        json_data = json.loads(read_file.to_json(orient="index"))

        col = db[collection]
        try:
            x = col.insert_one(json_data)
        except Exception as ex:
            print("{}\n could not be inserted: {}".format(collection,str(ex)))
            
