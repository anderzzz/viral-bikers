'''Analysis of impact on biking during covid times

'''
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.palettes import brewer
from bokeh.layouts import gridplot

from analysis.widgets import StandardAnalyze

DATABLOB_TPE = '../data_blob/taipei_bikeshare.csv'
DATABLOB_LON = '../data_blob/london_bikeshare.csv'
DATABLOB_HEL = '../data_blob/helsinki_bikeshare.csv'
DATABLOB_TOR = '../data_blob/toronto_bikeshare.csv'

EARLY_DATE_2019 = '2019-01-07'
EARLY_DATE_2020 = '2020-01-06'

CHUNKSIZE = 100000

CITY_DATA = {'taipei' : {'time_key' : 'start_rental_date_hour',
                         'station_key' : 'start_station_name_tradchinese',
                         'blob' : DATABLOB_TPE},
             'london' : {'time_key' : 'start_rental_date_time',
                         'station_key' : 'start_station_id',
                         'blob' : DATABLOB_LON},
             'toronto' : {'time_key' : 'start_rental_date_time',
                          'station_key' : 'start_station_name',
                          'blob' : DATABLOB_TOR},
             'helsinki' : {'time_key' : 'start_rental_date_time',
                           'station_key' : 'start_station_name',
                           'blob' : DATABLOB_HEL}
             }

tpe_bike = StandardAnalyze(**CITY_DATA['taipei'])
lon_bike = StandardAnalyze(**CITY_DATA['london'])
tor_bike = StandardAnalyze(**CITY_DATA['toronto'])

#
# Create 2018-2019 baseline for total system rentals by week
#
#df_tpe_week = tpe_bike.analyze('totals_per_x', gather_kwargs={'x' : 'week'}, analysis_kwargs={'x' : 'week'})
#df_tpe_week['counts'] = df_tpe_week['counts'] / 2.0
#df_tpe_week = df_tpe_week.rename(columns={'counts' : 'counts_tpe'})
#df_lon_week = lon_bike.analyze('totals_per_x', gather_kwargs={'x' : 'week'}, analysis_kwargs={'x' : 'week'})
#df_lon_week['counts'] = df_lon_week['counts'] / 2.0
#df_lon_week = df_lon_week.rename(columns={'counts' : 'counts_lon'})
#df_tor_week = tor_bike.analyze('totals_per_x', gather_kwargs={'x' : 'week'}, analysis_kwargs={'x' : 'week'})
#df_tor_week['counts'] = df_tor_week['counts'] / 2.0
#df_tor_week = df_tor_week.rename(columns={'counts' : 'counts_tor'})
#df_all = pd.concat([df_tpe_week, df_lon_week, df_tor_week], axis=1).reset_index()
#df_all.to_csv('df_all_week.csv')
df_all = pd.read_csv('df_all_week.csv', index_col=0)

source = ColumnDataSource(df_all)
fig_tot_week = figure(title='Total Bike Rentals per Week, 2018-19', y_axis_type='log',
                      x_range=(0,52), plot_width=800, plot_height=600)
fig_tot_week.title.text_font_size = '20px'
fig_tot_week.xaxis.axis_label = 'Week in Year'
fig_tot_week.xaxis.axis_label_text_font_size = '15px'
fig_tot_week.xaxis.major_label_text_font_size = '15px'
fig_tot_week.yaxis.axis_label = '#Rentals in Week (log-scale)'
fig_tot_week.yaxis.axis_label_text_font_size = '15px'
fig_tot_week.yaxis.major_label_text_font_size = '15px'
fig_tot_week.line(x='week', y='counts_tpe', source=source,
                  legend_label='Taipei',
                  color=brewer['PRGn'][7][0], line_width=3, line_alpha=0.6)
fig_tot_week.line(x='week', y='counts_lon', source=source,
                  legend_label='London',
                  color=brewer['PRGn'][7][6], line_width=3, line_alpha=0.6)
fig_tot_week.line(x='week', y='counts_tor', source=source,
                  legend_label='Toronto',
                  color=brewer['PRGn'][7][4], line_width=3, line_alpha=0.6)
fig_tot_week.legend.location = "bottom_right"
show(fig_tot_week)

