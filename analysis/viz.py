'''Bokeh visualization functions

'''
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import TSNE, MDS

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter, LinearColorMapper, ColorBar, BasicTicker, \
                         Range1d, LabelSet, Label, Text
from bokeh.palettes import brewer, diverging_palette
from bokeh.layouts import gridplot

def _axis_adjust(p):
    p.yaxis.axis_label_text_font_size = '15px'
    p.yaxis.major_label_text_font_size = '15px'
    p.xaxis.axis_label_text_font_size = '15px'
    p.xaxis.major_label_text_font_size = '15px'
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
    p.line(x="hour", y="freq", source=source, line_color=brewer['PRGn'][7][0], line_width=5)

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

    print (df)
    df = df.reset_index()
    df = df.sort_values(by=['station', 'year', 'week', 'day'])
    print (df)
    raise RuntimeError
    p = figure()
    p = _axis_adjust(p)
    source = ColumnDataSource(df)

    max_dist = df.mahalanobis.max()
    mapper = LinearColorMapper(palette=brewer['PRGn'][11], low=0.0, high=max_dist)


def viz_js_stations(df, manifold='TSNE'):

    if manifold == 'TSNE':
        model = TSNE(metric='precomputed')
    elif manifold == 'MDS':
        model = MDS(dissimilarity='precomputed')
    else:
        raise ValueError('Unknown manifold method: {}'.format(manifold))
    model.fit(df.values)

    p = figure()
    p = _axis_adjust(p)
    source = ColumnDataSource({'x' : model.embedding_[:, 0], 'y' : model.embedding_[:, 1],
                               'station_key' : df.index})

    p.circle(x='x', y='y', source=source, fill_color=brewer['PRGn'][7][0], line_color=brewer['PRGn'][7][0])
    labels = LabelSet(x='x', y='y', text='station_key', level='glyph',
                      x_offset=5, y_offset=5, source=source, render_mode='canvas',
                      text_font_size='8px')
    p.xaxis.axis_label = 'TSNE coordinate 1'
    p.yaxis.axis_label = 'TSNE coordinate 2'
    p.yaxis.major_tick_line_color = 'white'
    p.xaxis.major_tick_line_color = 'white'
#    citation = Label(x=70, y=70, x_units='screen', y_units='screen',
#                     text='Collected by Luke C. 2016-04-01', render_mode='css',
#                     border_line_color='black', border_line_alpha=1.0,
#                     background_fill_color='white', background_fill_alpha=1.0)
#
    p.add_layout(labels)
#    p.add_layout(citation)
    return p


