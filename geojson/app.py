import logging
import time
import json
import pymongo 
import datetime

from flask import Flask
from flask import jsonify
from flask import request
from subprocess import Popen, PIPE

from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://192.168.2.223:27017/comunas"
#app.config["MONGO_URI"] = "mongodb://localhost:27017/comunas"
mongo = PyMongo(app)
client = pymongo.MongoClient("mongodb://192.168.2.223:27017")


@app.route('/health_check', methods=['GET'])
def health_check():
    '''
    health_check
    '''
    app.logger.info("health_check")
    response = {'status': 'OK'}
    return jsonify(response), 200

@app.route('/v1/get_comunas', methods=['GET'])
def get_comunas():
    '''
    get_comunas
    '''
    app.logger.info("get_comunas")
    comunas = mongo.db.list_collection_names()
    response = {'comunas':comunas} 
    return jsonify(response), 200

@app.route('/v1/get_comuna_by_name', methods=['GET'])
def get_comuna_by_name():
    '''
    get_comuna_by_name
    '''
    app.logger.info("get_comuna_by_name")
    try:
        comuna_id = request.args.get('comuna')
        app.logger.info("Comuna ID: {}".format(comuna_id))
        db = client['comunas']
        collec = db[comuna_id]
    except pymongo.errors.InvalidName:
        return jsonify({"status":"empty field"}), 200
    doc = collec.find_one()
    if doc == None:
        response = {"status":"not found"}
    else:
        doc.pop("_id",None)
        response = doc
    return jsonify(response), 200

@app.route('/v1/get_comuna_by_cut', methods=['GET'])
def get_comuna_by_cut():
    '''
    get_comuna_by_cut:
    - Te paso el código de comuna y el parámetro de simplificación
    - Me retornas el topojson de la comuna correspondiente
    '''
    app.logger.info("get_comuna_by_cut")
    try:
        comuna_id = request.args.get('comuna')
        simpl_number = request.args.get('simpl_number')
        app.logger.info("Comuna ID: {}".format(comuna_id))
        app.logger.info("Simpl number: {}".format(simpl_number))
        db = client['comunas']
        collec = db[comuna_id]
    except pymongo.errors.InvalidName:
        return jsonify({"status":"empty field"}), 200
    doc = collec.find_one()
    if doc == None:
        response = {"status":"not found"}
    else:
        doc.pop("_id",None)
    #Topo
    #using 
    # https://gist.github.com/arthur-e/8495616
    ts = datetime.datetime.now().timestamp()
    geo = "{}.{}".format(ts,'json')
    topo = "topo_{}.{}".format(ts,'json')

    with open(geo, 'w') as outfile:
        json.dump(doc, outfile)

    cmd = "geo2topo {} -q {} -o {}".format(geo, simpl_number, topo)
    process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
    process.wait()
    with open(topo) as json_file:
        data = json.load(json_file)
    response = data
    return jsonify(response), 200

@app.route('/v1/get_region_by_id', methods=['GET'])
def get_region_by_id():
    '''
    get_region_by_id: 
    - Te paso el código de región y el parámetro de simplificación
    - Me retornas el topojson de la región correspondiente
    
    (Este no lo tengo tan definido en estructura ni nombre, pero nos puede ahorrar
    tiempo evitando hacer tantos requests por cada región. Siempre vamos a pedir
    todos los polígonos de las comunas de la región a visualizar)
    '''
    app.logger.info("get_region_by_id")
    comuna_id = request.args.get('comuna')
    app.logger.info("Comuna ID: {}".format(comuna_id))
    return jsonify(response), 200

@app.route('/v1/get_comunas_by_region_id', methods=['GET'])
def get_comunas_by_region_id():
    '''
    get_comunas_by_region_id:
    - Te paso el código de región y el parámetro de simplificación
    - Me retornas el topojson con los polígonos de todas las comunas de la región correspondiente
    
    '''
    app.logger.info("get_comunas_by_region_id")
    comuna_id = request.args.get('comuna')
    app.logger.info("Comuna ID: {}".format(comuna_id))
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    # setup logging using gunicorn logger
    formatter = logging.Formatter(
        '[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s] - %(message)s',
        '%d-%m-%Y %H:%M:%S'
    )
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.handlers[0].setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
