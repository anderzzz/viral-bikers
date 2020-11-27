'''Main for bike data covid analysis

'''
import os
from parser import bikerawdata

TPE_FILE_ROOT = './bike_raw_data/taipei'
HEL_FILE_ROOT = './bike_raw_data/helsinki'
TPE_FILES = ['{}/{}'.format(TPE_FILE_ROOT, f) for f in os.listdir(TPE_FILE_ROOT)]
HEL_FILES = ['{}/{}'.format(HEL_FILE_ROOT, f) for f in os.listdir(HEL_FILE_ROOT)]

for df_data in bikerawdata.parse('taipei', TPE_FILES):
    print (df_data)

for df_data in bikerawdata.parse('helsinki', HEL_FILES):
    print (df_data)