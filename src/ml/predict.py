#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from os.path import abspath, join
from typing import Dict

from joblib import load
from pandas import DataFrame, read_csv
from requests import post
from scipy.sparse import hstack, random

# In[ ]:


def predict(
    data: Dict = None
) -> float:
    if data == None:
        X = random(m=1, n=24627)
    else:
        strCols = ['location', 'contract']
        df = DataFrame(data, index=[0])
        df.loc[:, strCols] = df.loc[:, strCols].fillna('nan')
        for col in df:
            df[col] = df[col].str.lower()
            df[col] = df[col].replace('[^a-zA-Z0-9]',
                                      ' ', regex=True)
        X_categ = enc_categ.transform(df[strCols].to_dict('records'))
        X_text = enc_text.transform(df['description'])
        X = hstack([X_text, X_categ])
    return clf.predict(X=X)[0]


# In[ ]:


dir = abspath('')
enc_categ = load(join(dir, 'enc_categ.pkl'))
enc_text = load(join(dir, 'enc_text.pkl'))
clf = load(join(dir, 'model.pkl'))

data_test = read_csv(join(dir, 'data/salary-test-mini.csv'))
data_test.columns = ['description', 'location',
                     'contract'] + [data_test.columns[-1]]

for i in range(len(data_test)):
    print(predict(data_test.iloc[i, :-1].to_dict()))
