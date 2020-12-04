'''Bla bla

'''
import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon
from sklearn.cluster import AgglomerativeClustering
import seaborn as sns

def gather_root(blob, chunksize=100000,
                filter_func=None, **filter_func_kwargs):

    collection = []
    for df in pd.read_csv(blob, chunksize=chunksize):

        if not filter_func is None:
            df = filter_func(df, **filter_func_kwargs)

        if len(df) == 0:
            continue

        collection.append(df)

    return pd.concat(collection, ignore_index=True)

def filter_date_range(df, lower, upper, time_key):
    '''Filter on date range

    '''
    df[time_key] = pd.to_datetime(df[time_key])
    df = df.loc[(df[time_key] >= lower) & (df[time_key] <= upper)]
    return df

def cmp_counts_hour_resolve(df, station_key, time_key):
    '''Bla bla

    '''
    df[time_key] = pd.to_datetime(df[time_key])
    df['year'] = df[time_key].dt.year
    df['week'] = df[time_key].dt.isocalendar().week
    df['day'] = df[time_key].dt.isocalendar().day
    df['hour'] = df[time_key].dt.hour

    df['weekday'] = df[time_key].dt.dayofweek
    df['satsun'] = df['weekday'].map({0:False, 1:False, 2:False, 3:False, 4:False, 5:True, 6:True})
    df = df.drop(columns='weekday')

    group = df.groupby(by=[station_key, 'year', 'week', 'day', 'satsun', 'hour'])
    df_count = group.count().iloc[:, 0].rename('counts')
    df_count = df_count.reset_index()

    return df_count

def cmp_total_counts(df_s, df_e, station_key_s, station_key_e):
    '''Bla bla

    '''
    df_ = pd.merge(df_s, df_e,
                   left_on=[station_key_s, 'year', 'week', 'day', 'satsun', 'hour'],
                   right_on=[station_key_e, 'year', 'week', 'day', 'satsun', 'hour'],
                   how='outer', suffixes=('_start', '_end')).fillna(0.0)
    df_['counts'] = df_['counts_start'] + df_['counts_end']
    df_['station'] = df_[[station_key_s, station_key_e]].max(axis=1)
    df_ = df_.drop(columns=['counts_start', 'counts_end', station_key_s, station_key_e])

    return df_

def cmp_stations_most_traffic(df, q, station_key):
    '''Bla bla

    '''
    df = df.groupby(station_key).sum()
    n_top = int(df.shape[0] * q)
    df_ret = df.nlargest(n=n_top, columns='counts')

    return df_ret.index

def cmp_pdist_station_hour(df, station_key):
    '''Bla bla

    '''
    df = df.groupby([station_key, 'satsun', 'hour'])['counts'].sum()
    df_denom = df.groupby([station_key, 'satsun']).sum()
    df_denom = df_denom.reindex(df.index)
    df_freq = df.div(df_denom)
    df_freq = pd.DataFrame(df_freq)
    df_freq = df_freq.rename(columns={'counts' : 'freq'})

    return df_freq

def cmp_count_range_station_hour(df, station_key):
    '''Bla bla

    '''
    group = df.groupby([station_key, 'satsun', 'hour'])
    df_stat_q1 = group['counts'].quantile(q=0.25)
    df_stat_q2 = group['counts'].quantile(q=0.50)
    df_stat_q3 = group['counts'].quantile(q=0.75)
    df_stat_q0 = group['counts'].quantile(q=0.05)
    df_stat_q4 = group['counts'].quantile(q=0.95)

    df = pd.DataFrame.from_dict({'q_25' : df_stat_q1, 'q_75' : df_stat_q3, 'median' : df_stat_q2,
                                 'q_05' : df_stat_q0, 'q_95' : df_stat_q4})

    return df

def cmp_count_cov_station_hour(df, station_key):
    '''Bla bla

    '''
    collections = []
    group = df.groupby([station_key, 'satsun'])
    for key, df_group in group:
        df_c = df_group.pivot(index=[station_key, 'satsun', 'year', 'week', 'day'], columns='hour', values='counts')
        df_c = df_c.fillna(value=0.0)
        df_cov = df_c.cov()
        df_cov = df_cov.stack()
        index = pd.MultiIndex.from_tuples([(key[0], key[1], x1, x2) for x1, x2 in df_cov.index.tolist()],
                                          names=[station_key, 'satsun', 'hour1', 'hour2'])
        df_ = pd.DataFrame(df_cov.values, index=index, columns=['covariance'])
        collections.append(df_)

    return pd.concat(collections)

def cmp_total_per_x(df, time_label):
    '''Bla bla

    '''
    df = df.groupby(['year', time_label]).sum()
    df = df.groupby(time_label).mean()

    return df.loc[:, ['counts']]

def cmp_js_station_station(df, station_key):
    '''Bla bla

    '''
    def _js(df):
        df = df.reset_index()
        df = df.pivot(columns='hour', values='freq', index=station_key)
        df_ = df.T.corr(method=jensenshannon)
        df_.values[[np.arange(df_.shape[0])] * 2] = 0.0
        return df_

    df_1 = df.loc[:, False, :]
    df_weekday = _js(df_1)
    df_2 = df.loc[:, True, :]
    df_weekend = _js(df_2)

    return df_weekday, df_weekend
