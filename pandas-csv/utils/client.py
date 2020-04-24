#!/bin/python3
import json
import requests

if __name__ == '__main__':
    endpoint = "http://192.168.2.223:5004/v1/get_movilidad?month=1&year=2019"
    r = requests.get(endpoint) #, params = {"w":"774508"})   
    mydict = r.json()
    print(mydict)
    for key in mydict:
        print(key, '->', mydict[key])
