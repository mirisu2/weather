from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import config

engine = create_engine(f"mysql+pymysql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}",
                       echo=False)
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
        return session.execute('SELECT id, pressure, temp, feels_like, wind_speed, wind_dir, humidity, '
                               'FROM_UNIXTIME(obs_time) AS obs_time FROM yandex_weather ORDER BY id DESC '
                               'LIMIT 1').fetchone()

