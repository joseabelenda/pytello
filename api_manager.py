#!python3
from flask import Flask, jsonify, request
import logging
import sys

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


@app.route('/livros', methods=['GET'])
def get_livros():
    print('get_livros')
    return jsonify(livros)


@app.route('/drone/patrol', methods=['POST'])
def patrol():
    print('patrol')
    json = request.get_json()
    print(json)
    return jsonify(json)


def run():
    app.run(port=5001, host='localhost', debug=True)
