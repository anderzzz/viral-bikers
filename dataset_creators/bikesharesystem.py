'''Meta data on each bike share system

'''
from dataclasses import dataclass

@dataclass
class BikeShareSystem:
    city_name : str = ''
    country_name : str = ''
    bike_share_name : str = ''
    data_url_source : str = ''
    license : str = ''