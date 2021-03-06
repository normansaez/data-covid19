import logging
import json
import pandas as pd

from flask import Flask
from flask import jsonify
from flask import request
import datetime
import pymongo
#from werkzeug import secure_filename

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

@app.route('/v2/get_sochimi', methods=['GET'])
def get_sochimi():
    '''
    get_movilidad
    '''
    app.logger.info("v2: get_sochimi")
    monthinteger = int(request.args.get('month'))
    year = request.args.get('year')
    day = request.args.get('day')
    month = datetime.date(1900, monthinteger, 1).strftime('%b').upper()

    app.logger.info("day: {}".format(day))
    app.logger.info("month: {}".format(month))
    app.logger.info("year: {}".format(year))

    movi = "{}_{}_{}_UPC".format(year,month,day)
    #2020_APR_14_UPC

    db = client['SOCHIMIUPS']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v1/get_movilidad_por_comuna', methods=['GET'])
def get_movilidad_por_comuna():
    '''
    get_movilidad
    '''
    app.logger.info("v2: get_movilidad_por_comuna")
#    monthinteger = int(request.args.get('month'))
#    year = request.args.get('year')
#    month = datetime.date(1900, monthinteger, 1).strftime('%b').upper()

#    app.logger.info("month: {}".format(month))
#    app.logger.info("year: {}".format(year))

    movi = "diaria-JAN"#"{}-{}".format(year,month)

    db = client['movilidad_por_comuna']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v1/activos_comunas_por_dia_contagio', methods=['GET'])
def get_activos_comunas_dia_abril():
    '''
    '''
    movi = "activos_comunas_dia_abril"
#    activos_comunas_fecha_abril
    app.logger.info("v1: activos_comunas_por_dia_contagio")
    db = client['activos_comunas']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v1/activos_comunas_por_dia_contagio_marzo', methods=['GET'])
def get_activos_comunas_dia_marzo():
    '''
    '''
    movi = "activos_comunas_dia_marzo"
#    activos_comunas_fecha_abril
    app.logger.info("v1: activos_comunas_por_dia_contagio_marzo")
    db = client['activos_comunas']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v1/activos_comunas_por_fecha_contagio', methods=['GET'])
def get_activos_comunas_fecha_abril():
    '''
    '''
    movi = "activos_comunas_fecha_abril"
#    activos_comunas_fecha_abril
    app.logger.info("v1: activos_comunas_por_fecha_contagio")
    db = client['activos_comunas']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v1/contagios_acumulados_region', methods=['GET'])
def get_contagios_acumulados_region():
    '''
    '''
    movi = "contagios_acumulados_region"
#    activos_comunas_fecha_abril
    app.logger.info("v1: ontagios_acumulados_region")
    db = client['activos_comunas']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v1/contagio_acumulado_comuna', methods=['GET'])
def get_contagio_acumulado_():
    '''
    '''
    movi = "contagio_acumulado_comuna_marzo.csv"
    app.logger.info("v1: contagio_acumulado_comuna")
    db = client['activos_comunas']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200

@app.route('/v1/contagios_valpo', methods=['GET'])
def contagios_valpo():
    '''
    '''
    movi = "contagiosvalpo"
    app.logger.info("v1: contagios_valpo")
    db = client['contagios_valpo']
    collec = db[movi]
    doc = collec.find_one()
    if doc == None:
        return jsonify({"status":"not found"}), 200
    doc.pop("_id",None)
    response = doc
    return jsonify(response), 200
#@app.route('/upload')
#def upload_file():
#   return render_template('templates/upload.html')
#	
#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_file():
#   if request.method == 'POST':
#      f = request.files['file']
#      f.save(secure_filename(f.filename))
#      return 'file uploaded successfully'

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
