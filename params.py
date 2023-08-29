"""
control data that are unlikely to change in the short term
e.g. which ticker belongs to which sector, type of scores available
automation script to derive this from Refinitiv data?
wrapper for access I suppose
"""

import pickle

with open('./Dashboard/lib/sectors.pickle', 'rb') as handle:
    sectors = pickle.load(handle)

with open('./Dashboard/lib/tickers_by_sectors.pickle', 'rb') as handle:
    tickers_by_sectors = pickle.load(handle)

with open('./Dashboard/lib/tickers.pickle', 'rb') as handle:
    tickers = pickle.load(handle)

with open('./Dashboard/lib/score_types.pickle', 'rb') as handle:
    score_types = pickle.load(handle)
