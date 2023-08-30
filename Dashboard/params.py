"""
control data that are unlikely to change in the short term
e.g. which ticker belongs to which sector, type of scores available
automation script to derive this from Refinitiv data?
wrapper for access I suppose
"""

import pickle

with open('./lib/sectors.pickle', 'rb') as handle:
    sectors = pickle.load(handle)

with open('./lib/tickers_by_sectors.pickle', 'rb') as handle:
    tickers_by_sectors = pickle.load(handle)

with open('./lib/tickers.pickle', 'rb') as handle:
    tickers = pickle.load(handle)

with open('./lib/score_types.pickle', 'rb') as handle:
    score_types = pickle.load(handle)

with open('./lib/core.pickle', 'rb') as handle:
    core = pickle.load(handle)

with open('./lib/advanced.pickle', 'rb') as handle:
    advanced = pickle.load(handle)
