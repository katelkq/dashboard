"""
Update the stored pickles.

"""

from api import API_KEY
import os
import pandas as pd
import pickle
import requests
from varname import nameof

match os.getcwd().split('\\')[-1]:
    # enables correct generation of documentation
    case 'docs':
        dir = '../Dashboard'
    case _:
        dir = './Dashboard'

def make_pickles(var, var_name):
    """
    Make a pickle out of the item passed in and store it under :code:`./Dashboard/lib/` with the same name.

    """

    print(f'Pickled {var_name}.')
    with open(f'{dir}/lib/{var_name}.pickle', 'wb') as handle:
        pickle.dump(var, handle, protocol=pickle.DEFAULT_PROTOCOL)
    pass

# start of script
print('Making queries...')

url = f'https://dataapi.marketpsych.com/esg/v4/equcor/assets?apikey={API_KEY}&format=csv'
equcor_assets = pd.read_csv(url)
make_pickles(equcor_assets, nameof(equcor_assets))

url = f'https://dataapi.marketpsych.com/esg/v4/equesg/assets?apikey={API_KEY}&format=csv'
equesg_assets = pd.read_csv(url)
make_pickles(equesg_assets, nameof(equesg_assets))

url = f'https://dataapi.marketpsych.com/esg/v4/equcor/info?apikey={API_KEY}'
equcor_asset_class = requests.get(url).json()

url = f'https://dataapi.marketpsych.com/esg/v4/equesg/info?apikey={API_KEY}'
equesg_asset_class = requests.get(url).json()

print('Updating parameters...')

# data columns offered by Core
equcor_datacols = pd.DataFrame.from_records(equcor_asset_class['datacols'])
make_pickles(equcor_datacols, nameof(equcor_datacols))

equcor_datatypes = pd.DataFrame.from_records(equcor_asset_class['datatypes'])
make_pickles(equcor_datatypes, nameof(equcor_datatypes))

equcor_freqs = pd.DataFrame.from_records(equcor_asset_class['freqs'])
make_pickles(equcor_freqs, nameof(equcor_freqs))

# data columns offered by Advanced
equesg_datacols = pd.DataFrame.from_records(equesg_asset_class['datacols'])
make_pickles(equesg_datacols, nameof(equesg_datacols))

equesg_datatypes = pd.DataFrame.from_records(equesg_asset_class['datatypes'])
make_pickles(equesg_datatypes, nameof(equesg_datatypes))

equesg_freqs = pd.DataFrame.from_records(equesg_asset_class['freqs'])
make_pickles(equesg_freqs, nameof(equesg_freqs))

sectors = sorted(list(equcor_assets['TRBCEconomicSector'].dropna().drop_duplicates()))
make_pickles(sectors, nameof(sectors))

assets = sorted(list(equcor_assets['name'].dropna().drop_duplicates()))
make_pickles(assets, nameof(assets))

# data columns offered by Core, as a sorted list of strings
core = sorted(list(equcor_datacols['name']))
make_pickles(core, nameof(core))

# data columns offered by Advanced, as a sorted list of strings
advanced = sorted(list(equesg_datacols['name']))
make_pickles(advanced, nameof(advanced))

print('Update completed.')
