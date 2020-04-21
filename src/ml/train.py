#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Предобработка" data-toc-modified-id="Предобработка-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Предобработка</a></span></li><li><span><a href="#Выделение-признаков" data-toc-modified-id="Выделение-признаков-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Выделение признаков</a></span><ul class="toc-item"><li><span><a href="#Категориальные" data-toc-modified-id="Категориальные-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Категориальные</a></span></li><li><span><a href="#TF-IDF-признаки-из-текста" data-toc-modified-id="TF-IDF-признаки-из-текста-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>TF-IDF-признаки из текста</a></span></li><li><span><a href="#Объединение-признаков" data-toc-modified-id="Объединение-признаков-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Объединение признаков</a></span></li></ul></li><li><span><a href="#Обучение-гребневой-линейной-регрессии" data-toc-modified-id="Обучение-гребневой-линейной-регрессии-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Обучение гребневой линейной регрессии</a></span></li><li><span><a href="#Предсказание" data-toc-modified-id="Предсказание-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Предсказание</a></span></li><li><span><a href="#Сохранение-модели" data-toc-modified-id="Сохранение-модели-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Сохранение модели</a></span></li><li><span><a href="#Загрузка-модели" data-toc-modified-id="Загрузка-модели-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Загрузка модели</a></span></li><li><span><a href="#Предсказание-на-случайном-примере" data-toc-modified-id="Предсказание-на-случайном-примере-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Предсказание на случайном примере</a></span></li></ul></div>

# In[ ]:


from joblib import dump
from numpy import round, savetxt
from pandas import read_csv
from scipy.sparse import hstack
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge


# In[ ]:


data_train = read_csv(
    'data/salary-train.csv'
)

data_test = read_csv(
    'data/salary-test-mini.csv'
)


# In[ ]:


data_train.iloc[:100, :].to_csv(
    'data/salary-train-short.csv',
    index=False
)


# In[ ]:


data_train.info()


# In[ ]:


data_train


# In[ ]:


data_test


# # Предобработка

# In[ ]:


strCols = [
    'LocationNormalized',
    'ContractTime'
]


# In[ ]:


# производим замену пропущенных значений на специальные
# строковые величины (например, 'nan')
data_train.loc[:, strCols] = data_train.loc[:, strCols].fillna('nan')
data_test.loc[:, strCols] = data_test.loc[:, strCols].fillna('nan')


# In[ ]:


data_train.info()


# In[ ]:


data_train


# In[ ]:


data_test


# In[ ]:


for col in data_train:
    if data_train[col].dtype == object:
        data_train[col] = data_train[col].str.lower()
        data_test[col] = data_test[col].str.lower()

        # заменим все, кроме букв и цифр, на пробелы — это облегчит
        # дальнейшее разделение текста на слова
        data_train[col] = data_train[col].replace('[^a-zA-Z0-9]',
                                                  ' ',
                                                  regex=True)
        data_test[col] = data_test[col].replace('[^a-zA-Z0-9]',
                                                ' ',
                                                regex=True)


# In[ ]:


data_train.info()


# In[ ]:


data_train


# In[ ]:


data_test


# # Выделение признаков

# ## Категориальные
# one-hot кодировка

# In[ ]:


for col in strCols:
    print(data_train[col].value_counts(dropna=False))
    print()


# In[ ]:


# кодирование категориальных признаков one-hot-кодированием

enc_categ = DictVectorizer()
X_train_categ = enc_categ.fit_transform(
    data_train[strCols].to_dict('records')
)
X_test_categ = enc_categ.transform(
    data_test[strCols].to_dict('records')
)


# In[ ]:


X_train_categ


# In[ ]:


X_test_categ


# In[ ]:


enc_categ.get_feature_names()


# ## TF-IDF-признаки из текста

# In[ ]:


enc_text = TfidfVectorizer(min_df=5/len(data_train))
X_train_text = enc_text.fit_transform(
    data_train['FullDescription']
)
X_test_text = enc_text.transform(
    data_test['FullDescription']
)


# In[ ]:


enc_text.get_feature_names()


# In[ ]:


X_train_text


# In[ ]:


X_test_text


# ## Объединение признаков

# In[ ]:


X_train = hstack([
    X_train_text,
    X_train_categ
])
X_test = hstack([
    X_test_text,
    X_test_categ
])


# In[ ]:


X_train


# In[ ]:


X_test


# # Обучение гребневой линейной регрессии

# In[ ]:


clf = Ridge(
    alpha=1,
    random_state=241
)
clf


# In[ ]:


clf.fit(
    X=X_train,
    y=data_train['SalaryNormalized']
)


# # Предсказание

# In[ ]:


pred = round(clf.predict(
    X=X_test
), 2)
pred


# In[ ]:


pred


# In[ ]:


savetxt(
    fname='pred.csv',
    X=pred,
    fmt='%f',
    delimiter=','
)


# # Сохранение модели

# In[ ]:


clfFile = 'model.pkl'


# In[ ]:


dump(
    value=clf,
    filename=clfFile,
    compress=9
)


# # Загрузка модели

# In[ ]:


from joblib import load
from scipy.sparse import random


# In[ ]:


clfFile = 'model.pkl'


# In[ ]:


clf = load(
    filename=clfFile
)
clf


# # Предсказание на случайном примере

# In[ ]:


X_rand = random(
    m=1,  # количество объектов
    n=24627,
    random_state=clf.get_params()['random_state']  # необязательно
)
X_rand


# In[ ]:


pred = clf.predict(
    X=X_rand
)
pred

