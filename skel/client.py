#!/bin/python3
import json
import requests

if __name__ == '__main__':
    endpoint = "http://localhost:5000/v1/get_movilidad"
    r = requests.get(endpoint) #, params = {"w":"774508"})   
    mydict = r.json()
    print(mydict)
    for key in mydict:
        print(key, '->', mydict[key])
