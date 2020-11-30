'''Core part of parser of raw data

'''
from .bikesharesystem import BikeShareSystem, BikeDataContentDescription

class DataTypeDocumentationError(Exception):
    pass

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
                df, df_units = func(data_file)
                if strict:
                    self._validate_(df, df_units)

                yield df

        return wrapper

    def _validate_(self, df, df_units):

        if not set(df.columns) <= set(df_units.keys()):
            raise DataTypeDocumentationError('The DataFrame contains columns without data type documentation')

        if not set(df_units.keys()) <= set(df.columns):
            raise DataTypeDocumentationError('The data type documentation contains entries for columns absent from the DataFrame')

        for key, item in df_units.items():
            if not isinstance(item, BikeDataContentDescription):
                raise TypeError('Entry {} in data type documentation not of type {}'.format(key, BikeDataContentDescription))


