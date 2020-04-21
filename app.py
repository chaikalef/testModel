from flask import Flask, jsonify, request
from joblib import load

from ml.clf import Clf

app = Flask(__name__)
clf = Clf()


@app.route('/predict', methods=['POST'])
def pred():
    if request.is_json:
        return jsonify({'salary': clf.run(data=request.get_json())})
