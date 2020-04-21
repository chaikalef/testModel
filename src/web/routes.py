# -*- coding: utf-8 -*-
from flask import jsonify, render_template, request

from ..ml.pred import predict
from . import appInstance, enc_text


@appInstance.route('/', methods=['GET'])
@appInstance.route('/index', methods=['GET'])
def site():
    user = {'username': 'Cool pythonist'}
    preds = [
        {
            'name': 'Сергей Андреевич',
            'salary': 42
        },
        {
            'name': 'Василий ака питон',
            'salary': 24
        }
    ]
    return render_template(
        'index.html',
        title='Flask app',
        user=user,
        preds=preds
        )

@appInstance.route('/', methods=['POST'])
@appInstance.route('/index', methods=['POST'])
def pred():
    if request.is_json:
        data = request.get_json()
        pred = {
            'salary': predict(data=data,
            enc=enc_text
            )
        }
        return jsonify(pred)

if __name__ == "__main__":
    appInstance.run(host='127.0.0.1', port=5017)
