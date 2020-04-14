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

#app.config["MONGO_URI"] = "mongodb://192.168.2.223:27017/regiones"
app.config["MONGO_URI"] = "mongodb://localhost:27017/comunas"
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

@app.route('/v1/get_regiones', methods=['GET'])
def get_regiones():
    '''
    get_regiones
    '''
    app.logger.info("get_regiones")
    db = client['regiones']
    regiones = db.list_collection_names()
    response = {'regiones':regiones} 
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
        doc = collec.find_one()
        if doc == None:
            return jsonify({"status":"not found"}), 200
        doc.pop("_id",None)
        response = doc
        return jsonify(response), 200
    except pymongo.errors.InvalidName:
        return jsonify({"status":"empty field"}), 200

@app.route('/v1/get_comuna_by_region_id', methods=['GET'])
def get_comuna_by_region_id():
    '''
    - Te paso el código de región y el parámetro de simplificación
    - Me retornas el topojson de las comunas a la  región correspondiente
    
    '''
    try:
        region_cut = request.args.get('region')
        simplify = request.args.get('simplify')
        app.logger.info("Comuna ID: {}".format(region_cut))
        app.logger.info("simplify: {}".format(simplify))
        db = client['comunas']
        collec = db[region_cut]
        doc = collec.find_one()
        if doc == None:
            return jsonify({"status":"not found"}), 200
        doc.pop("_id",None)
        # https://gist.github.com/arthur-e/8495616
        ts = datetime.datetime.now().timestamp()
        geo = "{}.{}".format(ts,'json')
        topo = "topo_{}.{}".format(ts,'json')

        with open(geo, 'w') as outfile:
            json.dump(doc, outfile)

        cmd = "toposimplify {} -p {} -o {}".format(geo, simplify, topo)
        app.logger.info(cmd)
        process = Popen(cmd , stdout=subprocess.DEVNULL , stderr=subprocess.DEVNULL , shell=True)
        process.wait()
        with open(topo) as json_file:
            data = json.load(json_file)
        response = data
        return jsonify(response), 200
    except pymongo.errors.InvalidName:
        return jsonify({"status":"empty field"}), 200

@app.route('/v1/get_region_by_id', methods=['GET'])
def get_region_by_id():
    '''
    get_region_by_id: 
    - Te paso el código de región y el parámetro de simplificación
    - Me retornas el topojson de la región correspondiente
    '''
    try:
        region_id = request.args.get('region')
        simplify = request.args.get('simplify')
        app.logger.info("Region ID: {}".format(region_id))
        app.logger.info("simplify: {}".format(simplify))
        db = client['regiones']
        collec = db[region_id]
        doc = collec.find_one()
        if doc == None:
            return jsonify({"status":"not found"}), 200
        doc.pop("_id",None)
        app.logger.info(doc)
        #Topo
        #using 
        # https://gist.github.com/arthur-e/8495616
        ts = datetime.datetime.now().timestamp()
        geo = "{}.{}".format(ts,'json')
        topo = "topo_{}.{}".format(ts,'json')

        with open(geo, 'w') as outfile:
            json.dump(doc, outfile)

        cmd = "toposimplify {} -p {} -o {}".format(geo, simplify, topo)
        process = Popen(cmd , stdout=subprocess.DEVNULL , stderr=subprocess.DEVNULL , shell=True)
        process.wait()
        with open(topo) as json_file:
            data = json.load(json_file)
        response = data
        return jsonify(response), 200
    except pymongo.errors.InvalidName:
        return jsonify({"status":"empty field"}), 200


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
