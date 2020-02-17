# -*- coding: utf-8 -*-
import logging
import logging.handlers as handlers
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, jsonify
import requests
import re
from config import API_KEY, url
from models import Weather, session


logger = logging.getLogger('__weather__')
logger.setLevel(logging.DEBUG)
ch_file = handlers.RotatingFileHandler('logs/weather.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch_file.setFormatter(formatter)
logger.addHandler(ch_file)

app = Flask(__name__)
scheduler = BackgroundScheduler()


def get_data_from_api():
    try:
        logger.info('Making request...')
        req = requests.get(url, headers={'X-Yandex-API-Key': API_KEY})

        if req.status_code == 200:
            logger.info(f'req.status_code: {req.status_code}')
            req_json = req.json()
            logger.info(req_json)
            curr = Weather(
                pressure=req_json['fact']['pressure_mm'],
                temp=req_json['fact']['temp'],
                feels_like=req_json['fact']['feels_like'],
                wind_speed=req_json['fact']['wind_speed'],
                wind_dir=req_json['fact']['wind_dir'],
                humidity=req_json['fact']['humidity'],
                obs_time=req_json['fact']['obs_time'],
                season=req_json['fact']['season']
            )
            session.add(curr)
            session.commit()
            if curr.id:
                logger.info(f'Insert new record ID:{curr.id}')
            else:
                logger.error('Cant\'t add new record')

        elif req.status_code == 403:
            logger.error(f'req.status_code: {req.status_code}')

    except requests.exceptions.ConnectionError as e:
        logger.error(f'ConnectionError: {e}')


scheduler.add_job(get_data_from_api, 'cron', minute=45, max_instances=1)
scheduler.start()


@app.route('/')
def show_weather():
    wind_dirs = {
        'nw':'северо-западное',
        'n': 'северное',
        'ne': 'северо-восточное',
        'e': 'восточное',
        'se': 'юго-восточное',
        's': 'южное',
        'sw': 'юго-западное',
        'w': 'западное',
        'с': 'штиль'
    }
    last_record = Weather.get_last_weather()
    last_record['wind_dir'] = wind_dirs[last_record['wind_dir']]
    return render_template('index.html', last_record=last_record)


@app.route('/api/weather/<date>', methods=['GET'])
def last_week(date):
    if re.search('\d\d\d\d-\d\d-\d\d', date):
        labels = []
        temp = []
        feels_like = []
        pressure = []
        humidity = []
        selected_day = Weather.get_selected_day(date)
        for i in selected_day:
            labels.append(i['obs_time'])
            temp.append(i['temp'])
            feels_like.append(i['feels_like'])
            pressure.append(i['pressure'])
            humidity.append(i['humidity'])

        return jsonify({
            'status': True,
            'labels': labels,
            'temp': temp,
            'feels_like': feels_like,
            'pressure': pressure,
            'humidity': humidity
        })
    else:
        return jsonify({'error': 'Wrong format'})



logger.info('Starting app...')
