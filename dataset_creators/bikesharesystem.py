'''Meta data on each bike share system

'''
from dataclasses import dataclass

@dataclass
class BikeShareSystem:
    city_name : str = None
    country_name : str = None
    bike_share_name : str = None
    data_url_source : str = None
    license : str = None

@dataclass
class BikeDataContentDescription:
    unit : str = None
    content_description : str = None

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            raise NotImplemented
        return (self.unit, self.content_description) == \
               (other.unit, other.content_description)

