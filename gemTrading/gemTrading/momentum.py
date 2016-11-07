from strategy import Strategy
import pdb

class Momentum(Strategy):

	models = list()
	
	def __init__(self, trading_env):
		pdb.set_trace()
		strategy_type = 'MOMENTUM'
		strategies = trading_env.strategies[trading_env.strategies['strategy_type'] == strategy_type]['code'].tolist()
		models = trading_env.trading_models[trading_env.trading_models['enabled'] & trading_env.trading_models['strategy'].isin(strategies)]['code'].tolist()
		

	def update_market_data(self, market_environment):
		raise NotImplementedError()

	def run():
		raise NotImplementedError()


