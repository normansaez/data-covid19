import logging
import time
import json
import pymongo 

from flask import Flask
from flask import jsonify
from flask import request

#import comunas_mongo

app = Flask(__name__)

@app.route('/health_check', methods=['GET'])
def empty_view():
    app.logger.info('health check')
    response = {'status': 'OK'}
    return jsonify(response), 200

@app.route('/get_comunas', methods=['GET'])
def get_comunas():
#    comunas = comunas_mongo.get_comunas()
    client = pymongo.MongoClient('mongodb://192.168.2.223:27017/')
    db = client["comunas"]
    comunas = db.list_collection_names()
#    print(comunas)
#    print(type(comunas))
#    c = json.dumps(comunas)
    response = {'comunas':comunas} 
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
