from traceback import format_exc

from flask import Flask, abort, jsonify, request

from ml import Clf

app = Flask(__name__)
clf = Clf()


@app.route('/predict', methods=['POST'])
def pred():
    try:
        # raise ValueError('Manual error')
        if request.is_json:
            return jsonify({'salary': clf.run(data=request.get_json())})
        else:
            abort(500, 'request is not json')
    except:
        abort(500, format_exc())


@app.errorhandler(500)
def error(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response
