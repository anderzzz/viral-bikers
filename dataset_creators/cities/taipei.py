'''Parser and data cleansing for Taipei bike data

Written by: Anders Ohrn 2020

'''
import pandas as pd
import io
import pinyin

from dataset_creators.bikesharesystem import BikeShareSystem, BikeDataContentDescription

RAWDATA_KEYS = ['start_rental_date_hour', 'start_station_name_tradchinese',
                'end_rental_date_hour', 'end_station_name_tradchinese',
                'duration', 'start_date']

taipei_system = BikeShareSystem(city_name='Taipei', country_name='Taiwan',
                                bike_share_name='YouBike',
                                data_url_source='https://data.taipei/#/dataset/detail?id=9d9de741-c814-450d-b6bb-af8c438f08e5')

taipei_data_types = {RAWDATA_KEYS[0] : BikeDataContentDescription(unit='YYYY-MM-DD HH:00:00',
                                           content_description='Date and hour bike rental starts'),
                     RAWDATA_KEYS[1] : BikeDataContentDescription(unit='',
                                           content_description='Name of station at which rental starts in traditional Chinese'),
                     RAWDATA_KEYS[2] : BikeDataContentDescription(unit='YYYY-MM-DD HH:00:00',
                                           content_description='Date and hour bike rental ends'),
                     RAWDATA_KEYS[3] : BikeDataContentDescription(unit='',
                                           content_description='Name of station at which rental ends in traditional Chinese'),
                     RAWDATA_KEYS[4] : BikeDataContentDescription(unit='seconds',
                                           content_description='Duration of travel'),
                     RAWDATA_KEYS[5] : BikeDataContentDescription(unit='YYYY-MM-DD',
                                           content_description='Date bike rental starts')}

def parse_taipei_file(data_file):
    '''Parser function for Taipei raw data file

    '''
    print (data_file)
    # A small number of lines (~10) in raw data files are weirdly encoded. They are discarded entirely
    invalid_lines = 0
    valid_lines = []
    with open(data_file, 'r', encoding='utf_8') as fin:
        try:
            for line in fin:
                valid_lines.append(line)

        except UnicodeDecodeError:
            invalid_lines += 1

    df_raw = pd.read_csv(io.StringIO('\n'.join(valid_lines)),
                         names=RAWDATA_KEYS,
                         encoding='utf_8',
                         header=0)

    # In 41 instances in May 2018 the duration is not a time, but Chinese characters saying "number two exit".
    # These are removed. Most likely part of a name misplaced.
    if '201805' in data_file:
        df_raw = df_raw.loc[df_raw['duration'].str.count(':') == 2]

    # Convert into Pandas time units
    df_raw['start_rental_date_hour'] = pd.to_datetime(df_raw['start_rental_date_hour'], format='%Y-%m-%d %H:%M:%S')
    df_raw['end_rental_date_hour'] = pd.to_datetime(df_raw['end_rental_date_hour'], format='%Y-%m-%d %H:%M:%S')
    df_raw['start_date'] = pd.to_datetime(df_raw['start_date'], format='%Y-%m-%d')

    # Duration to seconds only
    df_raw['duration'] = pd.to_timedelta(df_raw['duration'])
    df_raw['duration'] = df_raw['duration'].apply(lambda x: x.total_seconds())
    df_raw['duration'] = df_raw['duration'].astype(str)

    # Prior to pinyin addition, missing entries are converted to empty strings
    df_raw['start_station_name_tradchinese'] = df_raw['start_station_name_tradchinese'].fillna(value='')
    df_raw['end_station_name_tradchinese'] = df_raw['end_station_name_tradchinese'].fillna(value='')

    # Add columns: pinyin variation to station names
    df_raw['start_station_name_pinyin'] = df_raw['start_station_name_tradchinese'].apply(pinyin.get,
                                                                                         **{'format' : 'strip',
                                                                                            'delimiter' : ''})
    taipei_data_types['start_station_name_pinyin'] = BikeDataContentDescription(unit='',
                                                         content_description='Name of station at which rental starts in pinyin')
    df_raw['end_station_name_pinyin'] = df_raw['end_station_name_tradchinese'].apply(pinyin.get,
                                                                                         **{'format' : 'strip',
                                                                                            'delimiter' : ''})
    taipei_data_types['end_station_name_pinyin'] = BikeDataContentDescription(unit='',
                                                       content_description='Name of station at which rental ends in pinyin')

    return df_raw, taipei_data_types