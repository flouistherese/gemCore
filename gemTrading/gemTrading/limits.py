import pdb
import pandas as pd

def apply_limits(positions, market_env, trading_env):
	limited_positions = positions.copy()

	pdb.set_trace()
	limited_positions = apply_model_limits(limited_positions, trading_env)
	limited_positions = apply_asset_limits(limited_positions, trading_env)
	limited_positions = apply_sector_limits(limited_positions, market_env, trading_env)

	return limited_positions

def apply_model_limits(positions, trading_env):
	if len(trading_env.model_limits) == 0:
		return positions
	
	model_limits = scale_limits_to_account(trading_env.model_limits, trading_env.accounts)
	limited_positions = positions.merge(model_limits, how = 'left')
	limited_positions['position'] = limited_positions['position'].combine(limited_positions['limit'], min, 0 )

	limited_positions.ix[limited_positions.side == 'SHORT','position'] = limited_positions[limited_positions.side == 'SHORT'][['position', 'limit']].max(axis = 1)
	limited_positions.ix[limited_positions.side == 'LONG','position'] = limited_positions[limited_positions.side == 'LONG'][['position', 'limit']].min(axis = 1)

	#Select most conservation position for each date + model + account
	limited_positions = limited_positions.iloc[limited_positions.groupby(['date', 'account', 'trading_model']).apply(lambda x: x['position'].abs().idxmin())]

	return limited_positions.drop(['side', 'limit'], axis = 1)

def apply_asset_limits(positions, trading_env):
	return positions

def apply_sector_limits(positions, market_env, trading_env):
	pdb.set_trace()
	sector_limits = scale_limits_to_account(trading_env.sector_limits, trading_env.accounts)

	limited_positions = positions.merge(market_env.instruments[['instrument', 'instrument_family']]).merge(market_env.instrument_families)
	sector_exposure = pd.DataFrame({'sector_exposure':limited_positions.groupby(['date','account','sector'])['position'].sum()}).reset_index()
	sector_exposure = sector_exposure.merge(sector_limits, how = 'left')
	sector_exposure['limit_scaling'] = 1.0

	sector_exposure.ix[sector_exposure.side == 'LONG','limit_scaling'] = sector_exposure[sector_exposure.side == 'LONG']['limit'] / sector_exposure[sector_exposure.side == 'LONG']['sector_exposure']
	sector_exposure.ix[sector_exposure.side == 'SHORT','limit_scaling'] = sector_exposure[sector_exposure.side == 'SHORT']['limit'] / sector_exposure[sector_exposure.side == 'SHORT']['sector_exposure']

	#Negative limit scaling means that exposure and limit are in different sides, so limit should not be applied
	sector_exposure.ix[(sector_exposure.limit_scaling < 0) | (sector_exposure.limit_scaling > 1), 'limit_scaling'] = 1.0

	#Select most conservation position for each date + sector + account
	sector_exposure = sector_exposure.iloc[sector_exposure.groupby(['date', 'account', 'sector']).apply(lambda x: x['limit_scaling'].idxmin())]

	limited_positions = limited_positions.merge(sector_exposure[['date', 'account', 'sector', 'limit_scaling']])
	limited_positions['position'] = limited_positions['position'] * limited_positions['limit_scaling']

	return limited_positions.drop(['instrument_family', 'sector', 'limit_scaling'], axis = 1)



	return positions

def scale_limits_to_account(limits, accounts):
	limits = limits.merge(accounts[['account', 'scaling']])
	limits.ix[limits.limit_type == 'ABSOLUTE','scaling'] = 1.0
	limits['limit'] = limits['limit'].astype('float64') * limits['scaling']
	return limits.drop(['scaling','limit_type'], axis = 1)

