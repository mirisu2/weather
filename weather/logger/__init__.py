import logging
import logging.handlers as handlers


logger = logging.getLogger('__weather__')
logger.setLevel(logging.INFO)
ch_file = handlers.RotatingFileHandler('logs/weather.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch_file.setFormatter(formatter)
logger.addHandler(ch_file)
