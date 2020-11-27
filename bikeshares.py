'''Meta data on bike share systems

'''
from dataclasses import dataclass

@dataclass
class BikeShareSystem:
    city_name : str = ''
    country_name : str = ''
    bike_share_name : str = ''
    data_url_source : str = ''
    license : str = ''

taipei = BikeShareSystem(city_name='Taipei', country_name='Taiwan',
                         bike_share_name='YouBike',
                         data_url_source='https://data.taipei/#/dataset/detail?id=9d9de741-c814-450d-b6bb-af8c438f08e5')
helsinki = BikeShareSystem(city_name='Helsinki', country_name='Finland',
                           bike_share_name='City Bike',
                           data_url_source='https://hri.fi/data/en_GB/dataset/helsingin-ja-espoon-kaupunkipyorilla-ajatut-matkat',
                           license='Creative Commons Attribution 4.0')