import pandas as pd
import json
import requests
import yaml

def read_enpoints(filename="endpoints.yaml"):
    with open(filename) as file:
        endpoints = yaml.load(file, Loader=yaml.FullLoader)
    return endpoints['endpoints']

if __name__ == '__main__':
    endpoints = read_enpoints()
    notjason = 0
    err = 0
    l_notjson= []
    l_err = []
    for endpoint in endpoints:
        print(endpoint)
        r = requests.get(endpoint) 
        try:
            df = pd.DataFrame.from_dict(r.json())
            print(df)
        except json.decoder.JSONDecodeError:
            l_notjson.append(endpoint)
            notjason += 1
        except:
            l_err.append(endpoint)
            err += 1
#####################################################################
total = len(endpoint)
jres =  len(endpoint) - notjason - err
print("Stats\n")
for i in l_notjson:
    print("not json: {}".format(i))
for i in l_err:
    print("error: {}".format(i))
print("\nTotal endpoints: {} , json response {} , not json {}, error {}".format(total, jres, notjason, err))

