from pandas import read_csv
from requests import post

data_test = read_csv(
    '../src/ml/data/salary-test-mini.csv'
)

for idx in data_test.index:
    answer = post(
        url='http://localhost:5017/',
        json=data_test.loc[idx].to_dict()
            )
    print(answer)
    response = answer.json()
    print(response)
