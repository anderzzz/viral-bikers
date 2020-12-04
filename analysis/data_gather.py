'''Bla bla

'''
import pandas as pd


def gather(blob, chunksize=100000,
           time_key, station_key_suffix,
           date_lower='2018-01-01', date_upper='2019-12-31',
           station_select_frac=0.25):

    gather_collection = []

    for df in pd.read_csv(blob, chunksize=chunksize):
        df[time_key] = pd.to_datetime(df[time_key])
        df = df.loc[(df[time_key] >= date_lower) & (df[time_key] <= date_upper)]

        if len(df) == 0:
            continue

        gather_collection.append(gather_func(df, **gather_kwargs))

    return post_func(gather_collection, **analysis_kwargs)