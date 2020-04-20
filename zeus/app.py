import logging
import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/health_check', methods=['GET'])
def health_check():
    '''
    health_check
    '''
    app.logger.info("health_check")
    response = {'status': 'OK'}
    return jsonify(response), 200

@app.route('/zeus_input', methods=['GET'])
def zeus_input():
    '''
    http://192.168.2.223:5002/zeus_input?campo=1
    '''
    campo = request.args.get('campo')
    print(campo) 
    response = {'status': 'OK'}
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
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
