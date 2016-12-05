from gemUtils.utils import *
from gemMarketDataCore.market_environment import MarketEnvironment
from gemTradingData.trading_environment import TradingEnvironment
from gemTrading.momentum import Momentum
from gemTrading.orders import *

import pandas as pd
from datetime import date, timedelta

logger = create_logger(file_path = 'logfile.log')

logger.info('Loading market environment')
market_env = MarketEnvironment.load()
logger.info('Loading trading environment')
trading_env = TradingEnvironment.load()

logger.info('Initializing Momentum strategy')
mom = Momentum(market_env, trading_env)
logger.info('Updating Momentum market data')
mom.update_market_data(market_env)
logger.info('Updating Momentum parameters')
mom.update_parameters(trading_env)
logger.info('Running Momentum strategy')
mom.run()
logger.info('Applying gearing to Momentum raw positions')
mom.apply_gearing()

#Read current positions (in lots) from file/DB
current_positions = pd.read_csv('~/python/gemCore/positions.csv')
logger.info('Calculating orders')
orders = create_orders(mom.geared_positions, current_positions, trading_env, market_env, orders_date = date.today() - timedelta(days = 3))

#TODO: Order file generator