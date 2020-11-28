'''Parser and data cleansing for Taipei bike data

'''
import pandas as pd

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