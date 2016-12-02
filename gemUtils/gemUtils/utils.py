from datetime import date
import os.path
import pdb

def default_dated_directory(date = date.today()):
	return str(os.path.join('/home/flouistherese/python/market_environment', str(date)))