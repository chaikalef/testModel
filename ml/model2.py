import pandas as pd
from joblib import load

df = None

df.fillna('NaN', inplace=True)
df.text = df.text.apply(lambda x: {d: x.lower().count(d)
                                   for d in 'abcdefghijklmnopqrstuvwxyz'})

location = load('location.pkl')
contract = load('contract.pkl')
model = load('model2.pkl')

X = pd.DataFrame(list(df.text.values))

X['location'] = location.transform(df.location)
X['contract'] = contract.transform(df.contract)

model.predict(X)[0]
