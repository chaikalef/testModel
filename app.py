from flask import Flask, jsonify, request

from ml import Clf
from validate import e_400, e_500, validate

app = Flask(__name__)
clf = Clf()

app.register_error_handler(400, e_400)
app.register_error_handler(500, e_500)


@app.route('/predict', methods=['POST'])
@validate
def pred():
    return jsonify({'salary': clf.run(data=request.get_json())}), 200
