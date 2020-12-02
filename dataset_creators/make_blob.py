'''Create big blob of data

'''
import os
import pandas as pd

from dataset_creators import bikerawdata

TPE_FILE_ROOT = '../bike_raw_data/taipei'
HEL_FILE_ROOT = '../bike_raw_data/helsinki'
LON_FILE_ROOT = '../bike_raw_data/london'
TOR_FILE_ROOT = '../bike_raw_data/toronto'
TPE_FILES = ['{}/{}'.format(TPE_FILE_ROOT, f) for f in os.listdir(TPE_FILE_ROOT)]
HEL_FILES = ['{}/{}'.format(HEL_FILE_ROOT, f) for f in os.listdir(HEL_FILE_ROOT)]
LON_FILES = ['{}/{}'.format(LON_FILE_ROOT, f) for f in os.listdir(LON_FILE_ROOT)]
TOR_FILES = ['{}/{}'.format(TOR_FILE_ROOT, f) for f in os.listdir(TOR_FILE_ROOT)]
TPE_BLOB = '../data_blob/taipei_bikeshare.csv'
HEL_BLOB = '../data_blob/helsinki_bikeshare.csv'
LON_BLOB = '../data_blob/london_bikeshare.csv'
TOR_BLOB = '../data_blob/toronto_bikeshare.csv'

def make_blob_by_city():
    for df in bikerawdata.parse('taipei', TPE_FILES):
        df.to_csv(TPE_BLOB, mode='a', header=not os.path.exists(TPE_BLOB), index=False)
    for df in bikerawdata.parse('helsinki', HEL_FILES):
        df.to_csv(HEL_BLOB, mode='a', header=not os.path.exists(HEL_BLOB), index=False)
    for df in bikerawdata.parse('london', LON_FILES):
        df.to_csv(LON_BLOB, mode='a', header=not os.path.exists(LON_BLOB), index=False)
    for df in bikerawdata.parse('toronto', TOR_FILES):
        df.to_csv(TOR_BLOB, mode='a', header=not os.path.exists(TOR_BLOB), index=False)

if __name__ == '__main__':
    make_blob_by_city()
