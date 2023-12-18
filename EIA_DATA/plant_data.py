import os
import requests
import zipfile
import io
import pandas as pd

zip_plant_URL = 'https://www.eia.gov/electricity/data/eia860/xls/eia8602022.zip'

def get_plant_data(url = zip_plant_URL, plant_file_name='2___Plant_Y2022.xlsx', generator_file_name='3_1_Generator_Y2022.xlsx'):
    # Download and unzip the data
    extract_to_path = 'LOCAL DATA\Capacity'
    download_and_unzip(url, extract_to_path)

    # Construct file paths for the Excel files
    plant_xlsx_filepath = os.path.join(extract_to_path, plant_file_name)
    generator_xlsx_filepath = os.path.join(extract_to_path, generator_file_name)

    # Read and merge the data
    df1 = read_and_concat_excel(plant_xlsx_filepath, sheet_name=['Plant'], skiprows=1)
    df2 = read_and_concat_excel(generator_xlsx_filepath, sheet_name=['Operable'], skiprows=1)

    #merged_df = pd.merge(df1, df2, on='Utility ID', how='left')

    return df2

def download_and_unzip(url, extract_to_path):
    # Download the zip file from the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the contents of the zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to_path)
        print(f"Successfully downloaded and unzipped {url}")
    else:
        print(f"Failed to download the file from {url}. Status code: {response.status_code}")

def read_and_concat_excel(filepath, **kwargs):
    # Read Excel file and concatenate sheets
    df = pd.concat(pd.read_excel(filepath, **kwargs).values(), keys=pd.read_excel(filepath, **kwargs).keys(), ignore_index=True)
    return df
