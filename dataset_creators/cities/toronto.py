'''Parser and data cleansing for Toronto bike data

Written by: Anders Ohrn 2020

'''
import pandas as pd

from dataset_creators.bikesharesystem import BikeShareSystem, BikeDataContentDescription

RAWDATA_KEYS = ['rental_id', 'duration',
                'start_rental_date_time', 'start_station_name',
                'end_rental_date_time', 'end_station_name',
                'user_type']

toronto_system = BikeShareSystem(city_name='Toronto', country_name='Canada',
                                 bike_share_name='Bike Share Toronto',
                                 data_url_source='https://open.toronto.ca/dataset/bike-share-toronto-ridership-data/',
                                 license='https://open.toronto.ca/open-data-license/')

toronto_data_types = {RAWDATA_KEYS[0] : BikeDataContentDescription(unit='',
                                            content_description='Rental event ID'),
                      RAWDATA_KEYS[1] : BikeDataContentDescription(unit='seconds',
                                            content_description='Duration of travel'),
                      RAWDATA_KEYS[2] : BikeDataContentDescription(unit='YYYY-MM-DD HH:MM:SS',
                                            content_description='Date and time of day rental starts'),
                      RAWDATA_KEYS[3] : BikeDataContentDescription(unit='',
                                            content_description='Name of station at which rental starts'),
                      RAWDATA_KEYS[4] : BikeDataContentDescription(unit='YYYY-MM-DD HH:MM:SS',
                                            content_description='Date and time of day rental ends'),
                      RAWDATA_KEYS[5] : BikeDataContentDescription(unit='',
                                            content_description='Name of station at which rental ends'),
                      RAWDATA_KEYS[6] : BikeDataContentDescription(unit='',
                                            content_description='User type')}

def parse_toronto_file(data_file):
    '''Parser function for Toronto raw data file

    '''
    print (data_file)

    # Raw data files come in many format and content variations
    if '2020' in data_file or '2019' in data_file:
        usecols = [0, 2, 4, 5, 7, 8, 10]
        names = [RAWDATA_KEYS[k] for k in [0, 1, 2, 3, 4, 5, 6]]
    elif '2017 Q3' in data_file or '2017 Q4' in data_file:
        usecols = [0, 1, 2, 3, 4, 5, 6]
        names = [RAWDATA_KEYS[k] for k in [0, 2, 4, 1, 3, 5, 6]]
    elif '2017 Q1'  in data_file or '2017 Q2' in data_file:
        usecols = [0, 1, 2, 3, 5, 7, 8]
        names = [RAWDATA_KEYS[k] for k in [0, 2, 4, 1, 3, 5, 6]]
    elif '2018' in data_file:
        usecols = [0, 1, 3, 4, 5, 7, 8]
        names = [RAWDATA_KEYS[k] for k in [0, 1, 2, 3, 4, 5, 6]]
    else:
        print (pd.read_csv(data_file).columns)
        raise RuntimeError

    df_raw = pd.read_csv(data_file,
                         names=names,
                         usecols=usecols,
                         encoding='utf_8',
                         header=0)

    # One rental event in 2017 is coded as 'NULL', which is entirely removed
    df_raw = df_raw.loc[~df_raw.isnull().any(axis=1)]

    # Convert into Pandas time units, which standardize it to ISO date format. Again a lot of diversity in
    # the format of time in the raw data files
    if '2017 Q2' in data_file or '2017 Q1' in data_file:
        df_raw['start_rental_date_time'] = pd.to_datetime(df_raw['start_rental_date_time'], format='%d/%m/%Y %H:%M')
        df_raw['end_rental_date_time'] = pd.to_datetime(df_raw['end_rental_date_time'], format='%d/%m/%Y %H:%M')

    elif '2017 Q4' in data_file in data_file:
        df_raw['start_rental_date_time'] = pd.to_datetime(df_raw['start_rental_date_time'], format='%m/%d/%y %H:%M:%S')
        df_raw['end_rental_date_time'] = pd.to_datetime(df_raw['end_rental_date_time'], format='%m/%d/%y %H:%M:%S')

    else:
        df_raw['start_rental_date_time'] = pd.to_datetime(df_raw['start_rental_date_time'], format='%m/%d/%Y %H:%M')
        df_raw['end_rental_date_time'] = pd.to_datetime(df_raw['end_rental_date_time'], format='%m/%d/%Y %H:%M')

    return df_raw, toronto_data_types