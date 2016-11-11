def apply_gearing(positions, gearings):
		geared_positions = positions.merge(gearings[['account_group', 'trading_model', 'gearing']])
		geared_positions['position'] = geared_positions['position'] * geared_positions['gearing']
		geared_positions = geared_positions.drop('gearing', 1)

		return geared_positions