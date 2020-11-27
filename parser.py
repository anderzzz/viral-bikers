'''Parsers for the different city bike data sets

'''
import pandas as pd

def parse_taipei(data_files):
    '''Parser function for Taipei raw data files

    '''
    for data_file in data_files:
        df_raw = pd.read_csv(data_file,
                             names=['start_rental_dt', 'start_station_name',
                                    'end_rental_dt', 'end_station_name',
                                    'duration', 'date'])

        yield df_raw

def parse_helsiki(data_files):
    '''Parser function for Helsinki raw data files

    '''
    for data_file in data_files:
        df_raw = pd.read_csv(data_file, names=['start_rental_dt', 'end_rental_dt',
                                               'start_station_id', 'start_station_name',
                                               'end_station_id', 'end_station_name',
                                               'distance', 'duration'],
                             header=0)

        yield df_raw

class BikeRawDataParser(object):

    def __init__(self):

        self._parsers = {}

    def keys(self):
        return self._parsers.keys()

    def parse(self, city_label, data_files):

        return self._parsers[city_label](data_files)

    def add_parser(self, city_label, parser_func):

        self._parsers[city_label] = parser_func

bikerawdata = BikeRawDataParser()
bikerawdata.add_parser('taipei', parse_taipei)
bikerawdata.add_parser('helsinki', parse_helsiki)
