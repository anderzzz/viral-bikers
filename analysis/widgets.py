'''Various analysis widgets

'''
import pandas as pd
import numpy as np
from sklearn import manifold
from scipy.spatial.distance import jensenshannon

def total_rental_by_date(rental_counts):
    df_counts_per_day = pd.DataFrame(pd.concat(rental_counts)).reset_index()
    df_counts_per_day = df_counts_per_day.rename(columns={'index' : 'date', 'start_date' : 'counts'})
    df_counts_per_day = df_counts_per_day.groupby('date').sum().reset_index()
    df_counts_per_day['day_of_week'] = df_counts_per_day['date'].dt.dayofweek
    df_counts_per_day['date'] = pd.to_datetime(df_counts_per_day['date'])

    x1 = df_counts_per_day.loc[df_counts_per_day['date'] <= '2019-07-28'].reset_index()
    x2 = df_counts_per_day.loc[(df_counts_per_day['date'] <= '2020-07-26') & (df_counts_per_day['date'] >= '2020-01-06')].reset_index()
    df_collate = pd.DataFrame({'2019' : x1['counts'], '2020' : x2['counts']}).reset_index()

def cmp_boxplot(group):
    print (group)
    print (group.name)
    df_stat_q1 = group.quantile(q=0.25)
    df_stat_q2 = group.quantile(q=0.50)
    df_stat_q3 = group.quantile(q=0.75)
    df_iqr = df_stat_q3 - df_stat_q1
    upper = df_stat_q3 + 1.5 * df_iqr
    lower = df_stat_q1 - 1.5 * df_iqr

    print (upper)
    raise RuntimeError

    def outliers(group):
        cat = group.name
        return group[(group.score > upper.loc[cat]['score']) | (group.score < lower.loc[cat]['score'])]['score']

    out = group.apply(outliers).dropna()

    # prepare outlier data for plotting, we need coordinates for every outlier.
    if not out.empty:
        outx = []
        outy = []
        for keys in out.index:
            outx.append(keys[0])
            outy.append(out.loc[keys[0]].loc[keys[1]])

