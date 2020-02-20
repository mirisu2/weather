from flask import Blueprint, jsonify
import re
from weather.db import get_db
from weather.logger import logger


bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/<date>', methods=['GET'])
def last_week(date):
    logger.debug(date)
    if re.search('\d\d\d\d-\d\d-\d\d', date):
        logger.debug(date)
        labels = []
        temp = []
        feels_like = []
        pressure = []
        humidity = []

        connection = get_db()
        with connection.cursor() as cursor:
            sql = "SELECT id, pressure, temp, feels_like, humidity, FROM_UNIXTIME(obs_time) AS obs_time FROM yandex_weather WHERE date LIKE '{}%'".format(date)
            logger.debug(sql)
            cursor.execute(sql)
            result = cursor.fetchall()

            logger.debug(result)

            for i in result:
                labels.append(str(i['obs_time']))
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
