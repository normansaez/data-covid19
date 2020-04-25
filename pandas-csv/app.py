import logging
import json
import pandas as pd

from flask import Flask
from flask import jsonify
from flask import request
import datetime
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

@app.route('/v1/get_movilidad', methods=['GET'])
def get_movilidad():
    '''
    get_movilidad
    '''
    app.logger.info("get_movilidad")

    monthinteger = int(request.args.get('month'))
    year = request.args.get('year')
    month = datetime.date(1900, monthinteger, 1).strftime('%b').upper()

    app.logger.info("month: {}".format(month))
    app.logger.info("year: {}".format(year))

    movi = "{}-{}".format(year,month)
    db = client['movilidad']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v2/get_movilidad', methods=['GET'])
@app.route('/v2/get_movilidad_by_cut', methods=['GET'])
def get_movilidad_by_cut():
    '''
    get_movilidad
    '''
    app.logger.info("v2: get_movilidad")
    monthinteger = int(request.args.get('month'))
    year = request.args.get('year')
    month = datetime.date(1900, monthinteger, 1).strftime('%b').upper()

    app.logger.info("month: {}".format(month))
    app.logger.info("year: {}".format(year))

    movi = "{}-{}".format(year,month)

    db = client['movilidad_by_cut']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True, ssl_context=('cert.pem', 'key.pem'))
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
