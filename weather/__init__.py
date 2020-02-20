import requests
from flask_apscheduler import APScheduler
from flask import Flask, render_template, current_app

from weather import db
from weather.logger import logger


def get_data_from_api():
    API_KEY = 'egerg'
    LAT = 00.123123123
    LON = 11.123123123
    LANG = 'ru_RU'
    url = f'https://api.weather.yandex.ru/v1/informers?lat={LAT}&lon={LON}&lang=[{LANG}]'

    req = requests.get(url, headers={'X-Yandex-API-Key': API_KEY})

    if req.status_code == 200:
        req_json = req.json()

        connection = db.get_db()
        with connection.cursor() as cursor:
            sql = 'INSERT INTO yandex_weather (pressure, temp, feels_like, wind_speed, wind_dir, humidity, obs_time, ' \
                  'season) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (
                req_json['fact']['pressure_mm'],
                req_json['fact']['temp'],
                req_json['fact']['feels_like'],
                req_json['fact']['wind_speed'],
                req_json['fact']['wind_dir'],
                req_json['fact']['humidity'],
                req_json['fact']['obs_time'],
                req_json['fact']['season']
            ))
            connection.commit()
            if cursor.rowcount:
                logger.info('Just insert new record')


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')


    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()


    from weather.api.v1 import endpoints
    app.register_blueprint(endpoints.bp)


    @app.route('/')
    def show_weather():
        wind_dirs = {
            'nw': 'северо-западное',
            'n': 'северное',
            'ne': 'северо-восточное',
            'e': 'восточное',
            'se': 'юго-восточное',
            's': 'южное',
            'sw': 'юго-западное',
            'w': 'западное',
            'с': 'штиль'
        }
        connection = db.get_db()
        with connection.cursor() as cursor:
            sql = 'SELECT id, pressure, temp, feels_like, wind_speed, wind_dir, humidity, FROM_UNIXTIME(obs_time) ' \
                  'AS obs_time FROM yandex_weather ORDER BY id DESC LIMIT 1'
            cursor.execute(sql)
            last_record = cursor.fetchone()
            last_record['wind_dir'] = wind_dirs[last_record['wind_dir']]
        return render_template('index.html', last_record=last_record)

    logger.info('Starting app...')

    return app
