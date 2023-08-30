"""
Updates pickled data in lib
the pickles are of pandas dataframes
"""

import requests
import pickle
import pandas as pd
from varname import nameof

API_KEY = 'rf_1nMfaWdyWfpmtWB9dRE'

def make_pickles(var, var_name):
    """
    Makes a pickle out of the item passed in
    Stores it under ./lib/
    """
    print(f'Pickled {var_name}.')
    with open(f'./lib/{var_name}.pickle', 'wb') as handle:
        pickle.dump(var, handle, protocol=pickle.DEFAULT_PROTOCOL)
    pass

# start of script
print('Updating parameters...')

url = f'https://dataapi.marketpsych.com/esg/v4/equcor/assets?apikey={API_KEY}&format=csv'
equcor_assets = pd.read_csv(url)
make_pickles(equcor_assets, nameof(equcor_assets))

url = f'https://dataapi.marketpsych.com/esg/v4/equcor/info?apikey={API_KEY}'
equcor_asset_class = requests.get(url).json()

equcor_datacols = pd.DataFrame.from_records(equcor_asset_class['datacols'])
make_pickles(equcor_datacols, nameof(equcor_datacols))

equcor_datatypes = pd.DataFrame.from_records(equcor_asset_class['datatypes'])
make_pickles(equcor_datatypes, nameof(equcor_datatypes))

equcor_freqs = pd.DataFrame.from_records(equcor_asset_class['freqs'])
make_pickles(equcor_freqs, nameof(equcor_freqs))

url = f'https://dataapi.marketpsych.com/esg/v4/equesg/assets?apikey={API_KEY}&format=csv'
equesg_assets = pd.read_csv(url)
make_pickles(equesg_assets, nameof(equesg_assets))

url = f'https://dataapi.marketpsych.com/esg/v4/equesg/info?apikey={API_KEY}'
equesg_asset_class = requests.get(url).json()

equesg_datacols = pd.DataFrame.from_records(equesg_asset_class['datacols'])
make_pickles(equesg_datacols, nameof(equesg_datacols))

equesg_datatypes = pd.DataFrame.from_records(equesg_asset_class['datatypes'])
make_pickles(equesg_datatypes, nameof(equesg_datatypes))

equesg_freqs = pd.DataFrame.from_records(equesg_asset_class['freqs'])
make_pickles(equesg_freqs, nameof(equesg_freqs))

sectors = sorted(list(equcor_assets['TRBCEconomicSector'].dropna().drop_duplicates()))
make_pickles(sectors, nameof(sectors))

tickers_by_sectors = {}
for sector in sectors:
    tickers_by_sectors[sector] = sorted(list(equcor_assets.loc[equcor_assets['TRBCEconomicSector'] == sector]['Ticker'].dropna().drop_duplicates()))
make_pickles(tickers_by_sectors, nameof(tickers_by_sectors))

tickers = sorted(list(equcor_assets['Ticker'].dropna().drop_duplicates()))
make_pickles(tickers, nameof(tickers))

score_types = sorted(list(pd.concat([equcor_datacols['name'], equesg_datacols['name']]).drop_duplicates()))

core = set(equcor_datacols['name'])
advanced = set(equesg_datacols['name'])

make_pickles(score_types, nameof(score_types))
make_pickles(core, nameof(core))
make_pickles(advanced, nameof(advanced))

print('Update completed.')
