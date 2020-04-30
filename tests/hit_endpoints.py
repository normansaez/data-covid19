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
    print(endpoints)
    for endpoint in endpoints:
        print(endpoint)
        r = requests.get(endpoint) 
        df = pd.DataFrame.from_dict(r.json())
        print(df)
