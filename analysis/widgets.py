'''Various analysis widgets

'''
import pandas as pd

def total_rental_by_date(rental_counts):
    df_counts_per_day = pd.DataFrame(pd.concat(rental_counts)).reset_index()
    df_counts_per_day = df_counts_per_day.rename(columns={'index' : 'date', 'start_date' : 'counts'})
    df_counts_per_day = df_counts_per_day.groupby('date').sum().reset_index()
    df_counts_per_day['day_of_week'] = df_counts_per_day['date'].dt.dayofweek
    df_counts_per_day['date'] = pd.to_datetime(df_counts_per_day['date'])

    x1 = df_counts_per_day.loc[df_counts_per_day['date'] <= '2019-07-28'].reset_index()
    x2 = df_counts_per_day.loc[(df_counts_per_day['date'] <= '2020-07-26') & (df_counts_per_day['date'] >= '2020-01-06')].reset_index()
    df_collate = pd.DataFrame({'2019' : x1['counts'], '2020' : x2['counts']}).reset_index()

class StandardAnalyze(object):

    def __init__(self, chunksize=100000, time_key=None, station_key=None, blob=None):

        self.chunksize = chunksize
        self.time_key = time_key
        self.station_key = station_key
        self.blob = blob

        self.widget = {'station_types' : {'gather_func' : self._gather_station_weekday_hour,
                                          'post_func' : self._post_station_types},
                       'totals_per_x' : {'gather_func' : self._gather_totals_per_x,
                                         'post_func' : self._post_totals_per_x}}

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
