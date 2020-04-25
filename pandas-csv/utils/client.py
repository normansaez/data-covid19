#!/bin/python3
import json
import requests
import pandas as pd

def get_similar_region(region_cut, word):
    word = word.upper()
    print(word)
    for region,cut in region_cut.items():
#        print("{}->{}".format(region,cut))
        if region.__contains__(word) is True:
            print("{} similar: {}->{}".format(word, region,cut))
#            return cut
if __name__ == '__main__':
    endpoint = "http://192.168.2.223:5004/v1/get_movilidad?month=1&year=2019"
    cut_endpoint = "http://192.168.2.220:8080/covid19/findComunaByIdState?idState="

    cuts = requests.get(cut_endpoint)
    cut_d = cuts.json()
    region_cut = {}
    for key in cut_d:
#        print("{}=>{}".format(key['description'],key['cut']))
#        print("-"*100)
        region_cut[key['description'].upper()] = key['cut']
#        region_cut.append({key['description']: key[cut]})
#    print(region_cut)
    #
    #
    #
    r = requests.get(endpoint) 
    movilidad = r.json()

    new_vector = {}
    for indice in movilidad:
        vector = movilidad[indice]
#        print(vector)
        try:    
##999 -> {'COM_Destino': 'Lo Prado', 'COM_Origen': 'La Florida', 'Conteo - COM_Destino': 2, 'Conteo - COM_Origen': 2}
#            print(vector)
            region_cut[vector['COM_Destino'].upper()]
            region_cut[vector['COM_Origen'].upper()]

            new_vector['COM_Destino'] = region_cut[vector['COM_Destino'].upper()] 
            new_vector['COM_Origen'] = region_cut[vector['COM_Origen'].upper()]
            new_vector['Conteo - COM_Destino'] = vector['Conteo - COM_Destino'] 
            new_vector['Conteo - COM_Origen'] = vector['Conteo - COM_Origen'] 
            print("{},{},{},{}".format(new_vector['COM_Destino'],new_vector['COM_Origen'],new_vector['Conteo - COM_Destino'],new_vector['Conteo - COM_Origen']))
        except AttributeError:
            print("COM_Destino {}".format(vector))
        except KeyError:
            print("COM_Destino {}".format(vector))
            get_similar_region(region_cut, vector['COM_Destino'])
