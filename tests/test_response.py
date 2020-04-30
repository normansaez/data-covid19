import pytest
import yaml
import requests

def test_check_status_code_equals_200():
    with open(r'endpoints.yaml') as file:
        endpoints = yaml.load(file, Loader=yaml.FullLoader)
    for endp in endpoints['endpoints']:
        response = requests.get(endp)
        print(endp)
        assert response.status_code == 200
