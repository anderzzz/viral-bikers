'''Bla bla

'''
import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon, mahalanobis
from scipy import linalg

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
                   how='outer', suffixes=('_start', '_end')).fillna(-1)
    df_['counts'] = df_['counts_start'] + df_['counts_end']
#    df_['station'] = df_[[station_key_s, station_key_e]].max(axis=1)
    df_['station'] = np.where(df_[station_key_s] != -1, df_[station_key_s], df_[station_key_e])
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

def cmp_pdist_station_day_hour(df, station_key):
    '''Bla bla

    '''
    print (df)
    group = df.groupby([station_key, 'year', 'week', 'day', 'hour', 'satsun'])
    df_count = group.mean()
    print (df_count)
    raise RuntimeError

def cmp_cumfreq(df):
    '''Bla bla

    '''
    val_counts = df.value_counts(normalize=True)
    val_counts = val_counts.sort_index()
    max_val = val_counts.index.max()
    new_ind = pd.UInt64Index(range(int(max_val) + 1), name='rental_events')
    val_counts = val_counts.reindex(new_ind, fill_value=0.0)
    val_counts = val_counts.cumsum()

    return val_counts

def cmp_count_range_station_hour(df, station_key):
    '''Bla bla

    '''
    df = cmp_add_zeros(df, station_key).reset_index()
    group = df.groupby([station_key, 'satsun', 'hour'])
    df_stat_q1 = group['counts'].quantile(q=0.25)
    df_stat_q2 = group['counts'].quantile(q=0.50)
    df_stat_q3 = group['counts'].quantile(q=0.75)
    df_stat_q0 = group['counts'].quantile(q=0.05)
    df_stat_q4 = group['counts'].quantile(q=0.95)
    df_stat_mean = group['counts'].mean()

    df = pd.DataFrame.from_dict({'q_25' : df_stat_q1, 'q_75' : df_stat_q3, 'median' : df_stat_q2,
                                 'q_05' : df_stat_q0, 'q_95' : df_stat_q4, 'mean' : df_stat_mean})

    df_x = group['counts'].apply(cmp_cumfreq)

    return df, df_x

def cmp_count_range_station_d(df, station_key):
    '''Bla bla

    '''
    df = cmp_add_zeros(df, station_key).reset_index()
    df1 = df.groupby(['year','week','day','satsun','station']).sum().reset_index()
    group = df1.groupby([station_key, 'satsun'])
    df_stat_q1 = group['counts'].quantile(q=0.25)
    df_stat_q2 = group['counts'].quantile(q=0.50)
    df_stat_q3 = group['counts'].quantile(q=0.75)
    df_stat_q0 = group['counts'].quantile(q=0.05)
    df_stat_q4 = group['counts'].quantile(q=0.95)
    df_stat_mean = group['counts'].mean()

    df = pd.DataFrame.from_dict({'q_25' : df_stat_q1, 'q_75' : df_stat_q3, 'median' : df_stat_q2,
                                 'q_05' : df_stat_q0, 'q_95' : df_stat_q4, 'mean' : df_stat_mean})

    df_x = group['counts'].apply(cmp_cumfreq)
    print (df)
    print (df_x)

    return df, df_x

def cmp_count_cov_station_hour(df, station_key):
    '''Bla bla

    '''
    collections = []
    group = df.groupby([station_key, 'satsun'])
    for key, df_group in group:
        df_c = df_group.pivot(index=[station_key, 'satsun', 'year', 'week', 'day'], columns='hour', values='counts')
        df_c = df_c.fillna(value=0.0)
        df_cov = df_c.cov()
        df_cov_inv = pd.DataFrame(linalg.inv(df_cov))
        df_cov = df_cov.stack()
        df_cov_inv = df_cov_inv.stack()
        index = pd.MultiIndex.from_tuples([(key[0], key[1], x1, x2) for x1, x2 in df_cov.index.tolist()],
                                          names=[station_key, 'satsun', 'hour1', 'hour2'])
        df_1 = pd.DataFrame(df_cov.values, index=index, columns=['covariance'])
        df_2 = pd.DataFrame(df_cov_inv.values, index=index, columns=['covariance_inv'])
        df_ = df_1.join(df_2)
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

def cmp_js_station_station_cities(df, station_key):
    '''Bla bla

    '''
    def _js(df):
        df = df.reset_index()
        df = df.pivot(columns='hour', values='freq', index=[station_key, 'city'])
        df_ = df.T.corr(method=jensenshannon)
        df_.values[[np.arange(df_.shape[0])] * 2] = 0.0
        return df_

    df_1 = df.loc[:, False, :, :]
    df_weekday = _js(df_1)
    df_2 = df.loc[:, True, :, :]
    df_weekend = _js(df_2)

    return df_weekday, df_weekend

def cmp_add_zeros(df, station_key):
    '''Bla bla

    '''
    existing_tups = list(df.groupby(['year', 'week', 'day', 'satsun', station_key]).groups.keys())
    new_index_tups = []
    for tup in existing_tups:
        for hour in range(24):
            tupper = list(tup)
            tupper.append(hour)
            new_index_tups.append(tuple(tupper))
    new_mindex = pd.MultiIndex.from_tuples(new_index_tups, names=['year', 'week', 'day', 'satsun', station_key, 'hour'])

    df = df.set_index(['year', 'week', 'day', 'satsun', station_key, 'hour'])
    df_expand = df.reindex(new_mindex, fill_value=0.0)

    return df_expand

def cmp_deviation(df_2020, df_count_baseline, station_key):
    '''Bla bla

    '''
    def _fit_percentile(s):
        station_ = s.name[4]
        satsun_ = s.name[3]
        station_baseline = df_count_baseline.loc[station_, satsun_]
        if station_baseline.index.max() < s.counts:
            ret = 1.0
        else:
            ret = station_baseline.loc[s.counts]

        return ret

    df_2020 = df_2020.groupby(['year','week','day','satsun','station']).sum()
    df_2020['percentile'] = df_2020.apply(_fit_percentile, axis=1)

    return df_2020[['counts','percentile']].reset_index()
