import logging
import time
import json
import pymongo 

from flask import Flask
from flask import jsonify
from flask import request

#import comunas_mongo

app = Flask(__name__)
client = pymongo.MongoClient('mongodb://192.168.2.223:27017/')

def dump_func_name(func):
    def echo_func(*func_args, **func_kwargs):
        app.logger.info('EXEC: {}'.format(func.__name__))
        return func(*func_args, **func_kwargs)
    return echo_func

#@dump_func_name
@app.route('/health_check', methods=['GET'])
def empty_view():
    response = {'status': 'OK'}
    return jsonify(response), 200

#@dump_func_name
@app.route('/get_comunas', methods=['GET'])
def get_comunas():
    db = client["comunas"]
    comunas = db.list_collection_names()
    response = {'comunas':comunas} 
    return jsonify(response), 200

#@dump_func_name
@app.route('/get_comuna_by_name', methods=['GET'])
def get_comuna_by_name():
    comuna = request.args.get('comuna')
    app.logger.info("Comuna: {}".format(comuna))
    db = client["comunas"]
    col = db[comuna] 
    x = col.find_one()
    app.logger.info(x)
    print(type(x))
    response = {'comuna': x}
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
