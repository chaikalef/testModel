from json import load
from traceback import format_exc

from flask import abort, jsonify, request
from marshmallow import Schema, ValidationError, fields
from marshmallow import validate as val


class DataSchema(Schema):
    valid_sets = None
    with open('valid_sets.json', 'r') as fp:
        valid_sets = load(fp)

    description = fields.Str(
        required=True,
        validate=val.Length(max=1000)
    )
    location = fields.Str(
        required=True,
        validate=val.OneOf(valid_sets['location'])
    )
    contract = fields.Str(
        required=True,
        validate=val.OneOf(valid_sets['contract'])
    )


class APISchema(Schema):
    models = fields.List(
        cls_or_instance=fields.Str,
        required=True,
        validate=val.Length(min=2)
    )
    data = fields.Nested(DataSchema)


schema = APISchema()


def validate(fn):
    def _wrap():
        try:
            if request.is_json:
                schema.load(request.get_json())
                return fn()
            else:
                raise ValueError('request is not json')

        except ValidationError as err:
            abort(400, err.messages)
        except ValueError as err:
            abort(400, err)
        except:
            abort(500, format_exc())

    return _wrap


def e_500(error):
    return jsonify({'error': str(error)}), 500


def e_400(error):
    return jsonify({'error_valid': str(error)}), 400
