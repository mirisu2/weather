import logging
import logging.handlers as handlers
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
import requests
from config import API_KEY, url
from models import Weather, session


logger = logging.getLogger('__weather__')
logger.setLevel(logging.INFO)
ch_file = handlers.RotatingFileHandler('weather.log', maxBytes=1000000, backupCount=5)
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


scheduler.add_job(get_data_from_api, 'cron', minute=55, max_instances=1)
scheduler.start()


@app.route('/')
def show_weather():
    last_record = Weather.get_last_weather()
    return render_template('index.html', last_record=last_record)


logger.info('Starting app...')
# app.run()
