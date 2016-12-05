from datetime import date
import os.path
import pdb
import logging

def default_dated_directory(date = date.today()):
	return str(os.path.join('/home/flouistherese/python/market_environment', str(date)))

def create_logger(file_path = None):
	logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
	logger = logging.getLogger('gem_logger')
	logger.setLevel(logging.DEBUG)

	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	logger.addHandler(consoleHandler)

	if file_path is not None:
		fileHandler = logging.FileHandler(file_path)
		fileHandler.setFormatter(logFormatter)
		logger.addHandler(fileHandler)

	return logger
