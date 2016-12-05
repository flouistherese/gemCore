import pandas as pd
import pdb
import logging

logger = logging.getLogger('gem_logger')

def add_currency_column(x, market_env):
	if len(x) == 0:
		logger.warning('Currency column cannot be added to empty DataFrame')
		return x

	if 'currency' in x.columns:
		return x

	if 'instrument' not in x.columns:
		raise Exception('Missing instrument column')

	if 'instrument_type' not in x.columns:
		x = x.merge(market_env.instruments[['instrument', 'instrument_type']])

	instrument_currency = pd.DataFrame()

	instrument_types = set(x['instrument_type'].tolist())
	for it in instrument_types:
		if it == 'FUTURE_CONTRACT':
			x_future = x[x.instrument_type == it].merge(market_env.future_contracts[['instrument', 'future']])
			x_future = x_future.merge(market_env.futures[['future', 'currency']])[['instrument', 'currency']]
			instrument_currency = pd.concat([instrument_currency, x_future])
		if it == 'STOCK':
			x_stock = x[x.instrument_type == it].merge(market_env.stocks[['instrument', 'currency']])[['instrument', 'currency']]
			instrument_currency = pd.concat([instrument_currency, x_stock])
		if it == 'FX_FORWARD':
			x_forward = x[x.instrument_type == it].merge(market_env.fx_forwards[['instrument', 'notional_currency']])[['instrument', 'notional_currency']]
			x_forward.rename(columns={'notional_currency':'currency'}, inplace = True)
			instrument_currency = pd.concat([instrument_currency, x_forward])
	return x.merge(instrument_currency)


def get_usd_currency_pair(currency, market_env):
	if currency == 'USD':
		return 'USDUSD'

	currency_pair_row = market_env.currency_pairs[(market_env.currency_pairs['base_currency'] == currency) & (market_env.currency_pairs['quoted_currency'] == 'USD')].reset_index()
	if len(currency_pair_row) > 0:
		return currency_pair_row.loc[0]['currency_pair']
	currency_pair_row = market_env.currency_pairs[(market_env.currency_pairs['quoted_currency'] == currency) & (market_env.currency_pairs['base_currency'] == 'USD')].reset_index()
	if len(currency_pair_row) > 0:
		return currency_pair_row.loc[0]['currency_pair']

	raise Exception('No USD currency pair found for currency ' + currency)

def get_currency_inversion(currency, currency_pair):
	if currency == currency_pair[0:3]:
		return 1
	return -1