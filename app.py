from flask import Flask, jsonify, request

from ml import Clf
from validate import validate

app = Flask(__name__)
clf = Clf()


@app.route('/predict', methods=['POST'])
@validate
def pred():
    return jsonify({'salary': clf.run(data=request.get_json())}), 200


@app.errorhandler(500)
def e_500(error):
    return jsonify({'error': str(error)}), 500


@app.errorhandler(400)
def e_400(error):
    return jsonify({'error_valid': str(error)}), 400
