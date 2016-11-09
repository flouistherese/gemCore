from strategy import Strategy
import pandas as pd
from datetime import date
import pdb

class Momentum(Strategy):

	strategy_type = None
	models = list()
	model_feeds = pd.DataFrame()
	price_data = pd.DataFrame()

	def __init__(self, market_env, trading_env):
		pdb.set_trace()
		strategy_type = 'MOMENTUM'
		strategies = trading_env.strategies[trading_env.strategies['strategy_type'] == strategy_type]['code'].tolist()
		models = trading_env.trading_models[trading_env.trading_models['enabled'] & trading_env.trading_models['strategy'].isin(strategies)]['code'].tolist()
		model_feeds = trading_env.model_feeds[trading_env.model_feeds['trading_model'].isin(models)]
		

	def update_market_data(self, market_environment, start_date = date.today() - 365 * 25, end_date = date.today()):
		price_data = market_env.feed_data[market_env.feed_data['feed'].isin(model_feeds['feed'])]

	def run():
		raise NotImplementedError()


