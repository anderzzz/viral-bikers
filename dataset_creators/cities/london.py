'''Parser and data cleansing for London bike data

Written by: Anders Ohrn 2020

'''
import pandas as pd

from dataset_creators.bikesharesystem import BikeShareSystem, BikeDataContentDescription

RAWDATA_KEYS = ['rental_id', 'duration', 'bike_id',
                'end_rental_date_time', 'end_station_id', 'end_station_name',
                'start_rental_date_time', 'start_station_id', 'start_station_name']

london_system = BikeShareSystem(city_name='London', country_name='Great Britain',
                                bike_share_name='Santander Cykles',
                                data_url_source='https://cycling.data.tfl.gov.uk',
                                license='https://tfl.gov.uk/corporate/terms-and-conditions/transport-data-service')

london_data_types = {RAWDATA_KEYS[6] : BikeDataContentDescription(unit='YYY-MM-DD HH:MM:SS',
                                           content_description='Date and time of day rental starts'),
                     RAWDATA_KEYS[3] : BikeDataContentDescription(unit='YYYY-MM-DD HH:MM:SS',
                                           content_description='Date and time of day rental ends'),
                     RAWDATA_KEYS[7] : BikeDataContentDescription(unit='',
                                           content_description='Station ID where rental starts'),
                     RAWDATA_KEYS[8] : BikeDataContentDescription(unit='',
                                           content_description='Name of station at which rental starts'),
                     RAWDATA_KEYS[4] : BikeDataContentDescription(unit='',
                                           content_description='Station ID where rental ends'),
                     RAWDATA_KEYS[5] : BikeDataContentDescription(unit='',
                                           content_description='Name of station at which rental ends'),
                     RAWDATA_KEYS[1] : BikeDataContentDescription(unit='seconds',
                                           content_description='Duration of travel'),
                     RAWDATA_KEYS[0] : BikeDataContentDescription(unit='',
                                           content_description='Rental event ID'),
                     RAWDATA_KEYS[2] : BikeDataContentDescription(unit='',
                                           content_description='Rental bike ID')}

def parse_london_file(data_file):
    '''Parser function for London raw data file

    '''
    print (data_file)
    df_raw = pd.read_csv(data_file,
                         names=RAWDATA_KEYS,
                         encoding='utf_8',
                         header=0)

    # Convert into Pandas time units
    df_raw['start_rental_date_time'] = pd.to_datetime(df_raw['start_rental_date_time'])
    df_raw['end_rental_date_time'] = pd.to_datetime(df_raw['end_rental_date_time'])
    df_raw['duration'] = pd.to_timedelta(df_raw['duration'], unit='s')

    return df_raw, london_data_types
