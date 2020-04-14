#!/bin/bash
curl http://192.168.2.223:5000/health_check
curl http://192.168.2.223:5000/v1/get_comunas
curl http://192.168.2.223:5000/v1/get_regiones
curl http://192.168.2.223:5000/v1/get_comuna_by_region_id?region=5&simplify=0.11
curl http://192.168.2.223:5000/v1/get_region_by_id?region=5&simplify=0.11
