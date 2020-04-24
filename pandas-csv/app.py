import logging
import json
import pandas as pd

from flask import Flask
from flask import jsonify
from flask import request
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://192.168.2.223:27017")


@app.route('/health_check', methods=['GET'])
def health_check():
    '''
    health_check
    '''
    app.logger.info("health_check")
    response = {'status': 'OK'}
    return jsonify(response), 200

@app.route('/v1/ingest_raw', methods=['GET'])
def get_comunas():
    '''
    get_comunas
    '''
#    app.logger.info("get_comunas")
#    db = client['comunas']
#    comunas = db.list_collection_names()
#    response = {'comunas':comunas} 
    read_file = pd.read_excel (r'movilidad_ene2019.csv')
    mycsv = read_file.to_csv (r'name.csv', index = None, header=True)
    response = {'status': mycsv}

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
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
