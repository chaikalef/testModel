from typing import Dict

from joblib import load
from pandas import DataFrame
from scipy.sparse import hstack, random
from sklearn.feature_extraction import DictVectorizer

from .conf import FEATURES_NUMBER
from .utils import preproc


def predict(
    enc,
    data: Dict = None
) -> float:
    if not(data is None):
        strCols = ['LocationNormalized', 'ContractTime']
        data = DataFrame(data, index=[0])
        data = preproc(df=data, strCols=strCols)

        enc_categ = DictVectorizer()
        X_categ = enc_categ.fit_transform(data[strCols].to_dict('records'))

        enc_text = enc
        X_text = enc_text.transform(data['FullDescription'])

        X = hstack([X_text, X_categ])

    else:
        # Предсказание на случайном примере
        X = random(
            m=1,  # количество объектов
            n=FEATURES_NUMBER
        )

    clf = load(filename='src/ml/model.pkl')
    return clf.predict(X=X)[0]
