#!/bin/bash
curl http://192.168.2.223:5000/health_check
curl http://192.168.2.223:5000/v1/get_comunas
#curl http://192.168.2.223:5000/v1/get_comuna_by_name?comuna=13130_SAN_MIGUEL
curl http://192.168.2.223:5000/v1/get_comuna_by_name?comuna=13130
curl http://192.168.2.223:5000/v1/get_comuna_by_cut?comuna=13130&simpl_number=50
curl http://192.168.2.223:5000/v1/get_region_by_id
curl http://192.168.2.223:5000/v1/get_comunas_by_region_id
