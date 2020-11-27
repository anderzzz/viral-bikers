'''Meta data on bike share systems

'''
from dataclasses import dataclass

@dataclass
class BikeShareSystem:
    city_name : str
    country_name : str
    bike_share_name : str

taipei = BikeShareSystem(city_name='Taipei', country_name='Taiwan',
                         bike_share_name='YouBike')
helsinki = BikeShareSystem(city_name='Helsinki', country_name='Finland',
                           bike_share_name='City Bike')