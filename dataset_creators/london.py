'''Parser and data cleansing for London bike data

'''
import pandas as pd

from .bikesharesystem import BikeShareSystem

london_system = BikeShareSystem(city_name='London', country_name='Great Britain',
                                bike_share_name='Santander Cykles',
                                data_url_source='https://cycling.data.tfl.gov.uk',
                                license='https://tfl.gov.uk/corporate/terms-and-conditions/transport-data-service')

def parse_london_file(data_file):
    '''Parser function for London raw data file

    '''
    df = pd.read_csv(data_file,
                     names=['rental_id', 'duration', 'bike_id', ''],
                     header=0)