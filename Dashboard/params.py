"""
Wrapper for access to pickled files.

"""

import os
import pickle

match os.getcwd().split('\\')[-1]:
    # enables correct generation of documentation
    case 'docs':
        dir = '../Dashboard'
    case _:
        dir = './Dashboard'

with open(f'{dir}/lib/sectors.pickle', 'rb') as handle:
    sectors = pickle.load(handle)

with open(f'{dir}/lib/assets.pickle', 'rb') as handle:
    assets = pickle.load(handle)

with open(f'{dir}/lib/core.pickle', 'rb') as handle:
    core = pickle.load(handle)

with open(f'{dir}/lib/advanced.pickle', 'rb') as handle:
    advanced = pickle.load(handle)

with open(f'{dir}/lib/equcor_datacols.pickle', 'rb') as handle:
    equcor_datacols = pickle.load(handle)

with open(f'{dir}/lib/equesg_datacols.pickle', 'rb') as handle:
    equesg_datacols = pickle.load(handle)

with open(f'{dir}/lib/equcor_assets.pickle', 'rb') as handle:
    equcor_assets = pickle.load(handle)

