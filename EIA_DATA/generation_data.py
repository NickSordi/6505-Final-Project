import os
from urllib.request import urlretrieve

import pandas as pd

URL = 'https://www.eia.gov/electricity/data/state/generation_monthly.xlsx'

def get_generation_data(filename='generation_monthly.xlsx', url=URL, force_download=False, sheet_name=None):
    if not os.path.exists('DATA'):
        os.makedirs('DATA')
    
    '''Download and cache the generation data
    
    Parameters
    ----------
    filename : str
        location to save the data
    url : str
        web location of the data
    force_download : bool
        if True, force redownload of data
    sheet_name : bool
        which sheet to download in a list, or None to download all

        
    Returns
    -------
    
data : pandas.DataFrame
    the generation data
    '''

    full_filepath = os.path.join('DATA', filename)

    if force_download or not os.path.exists(full_filepath):
        urlretrieve(url, full_filepath)

    excel_data = pd.read_excel(full_filepath, sheet_name=sheet_name,
                               names=["YEAR", "MONTH", "STATE", "TYPE OF PRODUCER", "ENERGY SOURCE", "GENERATION (Megawatthours)"])

    raw_df = pd.concat(excel_data.values(), keys=excel_data.keys(), ignore_index=True)
    return raw_df