#
# Create 2020 total system rentals by week and contrast to baseline
#
#df_tpe_week_2020 = tpe_bike.analyze('totals_per_x', gather_kwargs={'x' : 'week'}, analysis_kwargs={'x' : 'week'},
#                                    date_lower='2020-01-01', date_upper='2020-10-31')
#df_tpe_week_2020 = df_tpe_week_2020.rename(columns={'counts' : 'counts_tpe_2020'})
#df_lon_week_2020 = lon_bike.analyze('totals_per_x', gather_kwargs={'x' : 'week'}, analysis_kwargs={'x' : 'week'},
#                                    date_lower='2020-01-01', date_upper='2020-10-31')
#df_lon_week_2020 = df_lon_week_2020.rename(columns={'counts' : 'counts_lon_2020'})
#df_tor_week_2020 = tor_bike.analyze('totals_per_x', gather_kwargs={'x' : 'week'}, analysis_kwargs={'x' : 'week'},
#                                    date_lower='2020-01-01', date_upper='2020-10-31')
#df_tor_week_2020 = df_tor_week_2020.rename(columns={'counts' : 'counts_tor_2020'})
#df_all_2020 = pd.concat([df_tpe_week_2020, df_lon_week_2020, df_tor_week_2020], axis=1).reset_index()
#df_all_2020.to_csv('df_all_week_2020.csv')
df_all_2020 = pd.read_csv('df_all_week_2020.csv', index_col=0)

df_all_comp = pd.merge(df_all, df_all_2020, on='week', how='outer')
df_all_comp = df_all_comp.loc[df_all_comp['week'] <= 30]

source = ColumnDataSource(df_all_comp)
fig_tot_week_comp_tpe = figure(title='Total Bike Rentals per Week, 2020 Comparison', plot_width=800, plot_height=300, x_range=(1,30))
fig_tot_week_comp_tpe.line(x='week', y='counts_tpe', source=source,
                           legend_label='Taipei baseline',
                           color=brewer['PRGn'][7][0], line_width=3, line_alpha=0.6)
fig_tot_week_comp_tpe.line(x='week', y='counts_tpe_2020', source=source,
                           legend_label='Taipei 2020',
                           color=brewer['PRGn'][7][0], line_width=2, line_dash='dashed')
fig_tot_week_comp_tpe.legend.location = "bottom_right"
fig_tot_week_comp_tpe.xaxis.visible = False
fig_tot_week_comp_tpe.yaxis[0].formatter = NumeralTickFormatter(format='0a')
fig_tot_week_comp_lon = figure(plot_width=800, plot_height=300, x_range=(1,30))
fig_tot_week_comp_lon.line(x='week', y='counts_lon', source=source,
                           legend_label='London baseline',
                           color=brewer['PRGn'][7][6], line_width=3, line_alpha=0.6)
fig_tot_week_comp_lon.line(x='week', y='counts_lon_2020', source=source,
                           legend_label='London 2020',
                           color=brewer['PRGn'][7][6], line_width=2, line_dash='dashed')
fig_tot_week_comp_lon.legend.location = "bottom_right"
fig_tot_week_comp_lon.xaxis.visible = False
fig_tot_week_comp_lon.yaxis[0].formatter = NumeralTickFormatter(format='0a')
fig_tot_week_comp_tor = figure(plot_width=800, plot_height=300, x_range=(1,30))
fig_tot_week_comp_tor.line(x='week', y='counts_tor', source=source,
                           legend_label='Toronto baseline',
                           color=brewer['PRGn'][7][4], line_width=3, line_alpha=0.6)
fig_tot_week_comp_tor.line(x='week', y='counts_tor_2020', source=source,
                           legend_label='Toronto 2020',
                           color=brewer['PRGn'][7][4], line_width=2, line_dash='dashed')
fig_tot_week_comp_tor.yaxis[0].formatter = NumeralTickFormatter(format='0a')
fig_tot_week_comp_tor.legend.location = "bottom_right"
fig_tot_week_comp_tor.xaxis.major_label_overrides = {5:'Jan 27', 10: 'March 2', 15: 'April 6', 20: 'May 11', 25: 'June 15', 30: 'July 20'}
show(gridplot([fig_tot_week_comp_tpe, fig_tot_week_comp_lon, fig_tot_week_comp_tor],
              ncols=1, plot_width=800, plot_height=300))

df_tpe_prob = tpe_bike.analyze('prob_dist_deviate')
raise RuntimeError

df_onestation = pd.read_csv('tmp.csv', index_col=0)
print (df_onestation)
source = ColumnDataSource(df_onestation.reset_index())
fig_station = figure()
fig_station.line(x='index', y='counts', source=source)
show(fig_station)

raise RuntimeError
tpe_bike.analyze('station_to_station')