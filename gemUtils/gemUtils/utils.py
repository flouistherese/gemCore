from datetime import date
import os.path

def default_dated_directory(date = date.today()):
	return str(os.path.join('/home/florian/Dropbox/Code/gemDB/market_environment', str(date)))