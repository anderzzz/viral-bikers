'''Data model for the bike transport data

'''
from datetime import datetime
from dataclasses import dataclass

@dataclass
class BikeRide:
    start_station_id : int
    end_station_id : int
    rent_begin_date : datetime.date
    rent_end_data : datetime.date
    rent_begin_tod : datetime.time
    rent_end_tod : datetime.time