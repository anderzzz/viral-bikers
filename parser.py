'''Parsers for the different city bike data sets

'''
import pandas as pd

from _parser import BikeRawDataParser

def parse_taipei_file(data_file):
    '''Parser function for Taipei raw data file

    '''
    df_raw = pd.read_csv(data_file,
                         names=['start_rental_dt', 'start_station_name',
                                'end_rental_dt', 'end_station_name',
                                'duration', 'date'])

    df_raw['start_rental_dt'] = pd.to_datetime(df_raw['start_rental_dt'])
    df_raw['end_rental_dt'] = pd.to_datetime(df_raw['end_rental_dt'])
    df_raw['date'] = pd.to_datetime(df_raw['date'])
    df_raw['duration'] = pd.to_timedelta(df_raw['duration'])

    return df_raw

def parse_helsiki_file(data_file):
    '''Parser function for Helsinki raw data file

    '''
    df_raw = pd.read_csv(data_file, names=['start_rental_dt', 'end_rental_dt',
                                           'start_station_id', 'start_station_name',
                                           'end_station_id', 'end_station_name',
                                           'distance', 'duration'],
                         header=0)

    return df_raw

bikerawdata = BikeRawDataParser()
bikerawdata.add_parser('taipei', parse_taipei_file)
bikerawdata.add_parser('helsinki', parse_helsiki_file)
