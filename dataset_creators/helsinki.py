'''Parser and data cleansing for Helsinki bike data

'''
import pandas as pd

from .bikesharesystem import BikeShareSystem

helsinki_system = BikeShareSystem(city_name='Helsinki', country_name='Finland',
                                  bike_share_name='City Bike',
                                  data_url_source='https://hri.fi/data/en_GB/dataset/helsingin-ja-espoon-kaupunkipyorilla-ajatut-matkat',
                                  license='Creative Commons Attribution 4.0')

def parse_helsiki_file(data_file):
    '''Parser function for Helsinki raw data file

    '''
    df_raw = pd.read_csv(data_file,
                         names=['start_rental_dt', 'end_rental_dt',
                                'start_station_id', 'start_station_name',
                                'end_station_id', 'end_station_name',
                                'distance', 'duration'],
                         header=0)

    return df_raw