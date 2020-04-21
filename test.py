from pandas import read_csv
from requests import post

data_test = read_csv('data.csv')
for i in range(len(data_test)):
    answer = post(url='http://localhost:5017/predict',
                  json=data_test.iloc[i, :-1].to_dict())
    print(answer)
    print(answer.json())
