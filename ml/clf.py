from os.path import abspath, dirname, join
from typing import Dict

from joblib import load
from pandas import DataFrame
from scipy.sparse import hstack, random


class Clf():
    _enc = None
    _clf = None

    def __init__(self):
        dir = dirname(abspath(__file__))
        self._enc = {
            '001': {
                'categ': load(join(dir, 'enc_categ.pkl')),
                'text': load(join(dir, 'enc_text.pkl'))
            },
            '002': {
                'location': load(join(dir, 'location.pkl')),
                'contract': load(join(dir, 'contract.pkl'))
            }
        }
        self._clf = {
            '001': load(join(dir, 'model.pkl')),
            '002': load(join(dir, 'model2.pkl'))
        }

    def run(
        self,
        data: Dict = None,
        model_id: str = ''
    ) -> float:
        x = None
        str_cols = ['location', 'contract']
        _clf = self._clf[model_id]
        _enc = self._enc[model_id]

        if model_id == '001':
            if data == None:
                x = random(m=1, n=24627)
            else:
                df = DataFrame(data, index=[0])
                df.fillna('NaN', inplace=True)
                for col in df:
                    df[col] = df[col].str.lower()
                    df[col] = df[col].replace('[^a-zA-Z0-9]',
                                              ' ', regex=True)

                x_categ = _enc['categ'].transform(
                    df[str_cols].to_dict('records'))
                x_text = _enc['text'].transform(df['description'])
                x = hstack([x_text, x_categ])

        elif model_id == '002':
            if data == None:
                x = random(m=1, n=26)
            else:
                df = DataFrame(data, index=[0])
                df.fillna('NaN', inplace=True)
                df.description = df.description.apply(
                    lambda x: {d: x.lower().count(d) for d in 'abcdefghijklmnopqrstuvwxyz'})

                x = DataFrame(list(df.description.values))

                x['location'] = _enc['location'].transform(df.location)
                x['contract'] = _enc['contract'].transform(df.contract)

        else:
            return {
                'model_id': model_id,
                'error': 'Model not found',
                'result_code': 1
            }

        return {
            'model_id': model_id,
            'salary': _clf.predict(x)[0],
            'result_code': 0
        }
