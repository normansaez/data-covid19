import logging
import time
import json
import pymongo 


from flask import Flask
from flask import jsonify
from flask import request

from flask_pymongo import PyMongo

app = Flask(__name__)

#app.config["MONGO_URI"] = "mongodb://192.168.2.223:27017/comunas"
app.config["MONGO_URI"] = "mongodb://localhost:27017/comunas"
mongo = PyMongo(app)


def dump_func_name(func):
    def echo_func(*func_args, **func_kwargs):
        app.logger.info('EXEC: {}'.format(func.__name__))
        return func(*func_args, **func_kwargs)
    return echo_func

#@dump_func_name
@app.route('/health_check', methods=['GET'])
def empty_view():
    app.logger.info("health_check")
    response = {'status': 'OK'}
    return jsonify(response), 200

#@dump_func_name
@app.route('/get_comunas', methods=['GET'])
def get_comunas():
    app.logger.info("get_comunas")
    comunas = mongo.db.list_collection_names()
    response = {'comunas':comunas} 
    return jsonify(response), 200

#@dump_func_name
@app.route('/get_comuna_by_name', methods=['GET'])
def get_comuna_by_name():
    app.logger.info("get_comuna_by_name")
    comuna = request.args.get('comuna')
    app.logger.info("Comuna: {}".format(comuna))

    db = mongo.db.comunas
    app.logger.info(type(db))
    col = db[comuna]
    app.logger.info(type(col))

    x = col.find()
    app.logger.info(x)

    response = {'status': 'OK'}
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
