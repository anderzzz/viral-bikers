'''Bla bla

'''
from .taipei import parse_taipei_file, taipei_system
from .helsinki import parse_helsiki_file, helsinki_system

from ._bikerawdata import BikeRawData

bikerawdata = BikeRawData()
bikerawdata.add_system(city_label='taipei', bikesharesystem_data=taipei_system)
bikerawdata.add_parser(city_label='taipei', parser_func=parse_taipei_file)
bikerawdata.add_system(city_label='helsinki', bikesharesystem_data=helsinki_system)
bikerawdata.add_parser(city_label='helsinki', parser_func=parse_helsiki_file)

def compile_data(city_labels=None):
    '''Compile all data into common structure

    '''
    pass

def compile_and_save_data(f_out, city_labels=None):
    '''Compile and save all data

    '''
    pass