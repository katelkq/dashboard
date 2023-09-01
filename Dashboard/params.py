"""
control data that are unlikely to change in the short term
e.g. which ticker belongs to which sector, type of scores available
automation script to derive this from Refinitiv data?
wrapper for access I suppose
"""

import pickle

with open('./Dashboard/lib/sectors.pickle', 'rb') as handle:
    sectors = pickle.load(handle)

with open('./Dashboard/lib/assets.pickle', 'rb') as handle:
    assets = pickle.load(handle)

with open('./Dashboard/lib/core.pickle', 'rb') as handle:
    core = pickle.load(handle)

with open('./Dashboard/lib/advanced.pickle', 'rb') as handle:
    advanced = pickle.load(handle)

with open('./Dashboard/lib/equcor_datacols.pickle', 'rb') as handle:
    equcor_datacols = pickle.load(handle)

with open('./Dashboard/lib/equesg_datacols.pickle', 'rb') as handle:
    equesg_datacols = pickle.load(handle)

with open('./Dashboard/lib/equcor_assets.pickle', 'rb') as handle:
    equcor_assets = pickle.load(handle)

