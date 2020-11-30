'''Parser and data cleansing for Helsinki bike data

Written by: Anders Ohrn 2020

'''
import pandas as pd

from dataset_creators.bikesharesystem import BikeShareSystem, BikeDataContentDescription

RAWDATA_KEYS = ['start_rental_date_time', 'end_rental_date_time',
                'start_station_id', 'start_station_name',
                'end_station_id', 'end_station_name',
                'distance', 'duration']

helsinki_system = BikeShareSystem(city_name='Helsinki', country_name='Finland',
                                  bike_share_name='City Bike',
                                  data_url_source='https://hri.fi/data/en_GB/dataset/helsingin-ja-espoon-kaupunkipyorilla-ajatut-matkat',
                                  license='Creative Commons Attribution 4.0')

helsinki_data_types = {RAWDATA_KEYS[0] : BikeDataContentDescription(unit='YYY-MM-DD HH:MM:SS',
                                             content_description='Date and time of day rental starts'),
                       RAWDATA_KEYS[1] : BikeDataContentDescription(unit='YYYY-MM-DD HH:MM:SS',
                                             content_description='Date and time of day rental ends'),
                       RAWDATA_KEYS[2] : BikeDataContentDescription(unit='',
                                             content_description='Station ID where rental starts'),
                       RAWDATA_KEYS[3] : BikeDataContentDescription(unit='',
                                             content_description='Name of station at which rental starts'),
                       RAWDATA_KEYS[4] : BikeDataContentDescription(unit='',
                                             content_description='Station ID where rental ends'),
                       RAWDATA_KEYS[5] : BikeDataContentDescription(unit='',
                                             content_description='Name of station at which rental ends'),
                       RAWDATA_KEYS[6] : BikeDataContentDescription(unit='meters',
                                             content_description='Distance travelled'),
                       RAWDATA_KEYS[7] : BikeDataContentDescription(unit='seconds',
                                             content_description='Duration of travel')}

def parse_helsiki_file(data_file):
    '''Parser function for Helsinki raw data file

    '''
    df_raw = pd.read_csv(data_file,
                         names=RAWDATA_KEYS,
                         encoding='utf_8',
                         header=0)

    # Convert into Pandas time units
    df_raw['start_rental_date_time'] = pd.to_datetime(df_raw['start_rental_date_time'], format='%Y-%m-%dT%H:%M:%S')
    df_raw['end_rental_date_time'] = pd.to_datetime(df_raw['end_rental_date_time'], format='%Y-%m-%dT%H:%M:%S')

    return df_raw, helsinki_data_types