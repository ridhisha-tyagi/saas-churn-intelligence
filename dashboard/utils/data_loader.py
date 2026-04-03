import os
import pandas as pd

# Base path = dashboard folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_data(filename):
    file_path = os.path.join(BASE_DIR, "data", filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{filename} not found at {file_path}")
    
    return pd.read_csv(file_path)