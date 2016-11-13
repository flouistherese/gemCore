import pdb
from datetime import date
from gemTradingData.units import *
from limits import *

def create_orders(target_positions, current_positions, trading_env, market_env, orders_date = date.today()):
	pdb.set_trace()
	target_positions = target_positions[target_positions['date'] == orders_date]
	target_positions = scale_positions_to_capital(target_positions, trading_env.accounts)
	target_positions = add_target_instruments(target_positions, trading_env.target_instruments)

	target_positions = apply_limits(target_positions, market_env, trading_env)
	#TODO: Apply limits
	#Convert target pos from pos to Market
	target_positions = convert_units(target_positions, 'Market', market_env)

	current_positions['date'] = date.today()
	current_positions['unit'] = 'Market'
	current_positions = current_positions.merge(trading_env.model_feeds)
	
	

	#Diff with target to get orders
	#Convert 
def scale_positions_to_capital(positions, accounts):
	positions = positions.merge(accounts[['account_group', 'account', 'scaling']])
	positions['position'] = positions['position'] * positions['scaling']
	return positions.drop('scaling', 1)

def add_target_instruments(positions, target_instruments):
	return positions.merge(target_instruments)