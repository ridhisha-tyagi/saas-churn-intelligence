import os
import pandas as pd

# Get dashboard folder directly
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_data(filename):
    file_path = os.path.join(BASE_DIR, "data", filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{filename} not found at {file_path}")

    return pd.read_csv(file_path)