import json
from joblib import load
import numpy as np
import os

__data_columns = None
__locations = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)

def get_location_names():
    print(f"Getting location names: {__locations}")  # Debug print
    if __locations is None:
        print("Error: __locations is None")
    return __locations

def load_saved():
    print("Loading model and data...")
    global __data_columns
    global __locations
    global __model

    base_path = 'C:/Users/Admin/Desktop/start/model'

    try:
        with open(os.path.join(base_path, 'columns.json'), 'r') as f:
            __data_columns = json.load(f)['data_columns']
            print(f"Columns loaded: {__data_columns}")  # Debug print
            __locations = __data_columns[3:]  # Assuming locations start from index 3
            print(f"Locations loaded: {__locations}")  # Debug print
    except Exception as e:
        print(f"Error loading columns: {e}")

    try:
        __model = load(os.path.join(base_path, 'bengaluru_house_prices_model.joblib'))
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")

    print("Loading complete")

if __name__ == '__main__':
    load_saved()
    print(get_location_names())
    print(get_estimated_price('1st phase jp nagar', 1000, 3, 3))
    print(get_estimated_price('1st phase jp nagar', 1000, 2, 2))
    print(get_estimated_price('1st phase jp nagar', 1000, 1, 1))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
