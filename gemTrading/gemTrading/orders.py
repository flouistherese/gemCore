import pdb
from datetime import date

def create_orders(target_positions, current_positions, trading_env, market_env, orders_date = date.today()):
	pdb.set_trace()
	target_positions = target_positions[target_positions['date'] == orders_date]
	target_positions = scale_positions_to_capital(target_positions, trading_env.accounts)
	

def scale_positions_to_capital(positions, accounts):
	positions = positions.merge(accounts[['account_group', 'account', 'scaling']])
	positions['position'] = positions['position'] * positions['scaling']
	return positions.drop('scaling', 1)