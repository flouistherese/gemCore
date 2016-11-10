from gemMarketData.market_environment import MarketEnvironment
from gemTradingData.trading_environment import TradingEnvironment
from gemTrading.momentum import Momentum


market_env = MarketEnvironment.load()
trading_env = TradingEnvironment.load()

mom = Momentum(market_env, trading_env)
mom.update_market_data(market_env)
mom.update_parameters(trading_env)
mom.run()