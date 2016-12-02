from gemMarketDataCore.market_environment import MarketEnvironment
from gemTradingData.trading_environment import TradingEnvironment
from gemTrading.momentum import Momentum
from gemTrading.orders import *
import pandas as pd
from datetime import date
from datetime import timedelta

market_env = MarketEnvironment.load()
trading_env = TradingEnvironment.load()

mom = Momentum(market_env, trading_env)
mom.update_market_data(market_env)
mom.update_parameters(trading_env)
mom.run()
mom.apply_gearing()

#Read current positions (in lots) from file/DB
current_positions = pd.read_csv('~/python/gemCore/positions.csv')
orders = create_orders(mom.geared_positions, current_positions, trading_env, market_env, orders_date = date.today() - timedelta(days = 1))

#TODO: Order file generator