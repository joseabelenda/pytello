#!python3
from flask import Flask, jsonify, request
import logging
import sys
from drone_manager import DroneManager

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

app = Flask(__name__)

livros = [
    {
        'id': 1,
        'titulo': 'O Auto da Compadecida',
        'autor': 'Ariano Suassuna'
    }
]

drone_manager = None

try:
    drone_manager = DroneManager()
except Exception as exception:
    logger.error(exception)


@app.route('/takeoff', methods=['POST'])
def takeoff():
    print('takeoff')
    if drone_manager:
        try:
            drone_manager.takeoff()
            return jsonify('OK')

        except Exception as exception:
            logger.error(exception)
            return jsonify('ERROR')
    else:
        logger.error('Drone not connected')
        return jsonify('ERROR - Drone not connected')


@app.route('/land', methods=['POST'])
def land():
    print('land')
    if drone_manager:
        try:
            drone_manager.land()
            return jsonify('OK')

        except Exception as exception:
            logger.error(exception)
            return jsonify('ERROR')
    else:
        logger.error('Drone not connected')
        return jsonify('ERROR - Drone not connected')


@app.route('/livros', methods=['GET'])
def get_livros():
    print('get_livros')
    return jsonify(livros)


def run():
    app.run(port=5001, host='localhost', debug=True)
