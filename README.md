# weather
Что делает сервис:
* Запрашивает данные о погоде используя Yandex weather API.
* Записывает полученные данные в БД
* На страницу выводит последнюю запись из БД

<img src="https://github.com/mirisu2/weather/blob/master/static/bcd321da-ec87-44b5-9880-e43115f4151a.jpeg" width='540'>

> Запросы к API каждый час (можно поменять в scheduler в weather.py)