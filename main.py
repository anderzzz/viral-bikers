'''Main for bike data covid analysis

'''
import os
from dataset_creators import bikerawdata

TPE_FILE_ROOT = './bike_raw_data/taipei'
HEL_FILE_ROOT = './bike_raw_data/helsinki'
TPE_FILES = ['{}/{}'.format(TPE_FILE_ROOT, f) for f in os.listdir(TPE_FILE_ROOT)]
HEL_FILES = ['{}/{}'.format(HEL_FILE_ROOT, f) for f in os.listdir(HEL_FILE_ROOT)]

for df_data in bikerawdata.parse('taipei', TPE_FILES):
    print (df_data)
    print (df_data['start_rental_dt'].dtype)
    #raise RuntimeError

for df_data in bikerawdata.parse('helsinki', HEL_FILES):
    print (df_data)
    raise RuntimeError