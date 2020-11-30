'''Parser and data cleansing for Taipei bike data

'''
import pandas as pd
import io
import pinyin

from .bikesharesystem import BikeShareSystem, BikeDataContentDescription

taipei_system = BikeShareSystem(city_name='Taipei', country_name='Taiwan',
                                bike_share_name='YouBike',
                                data_url_source='https://data.taipei/#/dataset/detail?id=9d9de741-c814-450d-b6bb-af8c438f08e5')

RAWDATA_KEYS = ['start_rental_date_hour', 'start_station_name_tradchinese',
                'end_rental_date_hour', 'end_station_name_tradchinese',
                'duration', 'start_date']

taipei_data_types = {RAWDATA_KEYS[0] : BikeDataContentDescription(unit='YYYY-MM-DD HH:00:00',
                                           content_description='Date and hour bike rental starts'),
                     RAWDATA_KEYS[1] : BikeDataContentDescription(unit=None,
                                           content_description='Name of station at which rental starts in traditional Chinese'),
                     RAWDATA_KEYS[2] : BikeDataContentDescription(unit='YYYY-MM-DD HH:00:00',
                                           content_description='Date and hour bike rental ends'),
                     RAWDATA_KEYS[3] : BikeDataContentDescription(unit=None,
                                           content_description='Name of station at which rental ends in traditional Chinese'),
                     RAWDATA_KEYS[4] : BikeDataContentDescription(unit='HH:MM:SS',
                                           content_description='Duration of rental event, seconds resolution'),
                     RAWDATA_KEYS[5] : BikeDataContentDescription(unit='YYYY-MM-DD',
                                           content_description='Date bike rental starts')}

def parse_taipei_file(data_file):
    '''Parser function for Taipei raw data file

    '''

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

    # Convert into Pandas time units
    df_raw['start_rental_date_hour'] = pd.to_datetime(df_raw['start_rental_date_hour'])
    df_raw['end_rental_date_hour'] = pd.to_datetime(df_raw['end_rental_date_hour'])
    df_raw['start_date'] = pd.to_datetime(df_raw['start_date'])
    df_raw['duration'] = pd.to_timedelta(df_raw['duration'])

    # Add columns: pinyin variation to station names
    df_raw['start_station_name_pinyin'] = df_raw['start_station_name_tradchinese'].apply(pinyin.get,
                                                                                         **{'format' : 'strip',
                                                                                            'delimiter' : ''})
    taipei_data_types['start_station_name_pinyin'] = BikeDataContentDescription(unit=None,
                                                         content_description='Name of station at which rental starts in pinyin')
    df_raw['end_station_name_pinyin'] = df_raw['end_station_name_tradchinese'].apply(pinyin.get,
                                                                                         **{'format' : 'strip',
                                                                                            'delimiter' : ''})
    taipei_data_types['end_station_name_pinyin'] = BikeDataContentDescription(unit=None,
                                                       content_description='Name of station at which rental ends in pinyin')

    return df_raw, taipei_data_types