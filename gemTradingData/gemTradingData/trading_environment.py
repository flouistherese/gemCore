import pandas as pd
from datetime import date
import cPickle as pickle
import os.path
from gemUtils.utils import default_dated_directory


class TradingEnvironment:
	strategies = pd.DataFrame()
	trading_models = pd.DataFrame()
	model_feeds = pd.DataFrame()
	
	@staticmethod
	def load(date_directory = date.today(), file_path = None):
		if file_path is None:
			file_path = os.path.join(default_dated_directory(date_directory), 'trading_environment')

		if not os.path.exists(file_path):
			raise Exception('No trading environment was found for ' + date_directory)

		with open(file_path, 'rb') as f:
			return pickle.load(f)