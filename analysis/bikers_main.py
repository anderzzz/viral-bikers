'''Bla bla

'''
import pandas as pd
from bokeh.plotting import show

from analysis.analysis_srel import gather_root, filter_date_range, cmp_counts_hour_resolve, cmp_stations_most_traffic, \
                                   cmp_pdist_station_hour, cmp_count_range_station_hour, \
                                   cmp_count_cov_station_hour, cmp_total_per_x, cmp_total_counts, \
                                   cmp_js_station_station, cmp_deviation, cmp_pdist_station_day_hour, cmp_add_zeros
from analysis.viz import viz_box_by_hour, viz_cov_by_hour, viz_js_stations, viz_pfunc_by_hour, \
                         viz_pfunc_by_hour_33grid, viz_dist_map

DATABLOB_TPE = '../data_blob/taipei_bikeshare.csv'
DATABLOB_LON = '../data_blob/london_bikeshare.csv'
DATABLOB_HEL = '../data_blob/helsinki_bikeshare.csv'
DATABLOB_TOR = '../data_blob/toronto_bikeshare.csv'

CHUNKSIZE = 100000

CITY_DATA = {'taipei' : {'time_key_s' : 'start_rental_date_hour',
                         'time_key_e' : 'end_rental_date_hour',
                         'station_key_s' : 'start_station_name_tradchinese',
                         'station_key_e' : 'end_station_name_tradchinese',
                         'blob' : DATABLOB_TPE},
             'london' : {'time_key_s' : 'start_rental_date_time',
                         'time_key_e' : 'end_rental_date_time',
                         'station_key_s' : 'start_station_id',
                         'station_key_e' : 'end_station_id',
                         'blob' : DATABLOB_LON},
             'toronto' : {'time_key_s' : 'start_rental_date_time',
                          'time_key_e' : 'end_rental_date_time',
                          'station_key_s' : 'start_station_name',
                          'station_key_e' : 'end_station_name',
                          'blob' : DATABLOB_TOR},
             'helsinki' : {'time_key_s' : 'start_rental_date_time',
                           'time_key_e' : 'end_rental_date_time',
                           'station_key_s' : 'start_station_name',
                           'station_key_e' : 'end_station_name',
                           'blob' : DATABLOB_HEL}
             }
CITY_RUN = 'london'

#
# Gather raw data for city and date range
#
#df = gather_root(CITY_DATA[CITY_RUN]['blob'],
#                 filter_func=filter_date_range,
#                 lower='2018-01-01', upper='2019-12-31', time_key=CITY_DATA[CITY_RUN]['time_key_s'])
#
#df.to_csv('tmp.csv')
#print (df)
#df = pd.read_csv('tmp.csv', index_col=0)
#
#
#  Create an aggregate rental events column, rather than start and end
#
#df_s = cmp_counts_hour_resolve(df,
#                               station_key=CITY_DATA[CITY_RUN]['station_key_s'],
#                               time_key=CITY_DATA[CITY_RUN]['time_key_s'])
#df_e = cmp_counts_hour_resolve(df,
#                               station_key=CITY_DATA[CITY_RUN]['station_key_e'],
#                               time_key=CITY_DATA[CITY_RUN]['time_key_e'])
#df = cmp_total_counts(df_s, df_e, CITY_DATA[CITY_RUN]['station_key_s'], CITY_DATA[CITY_RUN]['station_key_e'])

#
# Aggregate system totals per week
#
#df_tots = cmp_total_per_x(df, 'week')

#
# Get top 25% of stations by rental events and filter data
#
#stations_index = cmp_stations_most_traffic(df, 0.25, station_key='station')
#df = df.loc[df['station'].isin(stations_index)]
#print (df)
#df.to_csv('tmp1.csv')
df = pd.read_csv('tmp1.csv', index_col=0)

#
# Estimate frequency of rental events per hour and compute Jensen-Shannon distances between frequency curves
#
df_p = cmp_pdist_station_hour(df, station_key='station')
df_js_wd, df_js_we = cmp_js_station_station(df_p, station_key='station')
p0 = viz_js_stations(df_js_wd)
p0s = viz_pfunc_by_hour(df_p.loc[492, False])
show(p0)

#
# Estimate R(h; S) distributions, as function of h and stations S
#
df_count_range = cmp_count_range_station_hour(df, station_key='station')
print (df_count_range)
p1 = viz_box_by_hour(df_count_range.loc[772, False])
show(p1)

#
# Estimate covariance between hour and hour for each station
#
df_cov = cmp_count_cov_station_hour(df, station_key='station')
print (df_cov)
p2 = viz_cov_by_hour(df_cov.loc[772, False])
show(p2)

#
# Collect 2020 data
#
#df_2020 = gather_root(CITY_DATA[CITY_RUN]['blob'],
#                      filter_func=filter_date_range,
#                      lower='2020-01-01', upper='2020-07-31', time_key=CITY_DATA[CITY_RUN]['time_key_s'])
#df_2020.to_csv('tmp_2020.csv')
#df_2020_s = cmp_counts_hour_resolve(df_2020,
#                             station_key=CITY_DATA[CITY_RUN]['station_key_s'],
#                             time_key=CITY_DATA[CITY_RUN]['time_key_s'])
#df_2020_e = cmp_counts_hour_resolve(df_2020,
#                                  station_key=CITY_DATA[CITY_RUN]['station_key_e'],
#                                  time_key=CITY_DATA[CITY_RUN]['time_key_e'])
#df_2020 = cmp_total_counts(df_2020_s, df_2020_e, CITY_DATA[CITY_RUN]['station_key_s'], CITY_DATA[CITY_RUN]['station_key_e'])
#
#df_2020_tots = cmp_total_per_x(df_2020, 'week')
#
#df_2020 = df_2020.loc[df_2020['station'].isin(stations_index)]
#print (df_2020)
#df_2020.to_csv('tmp1_2020.csv')
df_2020 = pd.read_csv('tmp1_2020.csv', index_col=0)

df_2020 = cmp_add_zeros(df_2020, station_key='station')
df_2020_dist_wd, df_2020_dist_we = cmp_deviation(df_count_range, df_cov, df_2020, station_key='station')
viz_dist_map(df_2020_dist_wd)

