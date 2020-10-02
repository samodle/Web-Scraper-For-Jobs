import pandas as pd
import ForkConfig as Fork

def import_city_data():
    raw_city_data = pd.read_csv(Fork.city_data_path)
    only_city_names = raw_city_data[['city', 'state_id']]
    return only_city_names
