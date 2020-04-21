from os.path import abspath, dirname, join

from joblib import load
from pandas import DataFrame
from scipy.sparse import hstack, random


class Clf():
    enc_categ = None
    enc_text = None
    clf = None

    def __init__(self):
        dir = dirname(abspath(__file__))
        self.enc_categ = load(join(dir, 'enc_categ.pkl'))
        self.enc_text = load(join(dir, 'enc_text.pkl'))
        self.clf = load(join(dir, 'model.pkl'))

    def run(
        self,
        data = None
    ) -> float:
        if data == None:
            X = random(m=1, n=24627)
        else:
            strCols = ['LocationNormalized', 'ContractTime']
            df = DataFrame(data, index=[0])
            df.loc[:, strCols] = df.loc[:, strCols].fillna('nan')
            for col in df:
                df[col] = df[col].str.lower()
                df[col] = df[col].replace('[^a-zA-Z0-9]',
                                                ' ', regex=True)
            X_categ = self.enc_categ.transform(df[strCols].to_dict('records'))
            X_text = self.enc_text.transform(df['FullDescription'])
            X = hstack([X_text, X_categ])
        return self.clf.predict(X=X)[0]
