'''Core part of parser of raw data

'''
from .bikesharesystem import BikeShareSystem

COL_NAMES = ['start_rental_dt', 'start_station_name', 'start_station_id', 'start_rental_date', 'start_rental_time',
             'end_rental_dt', 'end_station_name', 'end_station_id', 'end_rental_date', 'end_rental_time',
             'duration', 'distance', 'date']

class BikeRawData(object):

    def __init__(self):

        self._parsers = {}
        self._systems = {}

    def keys(self):
        return self._parsers.keys()

    def parse(self, city_label, data_files, kwargs={}):

        return self._parsers[city_label](data_files, **kwargs)

    def add_parser(self, city_label, parser_func, multi_file_wrapper=True, strict=True):

        if not city_label in self._parsers:
            raise RuntimeError('Adding parser for {} must be preceded by adding system for {}'.format(city_label, city_label))

        if multi_file_wrapper:
            self._parsers[city_label] = self._raw_file_wrapper(parser_func, strict)
        else:
            self._parsers[city_label] = parser_func

    def add_system(self, city_label, bikesharesystem_data):

        if not isinstance(bikesharesystem_data, BikeShareSystem):
            raise ValueError('The `bikesharesystem_data` argument not an instance of `BikeShareSystem`')
        self._systems[city_label] = bikesharesystem_data
        self._parsers[city_label] = None

    def _raw_file_wrapper(self, func, strict):

        def wrapper(data_files):
            for data_file in data_files:
                df = func(data_file)
                if strict:
                    self._validate_(df)

                yield df

        return wrapper

    def _validate_(self, df):

        if not set(df.columns.to_list()).issubset(set(COL_NAMES)):
            raise KeyError('The column names after raw data parsing must be subset of `COL_NAMES`')


