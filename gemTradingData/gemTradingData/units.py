import pandas as pd
from gemMarketData.add_columns import *
import pdb

def convert_units(x, to_unit, market_env):
	if to_unit not in ['USD', 'Market']:
		raise Exception('Unknown unit ' + to_unit)

	if 'instrument' not in x.columns:
		raise Exception('Missing instrument column')

	if 'instrument_type' not in x.columns:
		x = x.merge(market_env.instruments[['instrument', 'instrument_type']])

	if 'feed' not in x.columns:
		raise Exception('Missing feed column')
	
	calculation_exp = 1
	if to_unit == 'Market':
		calculation_exp = -1

	#TODO: Get ***unadjusted*** price of feed
	last_futures_date_idx = market_env.feed_data.groupby(['feed'])['date'].transform(max) == market_env.feed_data['date']
	last_futures_prices = market_env.feed_data[last_futures_date_idx][['feed', 'value']]
	last_fx_date_idx = market_env.fx_spot.groupby(['feed'])['date'].transform(max) == market_env.fx_spot['date']
	last_fx_prices = market_env.fx_spot[last_fx_date_idx][['feed', 'value']]
	last_prices = pd.concat([last_futures_prices,last_fx_prices])
	last_prices.rename(columns={'value':'price'}, inplace = True)
	price = x.merge(last_prices)


	x_future = x[x.instrument_type == 'FUTURE_CONTRACT'].merge(market_env.future_contracts[['instrument', 'future']])
	point_value = x_future.merge(market_env.futures[['future', 'point_value']]).drop('future', 1)

	
	fx_rate = add_currency_column(x, market_env)
	fx_rate['power'] = 1
	fx_rate['currency_pair'] = fx_rate['currency'].apply(get_usd_currency_pair, args = (market_env,))
	fx_rate['power'] = fx_rate.apply(lambda row: get_currency_inversion(row['currency'], row['currency_pair']), axis = 1)
	fx_rate = pd.merge(fx_rate, last_prices, how = 'left', left_on = 'currency_pair', right_on = 'feed')
	fx_rate.ix[fx_rate.currency_pair == 'USDUSD','price'] = 1.0
	fx_rate['fx_rate'] = pow(fx_rate['price'], fx_rate['power'])
	fx_conv = x.merge(fx_rate[['instrument', 'fx_rate']])

	##Futures
	x_to_futures = x[x.instrument_type == 'FUTURE_CONTRACT'].merge(price).merge(point_value).merge(fx_conv)
	x_to_futures['position'] = x_to_futures['position'] * pow(x_to_futures['price'].astype('float64') * x_to_futures['point_value'].astype('float64') * x_to_futures['fx_rate'].astype('float64'), calculation_exp)
	x_to_futures = x_to_futures.drop(['price', 'point_value', 'fx_rate'], axis = 1)

	#Fx Forwards
	x_to_fx_forwards = x[x.instrument_type == 'FX_FORWARD'].merge(fx_conv)
	x_to_fx_forwards['position'] = x_to_fx_forwards['position'] * pow(x_to_fx_forwards['fx_rate'].astype('float64'), calculation_exp)
	x_to_fx_forwards = x_to_fx_forwards.drop('fx_rate', axis = 1)

	result = pd.concat([x_to_futures, x_to_fx_forwards])
	result['unit'] = to_unit
	return result