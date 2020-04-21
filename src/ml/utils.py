from typing import List

from pandas import DataFrame, read_csv


def preproc(
    df: DataFrame,
    strCols: List[str]
) -> DataFrame:
    res = df.copy()
    res.loc[:, strCols] = res.loc[:, strCols].fillna('nan')
    for col in res:
        if res[col].dtype == object:
            res[col] = res[col].str.lower()
            res[col] = res[col].replace('[^a-zA-Z0-9]',
                                        ' ', regex=True)
    return res

def getTextFeats(enc):
    text = read_csv('src/ml/data/salary-train.csv', usecols=[0])
    text = preproc(df=text, strCols=text.columns)
    enc.fit_transform(text['FullDescription'])
