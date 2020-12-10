'''Bokeh visualization functions

'''
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE, MDS

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter, LinearColorMapper, ColorBar, BasicTicker, \
                         Range1d, LabelSet, Label, Text, HoverTool, FixedTicker
from bokeh.palettes import brewer, diverging_palette
from bokeh.layouts import gridplot
from bokeh.transform import factor_cmap, transform

def _axis_adjust(p):
    p.yaxis.axis_label_text_font_size = '15px'
    p.yaxis.major_label_text_font_size = '15px'
    p.xaxis.axis_label_text_font_size = '15px'
    p.xaxis.major_label_text_font_size = '15px'
    return p

def viz_box_by_station(df, satsun=False, low=0, high=20):

    df = df.loc[(slice(None), satsun), :]
    df = df.sort_values(['median'], ascending=False)
    df = df.iloc[low:high]
    df = df.reset_index()
    df['station'] = df['station'].astype('str')
    stations = df['station'].tolist()

    p = figure(x_range=stations)
    p = _axis_adjust(p)

    source = ColumnDataSource(df.reset_index())
    p.segment(x0='station', y0='q_95', x1='station', y1='q_75', source=source, line_color='black')
    p.segment(x0='station', y0='q_05', x1='station', y1='q_25', source=source, line_color='black')
    p.rect(x='station', y='q_95', width=0.5, height=0.01, line_color='black', fill_color='black', source=source)
    p.rect(x='station', y='q_05', width=0.5, height=0.01, line_color='black', fill_color='black', source=source)
    p.vbar(x='station', top='q_75', bottom='median', width=0.7, fill_color=brewer['PRGn'][7][0], source=source,
           line_color='black')
    p.vbar(x='station', top='median', bottom='q_25', width=0.7, fill_color=brewer['PRGn'][7][6], source=source,
           line_color='black')

    p.yaxis.axis_label = '# Rental Events in a Day'
    p.xaxis.axis_label = 'Top Traffic Stations'
    p.xaxis.major_label_text_color = None
    p.xgrid.grid_line_color = None

    return p

def viz_box_by_hour(df):
    print (df)

    p = figure()
    p = _axis_adjust(p)

    source = ColumnDataSource(df)
    p.segment(x0='hour', y0='q_95', x1='hour', y1='q_75', source=source, line_color='black')
    p.segment(x0='hour', y0='q_05', x1='hour', y1='q_25', source=source, line_color='black')
    p.rect(x='hour', y='q_95', width=0.5, height=0.01, line_color='black', fill_color='black', source=source)
    p.rect(x='hour', y='q_05', width=0.5, height=0.01, line_color='black', fill_color='black', source=source)
    p.vbar(x='hour', top='q_75', bottom='median', width=0.7, fill_color=brewer['PRGn'][7][0], source=source, line_color='black')
    p.vbar(x='hour', top='median', bottom='q_25', width=0.7, fill_color=brewer['PRGn'][7][6], source=source, line_color='black')

    p.yaxis.axis_label = '# Rental Events'
    p.xaxis.axis_label = 'Hour'

    return p

def viz_pfunc_by_hour(df, axis_labels=True, y_range=None):

    p = figure(y_range=y_range)
    p = _axis_adjust(p)

    source = ColumnDataSource(df)
    p.line(x="hour", y="freq", source=source, line_color=brewer['PRGn'][7][6], line_width=5)

    if axis_labels:
        p.yaxis.axis_label = 'Normalized Rental Event Occurrence'
        p.xaxis.axis_label = 'Hour'

    return p

def viz_pfunc_by_hour_33grid(df, satsun, station_keys):

    p = figure()
    p = _axis_adjust(p)

    df = df.reset_index()
    df = df.loc[df['station'].isin(station_keys)]
    df = df.loc[df['satsun'] == satsun]

    p_ = []
    for station_id in station_keys:
        if station_id is None:
            p = figure(y_range=Range1d(0.0, 0.25))
            p.outline_line_color = None
        else:
            p = viz_pfunc_by_hour(df.loc[df['station'] == station_id], axis_labels=False, y_range=Range1d(0.0, 0.25))
        p_.append(p)

    show(gridplot(p_, ncols=3, plot_width=300, plot_height=300))

def viz_cov_by_hour(df):
    #df.covariance = df.covariance.apply(lambda x: np.sqrt(x) if x >=0.0 else -1.0 * np.sqrt(-1.0 * x))

    p = figure()
    p = _axis_adjust(p)

    source = ColumnDataSource(df.reset_index())
    print (df.reset_index())

    palette = diverging_palette(brewer['Purples'][9], brewer['Greens'][9], 18)
    max_var = df.covariance.max()
    mapper = LinearColorMapper(palette=palette, low=-1.0 * max_var, high=max_var)

    p.rect(x='hour1', y='hour2', width=1, height=1, source=source,
           fill_color={'field' : 'covariance', 'transform' : mapper},
           line_color=None)
    p.x_range = Range1d(-0.5, 23.5)
    p.y_range = Range1d(-0.5, 23.5)

    p.yaxis.axis_label = 'Hour of Day'
    p.xaxis.axis_label = 'Hour of Day'

    #color_bar = ColorBar(color_mapper=mapper,major_label_text_font_size='7px',
    #                     ticker=BasicTicker(desired_num_ticks=18),
    #                     label_standoff=6, border_line_color=None, location=(0,0))
    #p.add_layout(color_bar, 'right')

    return p

