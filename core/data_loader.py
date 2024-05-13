import pandas as pd 
import os 

def load(filename: str) -> pd.DataFrame:
    # Get the directory of the current file (__file__ is the path to data_loader.py)
    current_dir = os.path.dirname(__file__)
    
    # Construct the absolute path to the data directory
    data_dir = os.path.join(current_dir, 'data')
    
    # Construct the absolute path to the file
    file_path = os.path.join(data_dir, filename)
    
    # Load and return the DataFrame
    return pd.read_csv(file_path)