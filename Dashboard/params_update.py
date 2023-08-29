"""
Updates pickled data in lib
the pickles are of pandas dataframes
"""

import requests
import pickle
import pandas as pd

API_KEY = 'rf_1nMfaWdyWfpmtWB9dRE'

print('Fetching updates...')

url = f'https://dataapi.marketpsych.com/esg/v4/equcor/assets?apikey={API_KEY}&format=csv'
equcor_assets = pd.read_csv(url)
with open('./lib/equcor_assets.pickle', 'wb') as handle:
    pickle.dump(equcor_assets, handle, protocol=pickle.DEFAULT_PROTOCOL)

url = f'https://dataapi.marketpsych.com/esg/v4/equcor/info?apikey={API_KEY}'
equcor_asset_class = requests.get(url).json()

equcor_datacols = pd.DataFrame.from_records(equcor_asset_class['datacols'])

with open('./lib/equcor_datacols.pickle', 'wb') as handle:
    pickle.dump(equcor_datacols, handle, protocol=pickle.DEFAULT_PROTOCOL)

with open('./lib/equcor_datatypes.pickle', 'wb') as handle:
    pickle.dump(pd.DataFrame.from_records(equcor_asset_class['datatypes']), handle, protocol=pickle.DEFAULT_PROTOCOL)

with open('./lib/equcor_freqs.pickle', 'wb') as handle:
    pickle.dump(pd.DataFrame.from_records(equcor_asset_class['freqs']), handle, protocol=pickle.DEFAULT_PROTOCOL)

url = f'https://dataapi.marketpsych.com/esg/v4/equesg/assets?apikey={API_KEY}&format=csv'
equesg_assets = pd.read_csv(url)
with open('./lib/equesg_assets.pickle', 'wb') as handle:
    pickle.dump(equesg_assets, handle, protocol=pickle.DEFAULT_PROTOCOL)

url = f'https://dataapi.marketpsych.com/esg/v4/equesg/info?apikey={API_KEY}'
equesg_asset_class = requests.get(url).json()

equesg_datacols = pd.DataFrame.from_records(equesg_asset_class['datacols'])
                                            
with open('./lib/equesg_datacols.pickle', 'wb') as handle:
    pickle.dump(equesg_datacols, handle, protocol=pickle.DEFAULT_PROTOCOL)

with open('./lib/equesg_datatypes.pickle', 'wb') as handle:
    pickle.dump(pd.DataFrame.from_records(equesg_asset_class['datatypes']), handle, protocol=pickle.DEFAULT_PROTOCOL)

with open('./lib/equesg_freqs.pickle', 'wb') as handle:
    pickle.dump(pd.DataFrame.from_records(equesg_asset_class['freqs']), handle, protocol=pickle.DEFAULT_PROTOCOL)

print('Updating parameters...')

sectors = sorted(list(equcor_assets['TRBCEconomicSector'].dropna().drop_duplicates()))

with open('./lib/sectors.pickle', 'wb') as handle:
    pickle.dump(sectors, handle, protocol=pickle.DEFAULT_PROTOCOL)

tickers_by_sectors = {}
for sector in sectors:
    tickers_by_sectors[sector] = sorted(list(equcor_assets.loc[equcor_assets['TRBCEconomicSector'] == sector]['Ticker'].dropna().drop_duplicates()))

with open('./lib/tickers_by_sectors.pickle', 'wb') as handle:
    pickle.dump(tickers_by_sectors, handle, protocol=pickle.DEFAULT_PROTOCOL)

tickers = sorted(list(equcor_assets['Ticker'].dropna().drop_duplicates()))

print(tickers)

with open('./lib/tickers.pickle', 'wb') as handle:
    pickle.dump(tickers, handle, protocol=pickle.DEFAULT_PROTOCOL)

score_types = sorted(list(equcor_datacols['name']) + list(equesg_datacols['name']))

with open('./lib/score_types.pickle', 'wb') as handle:
    pickle.dump(score_types, handle, protocol=pickle.DEFAULT_PROTOCOL)

print('Update completed.')
