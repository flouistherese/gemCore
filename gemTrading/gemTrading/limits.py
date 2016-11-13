import pdb
import pandas as pd

def apply_limits(positions, trading_env):
	limited_positions = positions.copy()

	pdb.set_trace()
	limited_positions = apply_model_limits(limited_positions, trading_env)
	limited_positions = apply_strategy_limits(limited_positions, trading_env)
	limited_positions = apply_sector_limits(limited_positions, trading_env)

	return limited_positions

def apply_model_limits(positions, trading_env):
	if len(trading_env.model_limits) == 0:
		return positions
	
	model_limits = trading_env.model_limits.copy()
	model_limits = scale_limits_to_account(model_limits, trading_env.accounts)
	limited_positions = positions.merge(model_limits, how = 'left')
	limited_positions['position'] = limited_positions['position'].combine(limited_positions['limit'], min, 0 )

	limited_positions.ix[limited_positions.side == 'SHORT','position'] = limited_positions[limited_positions.side == 'SHORT'][['position', 'limit']].max(axis = 1)
	limited_positions.ix[limited_positions.side == 'LONG','position'] = limited_positions[limited_positions.side == 'LONG'][['position', 'limit']].min(axis = 1)

	#Select most conservation position for each date + model + account
	limited_positions = limited_positions.iloc[limited_positions.groupby(['date', 'account', 'trading_model']).apply(lambda x: x['position'].abs().idxmin())]

	return limited_positions.drop(['side', 'limit'], axis = 1)

def apply_strategy_limits(positions, trading_env):
	return positions

def apply_sector_limits(positions, trading_env):
	return positions

def scale_limits_to_account(limits, accounts):
	limits = limits.merge(accounts[['account', 'scaling']])
	limits.ix[limits.limit_type == 'ABSOLUTE','scaling'] = 1.0
	limits['limit'] = limits['limit'].astype('float64') * limits['scaling']
	return limits.drop(['scaling','limit_type'], axis = 1)

