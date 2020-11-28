'''Bla bla

'''
from .taipei import parse_taipei_file
from .helsinki import parse_helsiki_file

from ._parser import BikeRawDataParser

bikerawdata = BikeRawDataParser()
bikerawdata.add_parser(city_label='taipei', parser_func=parse_taipei_file)
bikerawdata.add_parser(city_label='helsinki', parser_func=parse_helsiki_file)