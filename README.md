# Salary prediction

Требования:

- права sudo пользователя
- requirements.txt
- скачать в `src/ml/data` [данные](https://drive.google.com/file/d/1qhXw8C2FxOvGN9sPvrQ75CoOyP64rgk0/view?usp=sharing)

Запустить Gunicorn:

    sudo make

или

    sudo make guni

Зарегистрировать сервис:

    sudo make service

Зарегистрировать сайт в Nginx:

    sudo make site

Проверить состояние сервиса:

    sudo make status

Удалить сервис:

    sudo make service_rm

Удалить сайт в Nginx:

    sudo make site_rm

Зарегистрировать сервис и сайт в Nginx:

    sudo make all

Удалить сервис и сайт в Nginx:

    sudo make clean
