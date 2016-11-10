from strategy import Strategy
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
from gemTradingData.trading_environment import TradingEnvironment
import pdb

class Momentum(Strategy):
	#Models
	strategy_type = None
	models = list()
	model_feeds = pd.DataFrame()

	#Market Data
	price_data = pd.DataFrame()

	#Gearings
	gearings = pd.DataFrame()

	#Positions
	raw_positions = pd.DataFrame()
	geared_positions = pd.DataFrame()

	def __init__(self, market_env, trading_env):
		self.strategy_type = 'MOMENTUM'
		strategies = trading_env.strategies[trading_env.strategies['strategy_type'] == self.strategy_type]['strategy'].tolist()
		self.models = trading_env.trading_models[trading_env.trading_models['enabled'] & trading_env.trading_models['strategy'].isin(strategies)]['trading_model'].tolist()
		self.model_feeds = trading_env.model_feeds[trading_env.model_feeds['trading_model'].isin(self.models)]
		

	def update_market_data(self, market_env, start_date = date.today() + timedelta(days = 365 * 25), end_date = date.today()):
		self.price_data = market_env.feed_data[market_env.feed_data['feed'].isin(self.model_feeds['feed'])]

	def update_parameters(self,trading_env):
		pdb.set_trace()
		self.gearings = trading_env.extract_gearing()

	def run(self):
		dates = self.price_data['date'].copy()
		dates.sort_values(inplace=True)
		self.raw_positions = pd.DataFrame(dates)
		self.raw_positions['account_group'] = 'MAIN'
		self.raw_positions['trading_model'] = 'ENERGY_MOM_CL'
		self.raw_positions['feed'] = 'CL1'
		self.raw_positions['unit'] = 'USD'
		self.raw_positions['position'] = pd.Series(np.random.randn(len(self.raw_positions))) * 100
		pdb.set_trace()

		self.geared_positions = self.raw_positions * 2000



		


