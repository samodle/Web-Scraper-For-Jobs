import pandas as pd


def import_city_data():
    raw_city_data = pd.read_csv("CensusData/uscitydata.csv")
    only_city_names = raw_city_data[['city', 'state_id']]
    #  print(only_city_names.head())
    return only_city_names
