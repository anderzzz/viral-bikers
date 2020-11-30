'''Core parser class that defines a common interface to all city raw data sets

Written by: Anders Ohrn 2020

'''
from .bikesharesystem import BikeShareSystem, BikeDataContentDescription

class DataTypeDocumentationError(Exception):
    pass

class BikeRawData(object):
    '''Parser of all city data sets on bike rental events

    '''
    def __init__(self):
        self._parsers = {}
        self._systems = {}

    def keys(self):
        return self._parsers.keys()

    def parse(self, city_label, data_files, kwargs={}):
        '''Parser generator method for data for specified city

        Args:
            city_label : Label of city to obtain data for. For available city labels see `keys` method.
            data_files : Path to folder with raw data files
            kwargs (optional) : Named arguments to pass to the parser function

        Yields:
            df : DataFrame with a batch of data

        '''
        return self._parsers[city_label](data_files, **kwargs)

    def add_parser(self, city_label, parser_func, strict=True):
        '''Add parser method for a specific city

        Args:
            city_label : Label of city to add the parser function for
            parser_func : Callable function that can process a single file of raw data. The function must
                return a DataFrame of data plus a dictionary of data content descriptions, see class documentation
            strict (optional) : If True, performs checks on return data from parser function

        '''

        if not city_label in self._parsers:
            raise RuntimeError('Adding parser for {} must be preceded by adding system for {}'.format(city_label, city_label))

        self._parsers[city_label] = self._raw_file_wrapper(parser_func, strict)

    def add_system(self, city_label, bikesharesystem_data):

        if not isinstance(bikesharesystem_data, BikeShareSystem):
            raise ValueError('The `bikesharesystem_data` argument not an instance of {}'.format(BikeShareSystem))
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


