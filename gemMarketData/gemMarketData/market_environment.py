import pandas as pd
from datetime import date
import cPickle as pickle
import os.path
from gemUtils.utils import default_dated_directory

class MarketEnvironment:

	currencies = pd.DataFrame()
	currency_pairs = pd.DataFrame()
	instruments = pd.DataFrame()
	instrument_families = pd.DataFrame()
	exchanges = pd.DataFrame()
	futures = pd.DataFrame()
	future_contracts = pd.DataFrame()
	stocks = pd.DataFrame()
	stock_data = pd.DataFrame()
	feed_data = pd.DataFrame()
	fx_forwards = pd.DataFrame()
	fx_spot = pd.DataFrame()

	@staticmethod
	def load(date_directory = date.today(), file_path = None):
			if file_path is None:
				file_path = os.path.join(default_dated_directory(date_directory), 'market_environment')

			if not os.path.exists(file_path):
				raise Exception('No market environment was found for ' + str(date_directory))

			with open(file_path, 'rb') as f:
				return pickle.load(f)