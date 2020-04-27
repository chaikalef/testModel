from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request

from ml import Clf
from validate import e_400, e_500, validate

app = Flask(__name__)
swagger = Swagger(app)
clf = Clf()

app.register_error_handler(400, e_400)
app.register_error_handler(500, e_500)


@app.route('/predict', methods=['POST'])
@swag_from('swag.yaml')
@validate
def predict():
    req = request.get_json()
    res = []

    for model_id in req['models']:
        res.append(clf.run(
            model_id=model_id,
            data=req['data']
        ))

    return jsonify(res), 200
