from json import dumps, load
from traceback import format_exc

from flask import abort, request
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


schema = DataSchema()


def validate(fn):
    def _():
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

    return _
