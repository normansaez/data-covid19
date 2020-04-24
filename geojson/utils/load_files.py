#! /usr/bin/python3
# -- coding: utf-8 --
import glob
from pathlib import Path
import os
import json
import pymongo
import gridfs

if __name__ == '__main__':
#    client = pymongo.MongoClient()
    client = pymongo.MongoClient("mongodb://192.168.2.223:27017")
    db = client["regiones"]
    fs = gridfs.GridFS(client.comunas)

    files = []
    path = Path('.').rglob('*.topo')
    #    path.rename(path.name.replace(' ','_'))
    for i in path:
       files.append(i.name)
    print("total files: {}".format(len(files))  ) 
    files.sort(key=lambda f: os.stat(f).st_size, reverse=True)
    for name in files:
        print(name)
        with open(name, 'r') as jsonfile:
            json_data = json.load(jsonfile)
        #print(json_data)
        
        col = db[name.rstrip('.topo')]
        try:
            x = col.insert_one(json_data)
        #    print(x)
        except pymongo.errors.DocumentTooLarge:
            print("{}\n could not be inserted".format(name))
            with open(name, 'rb') as jsonfile:
                a = fs.put(jsonfile)
            dict_name_pointer = {name:a}
            print(dict_name_pointer)
#    x = col.find_one()
#    print(db.getCollectionNames())
        #    x = col.find_one()
