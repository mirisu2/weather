# weather
Что делает сервис:
* Запрашивает данные о погоде используя Yandex weather API.
* Записывает полученные данные в БД
* На страницу выводит последнюю запись из БД
  
> Запросы к API каждый час (можно поменять в scheduler в weather.py)