def viz_dist_map(df):

    #df = df.loc[df['station']]
    df = df.loc[(df['week']>=2) & (df['week']<=29)]

    df.station = df.station.astype('str')
    df['unique_day'] = df.apply(lambda x: 'w{}d{}'.format(x['week'], x['day']), axis=1)
    df.unique_day = df.unique_day.astype('str')
    df = df.drop(columns=['year','week','day','satsun','counts'])
    df = df.set_index('unique_day').reset_index()

    source = ColumnDataSource(df)
    mapper = LinearColorMapper(palette=brewer['PRGn'][11], low=-0.05, high=1.05)

    print (list(df.percentile))

    p = figure(plot_width=1000, plot_height=800,
               x_range=list(df.unique_day.unique()), y_range=list(df.station.unique()),
               toolbar_location='above', x_axis_location="above")

    p.rect(y="station", x="unique_day", width=1, height=1, source=source,
           line_color=None, fill_color=transform('percentile', mapper))

    color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                         ticker=FixedTicker(ticks=[0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95]),
                         label_standoff=5, orientation='horizontal')
    p.add_layout(color_bar, 'below')

    p.xaxis.major_label_text_color = None
    p.yaxis.major_label_text_color = None
    p.add_tools(HoverTool(
        tooltips=[('station', '@station'),
                  ('day', '@unique_day')]
    ))

    return p

def viz_js_stations_two(df, manifold='TSNE'):

    if manifold == 'TSNE':
        model = TSNE(metric='precomputed')
    elif manifold == 'MDS':
        model = MDS(dissimilarity='precomputed')
    else:
        raise ValueError('Unknown manifold method: {}'.format(manifold))
    model.fit(df.values)

    p = figure()
    p = _axis_adjust(p)
    source = ColumnDataSource({'x': model.embedding_[:, 0], 'y': model.embedding_[:, 1],
                               'station_key': df.index.get_level_values(0), 'city': df.index.get_level_values(1)})
    p.circle(x='x', y='y', source=source,
             fill_color=factor_cmap('city', [brewer['PRGn'][7][0], brewer['PRGn'][7][6]], ['London', 'Taipei']),
             line_color=factor_cmap('city', [brewer['PRGn'][7][0], brewer['PRGn'][7][6]], ['London', 'Taipei']),
             size=10.0, fill_alpha=0.6)

    labels = LabelSet(x='x', y='y', text='station_key', level='glyph',
                      x_offset=5, y_offset=5, source=source, render_mode='canvas',
                      text_font_size='6px')
    p.add_tools(HoverTool(
        tooltips=[('station', '@station_key')]
    ))
    p.xaxis.axis_label = 'MDS Embedded Coordinate 1'
    p.yaxis.axis_label = 'MDS Embedded Coordinate 2'
    p.yaxis.major_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    #p.add_layout(labels)

    return p

def viz_js_stations(df, manifold='MDS'):

    if manifold == 'TSNE':
        model = TSNE(metric='precomputed')
    elif manifold == 'MDS':
        model = MDS(dissimilarity='precomputed')
    else:
        raise ValueError('Unknown manifold method: {}'.format(manifold))
    model.fit(df.values)

    p = figure()
    p = _axis_adjust(p)
    special_stations_1 = [789,625,248,658,404,719,785,252,111,191,307]
    special_stations_2 = [433,393,392,361,331,214,215,193,154,140,66,41,12]
    all_special = special_stations_1 + special_stations_2
    size_mapper = lambda x: 20 if int(x) in all_special else 10
    color_mapper = lambda x: brewer['PRGn'][11][10] if int(x) in special_stations_1 else \
        (brewer['PRGn'][11][0] if int(x) in special_stations_2 else brewer['PRGn'][11][5])
    sizes = [size_mapper(station) for station in df.index]
    colours = [color_mapper(station) for station in df.index]

    source = ColumnDataSource({'x' : model.embedding_[:, 0], 'y' : model.embedding_[:, 1],
                               'station_key' : df.index, 'sizes' : sizes, 'colours' : colours})

    p.circle(x='x', y='y', source=source, fill_color='colours', line_color=brewer['PRGn'][7][0],
             size='sizes', fill_alpha=0.6)
    #labels = LabelSet(x='x', y='y', text='station_key', level='glyph',
    #                  x_offset=5, y_offset=5, source=source, render_mode='canvas',
    #                  text_font_size='8px')
    p.add_tools(HoverTool(
        tooltips=[('station', '@station_key')]))
    p.xaxis.axis_label = 'MDS Embedded Coordinate 1'
    p.yaxis.axis_label = 'MDS Embedded Coordinate 2'
    p.yaxis.major_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    #p.add_layout(labels)
#    p.add_layout(citation)
    show(p)

    return p

def viz_comp_by_hour(df_base, df_2020):
    '''Bla bla

    '''
    print (df_base)
    print (df_2020)

    pp = viz_box_by_hour(df_base)

    df_2020 = df_2020.loc[df_2020['satsun'] == False]
    df_2020 = df_2020.loc[df_2020['week'].isin([13,14,15])]
    gg = df_2020.groupby(['hour']).mean()

    source = ColumnDataSource(gg.reset_index())
    pp.circle(x='hour', y='counts', source=source, color='red', size=10, fill_alpha=0.75, line_color='red')

    return pp
