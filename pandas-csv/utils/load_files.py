#! /usr/bin/python3
# -- coding: utf-8 --
import glob
from pathlib import Path
import os
import json
import pymongo
import datetime


if __name__ == '__main__':
#    client = pymongo.MongoClient()
    client = pymongo.MongoClient("mongodb://192.168.2.223:27017")
    db = client["movilidad"]
    path = Path('.').rglob('*.csv')
    for filename in path:
        print(filename.name)
        names = filename.name.rstrip('.csv').split("_")
        year = names[1]
        monthinteger= int(names[2])
        month = datetime.date(1900, monthinteger, 1).strftime('%b').upper()
        read_file = pd.read_csv(filename.name)
        json_data = json.loads(read_file.to_json(orient="index"))
        col = db["{}-{}".format(year,month)]
        print(month)
        print(year)
        try:
            x = col.insert_one(json_data)
        except pymongo.errors.DocumentTooLarge:
            print("{}\n could not be inserted".format(name))
