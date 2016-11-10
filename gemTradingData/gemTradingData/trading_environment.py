import pandas as pd
from datetime import date
import cPickle as pickle
import os.path
from gemUtils.utils import default_dated_directory


class TradingEnvironment:
	accounts = pd.DataFrame()

	#Models
	strategies = pd.DataFrame()
	trading_models = pd.DataFrame()
	model_feeds = pd.DataFrame()
	target_instruments = pd.DataFrame()

	#Limits
	model_limits = pd.DataFrame()
	sector_limits = pd.DataFrame()
	asset_limits = pd.DataFrame()

	#Portfolio Tree
	portfolio_weights = pd.DataFrame()
	strategy_type_gearings = pd.DataFrame()
	strategy_gearings = pd.DataFrame()
	strategy_type_weights = pd.DataFrame()
	strategy_weights = pd.DataFrame()
	model_weights = pd.DataFrame()
	
	@staticmethod
	def load(date_directory = date.today(), file_path = None):
		if file_path is None:
			file_path = os.path.join(default_dated_directory(date_directory), 'trading_environment')

		if not os.path.exists(file_path):
			raise Exception('No trading environment was found for ' + date_directory)

		with open(file_path, 'rb') as f:
			return pickle.load(f)

	def extract_gearing(self):
		gearings = self.portfolio_gearings.merge(self.strategy_types_gearings, on = ['account_group'])
		gearings = gearings.merge(self.strategy_types_weights, on = ['account_group','strategy_type'])
		gearings = gearings.merge(self.strategy_gearings, on = ['account_group','strategy_type'])
		gearings = gearings.merge(self.strategy_weights, on = ['account_group','strategy_type', 'strategy'])
		gearings['gearing'] = gearings['portfolio_gearing'] * gearings['strategy_types_gearing'] * gearings['strategy_gearing'] * gearings['strategy_types_weight'] * gearings['strategy_weight']
		return gearings[['account_group', 'strategy_type', 'strategy', 'gearing']]