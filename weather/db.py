import pymysql


def get_db():
    db = pymysql.connect(
        host='localhost',
        user='weather_user',
        password='werwerwerwer',
        db='weather',
        cursorclass=pymysql.cursors.DictCursor
    )

    return db
