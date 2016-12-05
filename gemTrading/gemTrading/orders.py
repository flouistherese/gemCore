import pdb
from datetime import date
from gemTradingData.units import *
from limits import *
import logging

logger = logging.getLogger('gem_logger')

def create_orders(target_positions, current_positions, trading_env, market_env, orders_date = date.today()):
	target_positions = target_positions[target_positions['date'] == orders_date]
	target_positions = scale_positions_to_capital(target_positions, trading_env.accounts)
	target_positions = add_target_instruments(target_positions, trading_env.target_instruments)

	logger.info('Applying limits')
	target_positions = apply_limits(target_positions, market_env, trading_env)
	target_positions = convert_units(target_positions, 'Market', market_env)
	target_positions = round_positions(target_positions, trading_env)
	target_positions = target_positions.drop('date', axis = 1)
	
	current_positions['unit'] = 'Market'
	current_positions = current_positions.merge(trading_env.model_feeds)
	
	orders = calculate_orders(current_positions, target_positions)

	#TODO: Interleaving

	return orders
	
def scale_positions_to_capital(positions, accounts):
	positions = positions.merge(accounts[['account_group', 'account', 'scaling']])
	positions['position'] = positions['position'] * positions['scaling']
	return positions.drop('scaling', 1)

def add_target_instruments(positions, target_instruments):
	missing_models = set(positions['trading_model']) - set(target_instruments['trading_model'])
	if(len(missing_models) > 0):
		logger.warning("No target instruments found for models " + ', '.join(missing_models))
	return positions.merge(target_instruments)

def calculate_orders(current_positions, target_positions):
	if 'position' in current_positions.columns:
		current_positions.rename(columns={'position':'current_position'}, inplace = True)

	if 'position' in target_positions.columns:
		target_positions.rename(columns={'position':'target_position'}, inplace = True)

	missing_current_positions = set(target_positions['trading_model'].unique()) - set(current_positions['trading_model'].unique())
	missing_target_positions = set(current_positions['trading_model'].unique()) - set(target_positions['trading_model'].unique())

	if(len(missing_current_positions)):
		logger.warning("No current positions found for models " + ', '.join(missing_current_positions))

	if(len(missing_target_positions)):
		logger.warning("No target positions found for models " + ', '.join(missing_target_positions))
	
	orders = target_positions.merge(current_positions, how = 'outer')

	orders['current_position'] = orders['current_position'].fillna(int(0))
	orders['target_position'] = orders['target_position'].fillna(int(0))

	columns = ['account_group', 'account', 'trading_model', 'feed', 'instrument_type', 'instrument', 'unit', 'current_position', 'target_position']
	orders = orders[columns]

	orders['amount'] = orders['target_position'] - orders['current_position']	

	return orders.drop(['current_position', 'target_position'], axis = 1)