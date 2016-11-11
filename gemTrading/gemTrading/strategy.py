import pandas as pd
from gemPortfolio.gearing import apply_gearing

class Strategy:

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

	def __init__(self, trading_environment):
		raise NotImplementedError()

	def update_parameters(self,trading_env):
		raise NotImplementedError()

	def update_market_data(self, market_environment):
		raise NotImplementedError()

	def run(self):
		raise NotImplementedError()

	def apply_gearing(self):
		self.geared_positions = apply_gearing(self.raw_positions, self.gearings)