class StandardAnalyze(object):

    def __init__(self, chunksize=100000, time_key=None, station_key=None, blob=None,
                 station_select_by_frac=None, station_select_individual=None,
                 time_select_lower=None, time_select_upper=None):

        self.chunksize = chunksize
        self.time_key = time_key
        self.station_key = station_key
        self.blob = blob
        self.station_select_by_frac = station_select_by_frac
        self.station_select_individual = station_select_individual

        gather_collection = []
        for df in pd.read_csv(self.blob, chunksize=self.chunksize):

            df[self.time_key] = pd.to_datetime(self.time_key)
            df = df.loc[(df[self.time_key] >= time_select_lower) & (df[self.time_key] <= time_select_lower)]

            df[self.station_key] =

        self.widget = {'station_types' : {'gather_func' : self._gather_station_weekday_hour,
                                          'post_func' : self._post_station_types},
                       'totals_per_x' : {'gather_func' : self._gather_totals_per_x,
                                         'post_func' : self._post_totals_per_x},
                       'station_to_station' : {'gather_func' : self._gather_station_time_hourres,
                                               'post_func' : self._post_station_time_hourres},
                       'prob_dist_station' : {'gather_func' : self._gather_station_weekday_hour,
                                              'post_func' : self._post_prob_dist},
                       'prob_dist_cluster' : {'gather_func' : self._gather_station_weekday_hour,
                                              'post_func' : self._post_prob_dist_cluster},
                       'prob_dist_deviate' : {'gather_func' : self._gather_station_weekday_hour,
                                              'post_func' : self._post_dist_from_norm},
                       'special_station' : {'gather_func' : self._gather_station_time_hourres,
                                            'post_func' : self._post_special_station}
                       }

    def analyze(self, analysis_key, date_lower='2018-01-01', date_upper='2019-12-31',
                gather_kwargs={}, analysis_kwargs={}):

        gather_collection = []

        gather_func = self.widget[analysis_key]['gather_func']
        post_func = self.widget[analysis_key]['post_func']
        for df in pd.read_csv(self.blob, chunksize=self.chunksize):

            df[self.time_key] = pd.to_datetime(df[self.time_key])
            df = df.loc[(df[self.time_key] >= date_lower) & (df[self.time_key] <= date_upper)]



            if len(df) == 0:
                continue

            gather_collection.append(gather_func(df, **gather_kwargs))

        return post_func(gather_collection, **analysis_kwargs)

    def _gather_station_time_hourres(self, df):
        '''Bla bla

        '''
        df['year'] = df[self.time_key].dt.year
        df['week'] = df[self.time_key].dt.isocalendar().week
        df['day'] = df[self.time_key].dt.isocalendar().day
        df['hour'] = df[self.time_key].dt.hour

        group = df.groupby(by=[self.station_key, 'year', 'week', 'day', 'hour'])
        df_count = group.count().iloc[:, 0].rename("counts")
        df_count = df_count.reset_index()

        return df_count

    def _post_special_station(self, collection, station_keys):
        '''Bla bla

        '''
        df = pd.concat(collection, ignore_index=True)
        df = df.groupby([self.station_key, 'year', 'week', 'day', 'hour']).sum().reset_index()
        df = df.loc[df[self.station_key].isin(station_keys)]

        return df

    def _post_station_time_hourres(self, collection, frac_top=0.25):
        '''Bla bla

        '''
        df = pd.concat(collection, ignore_index=True)
        df = df.groupby([self.station_key, 'year', 'week', 'day', 'hour']).sum().reset_index()

        xx = df.groupby(self.station_key).count()
        n_top = int(xx.shape[0] * frac_top)
        df_top_stations = xx.nlargest(n=n_top, columns='counts').reset_index()

        df_subset = df.loc[df[self.station_key].isin(df_top_stations[self.station_key])]
        print (df_subset)
        df_subset.to_csv('tmp.csv')
        df_pivot = df_subset.pivot(columns=self.station_key, values='counts', index=['year','week','day','hour'])
        df_pivot = df_pivot.fillna(0.0)
        df_corr = df_pivot.corr()

        tsne_coords = manifold.TSNE(n_components=2, metric='precomputed').fit_transform(df_corr)

        return tsne_coords

    def _post_dist_from_norm(self, collection, frac_top=0.25, weekend_split=True):
        '''Bla bla

        '''
        df = pd.concat(collection, ignore_index=True)
        print (df)
        df.to_csv('tmp.csv')
        df = df.loc[df[self.station_key] == '?公公園']
        if weekend_split:
            group = df.groupby(['satsun', 'hour'])
            g_mean = group.mean()
            g_q1 = group.quantile(q=0.25)
            g_q2 = group.quantil(q=0.5)
            g_q3 = group.quantile(q=0.75)


            cmp_boxplot(group)

    def _post_prob_dist(self, collection, frac_top=0.25, weekend_split=True):
        '''Bla bla

        '''
        df = pd.concat(collection, ignore_index=True)
        if weekend_split:
            df = df.groupby([self.station_key, 'satsun', 'hour']).sum()
            df_denom = df.groupby([self.station_key, 'satsun']).sum()
            df_denom = df_denom.reindex(df.index)
            df_freq = df.div(df_denom)
        else:
            df = df.groupby([self.station_key, 'hour']).sum()
            df_denom = df.groupby([self.station_key]).sum()
            df_denom = df_denom.reindex(df.index)
            df_freq = df.div(df_denom)
        df_freq = df_freq.reset_index()

        xx = df.groupby(self.station_key).sum()
        n_top = int(xx.shape[0] * frac_top)
        df_top_stations = xx.nlargest(n=n_top, columns='counts').reset_index()

        df_subset = df_freq.loc[df_freq[self.station_key].isin(df_top_stations[self.station_key])]

        return df_subset

    def _post_prob_dist_cluster(self, collection, frac_top=0.05, weekend_split=True):
        '''Bla bla

        '''
        df_probs = self._post_prob_dist(collection, frac_top=frac_top, weekend_split=weekend_split)
        df_probs.to_csv('tmp.csv')
        df_probs = df_probs.pivot(columns=['hour'], values='counts', index=df_probs.columns.drop(['hour', 'counts']))
        if not weekend_split:
            df_dist = df_probs.T.corr(method=jensenshannon)
            df_dist.values[[np.arange(df_dist.shape[0])] * 2] = 0.0

        else:
            df_dist_satsun = df_probs.loc[(slice(None), True), :].T.corr(method=jensenshannon)
            df_dist_satsun.values[[np.arange(df_dist_satsun.shape[0])] * 2] = 0.0
            df_dist_not_satsun = df_probs.loc[(slice(None), False), :].T.corr(method=jensenshannon)
            df_dist_not_satsun.values[[np.arange(df_dist_not_satsun.shape[0])] * 2] = 0.0

        print (df_dist_not_satsun)
        df_dist_not_satsun.to_csv('tmp_2.csv')
        raise RuntimeError

    def _gather_station_weekday_hour(self, df):
        '''Bla bla

        '''
        df['weekday'] = df[self.time_key].dt.dayofweek
        df['hour'] = df[self.time_key].dt.hour
        df['satsun'] = df['weekday'].map({0: False, 1: False, 2: False, 3: False, 4: False, 5: True, 6: True})

        group = df.groupby(by=[self.station_key, 'satsun', 'hour'])
        df_count = group.count().iloc[:, 0].rename("counts")
        df_count = df_count.reset_index()

        return df_count

    def _post_station_types(self, collection):
        '''Bla bla

        '''
        df = pd.concat(collection, ignore_index=True)
        df = df.groupby([self.station_key, 'satsun', 'hour']).sum()
        print(df)
        df.to_csv('tmp.csv')

    def _gather_totals_per_x(self, df, x):
        '''Bla bla

        '''
        if x == 'weekday':
            df[x] = df[self.time_key].dt.dayofweek
            group = df.groupby(x)

        elif x == 'week':
            df[x] = df[self.time_key].dt.isocalendar().week
            group = df.groupby(x)

        elif x == 'month':
            df[x] = df[self.time_key].dt.month_name()
            group = df.groupby(x)

        df_count = group.count().iloc[:, 0].rename("counts")
        df_count = df_count.reset_index()

        return df_count

    def _post_totals_per_x(self, collection, x):
        '''Bla bla

        '''
        df = pd.concat(collection, ignore_index=True)
        df = df.groupby(x).sum()

        return df
