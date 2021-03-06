from strategy import Strategy
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
import warnings
from gemTradingData.trading_environment import TradingEnvironment
import pdb

class Momentum(Strategy):
	

	def __init__(self, market_env, trading_env):
		self.strategy_type = 'MOMENTUM'
		strategies = trading_env.strategies[trading_env.strategies['strategy_type'] == self.strategy_type]['strategy'].tolist()
		self.models = trading_env.trading_models[trading_env.trading_models['enabled'] & trading_env.trading_models['strategy'].isin(strategies)]['trading_model'].tolist()
		self.model_feeds = trading_env.model_feeds[trading_env.model_feeds['trading_model'].isin(self.models)]

		##Warn when feeds cant be found for required models
		missing_models = set(self.models) - set(self.model_feeds['trading_model'])
		if(len(missing_models) > 0):
			warnings.warn("No feed found for models " + ', '.join(missing_models))

	def update_market_data(self, market_env, start_date = date.today() + timedelta(days = 365 * 25), end_date = date.today()):
		feed_data = market_env.feed_data[market_env.feed_data['feed'].isin(self.model_feeds['feed'])]
		fx_data = market_env.fx_spot[market_env.fx_spot['feed'].isin(self.model_feeds['feed'])]
		self.price_data = pd.concat([feed_data, fx_data])

	def update_parameters(self,trading_env):
		self.gearings = trading_env.extract_gearing()

		##Warn when gearing cant be found for required models
		missing_models = set(self.models) - set(self.gearings['trading_model'])
		if(len(missing_models) > 0):
			warnings.warn("No gearing found for models " + ', '.join(missing_models))

	def run(self):
		dates = self.price_data['date'].drop_duplicates().copy()
		dates.sort_values(inplace=True)
		raw_positions1 = pd.DataFrame(dates)
		raw_positions1['account_group'] = 'MAIN'
		raw_positions1['trading_model'] = 'ENERGY_MOM_CL'
		raw_positions1['feed'] = 'CL1'
		raw_positions1['unit'] = 'USD'
		raw_positions1['position'] = pd.Series(np.random.randn(len(raw_positions1))) * 100
		raw_positions2 = pd.DataFrame(dates)
		raw_positions2['account_group'] = 'MAIN'
		raw_positions2['trading_model'] = 'BOND_MOM_TY'
		raw_positions2['feed'] = 'TY1'
		raw_positions2['unit'] = 'USD'
		raw_positions2['position'] = pd.Series(np.random.randn(len(raw_positions2))) * 100
		raw_positions3 = pd.DataFrame(dates)
		raw_positions3['account_group'] = 'MAIN'
		raw_positions3['trading_model'] = 'FX_MOM_GBP'
		raw_positions3['feed'] = 'GBPUSD'
		raw_positions3['unit'] = 'USD'
		raw_positions3['position'] = pd.Series(np.random.randn(len(raw_positions3))) * 100
		raw_positions4 = pd.DataFrame(dates)
		raw_positions4['account_group'] = 'MAIN'
		raw_positions4['trading_model'] = 'ENERGY_MOM_NG'
		raw_positions4['feed'] = 'NG1'
		raw_positions4['unit'] = 'USD'
		raw_positions4['position'] = pd.Series(np.random.randn(len(raw_positions4))) * 100

		self.raw_positions = pd.concat([raw_positions1, raw_positions2, raw_positions3, raw_positions4])



		


