from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import config

engine = create_engine(f"mysql+pymysql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}",
                       echo=False, pool_pre_ping=True, pool_recycle=600)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Weather(Base):
    __tablename__ = 'yandex_weather'
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    pressure = Column(INTEGER(unsigned=True), nullable=False, comment='Давление (в мм рт. ст.)')
    temp = Column(Integer, nullable=False, comment='Температура (°C)')
    feels_like = Column(Integer, nullable=False, comment='Ощущаемая температура (°C)')
    wind_speed = Column(INTEGER(unsigned=True), nullable=False, comment='Скорость ветра (в м/с)')
    wind_dir = Column(String(3), nullable=False, comment='Направление ветра.')
    humidity = Column(INTEGER(unsigned=True), nullable=False, comment='Влажность воздуха (в процентах)')
    obs_time = Column(INTEGER(unsigned=True), nullable=False,
                      comment='Время замера погодных данных в формате Unixtime.')
    season = Column(String(6), nullable=False)

    def get_last_weather():
        record = session.execute('SELECT id, pressure, temp, feels_like, wind_speed, wind_dir, humidity, '
                               'FROM_UNIXTIME(obs_time) AS obs_time FROM yandex_weather ORDER BY id DESC '
                               'LIMIT 1').fetchone()
        return {
            'pressure': record.pressure,
            'temp': record.temp,
            'feels_like': record.feels_like,
            'wind_speed': record.wind_speed,
            'wind_dir': record.wind_dir,
            'humidity': record.humidity,
            'obs_time': record.obs_time
        }

    def get_selected_day(day):
        res = session.execute('SELECT id, pressure, temp, feels_like, humidity, FROM_UNIXTIME(obs_time) AS obs_time '
                              'FROM yandex_weather WHERE date LIKE \'' + day + '%\'').fetchall()
        answer = []
        for i in res:
            answer.append({
                'obs_time': str(i[5]).split(' ')[1],
                'pressure': i[1],
                'temp': i[2],
                'feels_like': i[3],
                'humidity': i[4]
            })
        return answer

