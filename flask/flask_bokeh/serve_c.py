from os.path import join, dirname

import pandas as pd
import lasio

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select
from bokeh.palettes import Blues4
from bokeh.plotting import figure

DATA_PATH = "../../data/EAGE2018/"

MEAS_SIZE = .15
INDEX_WINDOW = 100
DEPTH_WINDOW = INDEX_WINDOW * MEAS_SIZE

file1 = "{}Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS".format(DATA_PATH)
file2 = "{}Well-AA_finished/HQLD_B_2C1_85-1_BHC-GR_COMPOSITED_1.LAS".format(DATA_PATH)

def get_dataset(src):
    """Prepare dataset for plotting

    Compute rolling averages of a src dataframe and convert to bokeh format
    # Arguments
        src: pandas dataframe to be converted
    # Returns
        A Source object containing the rolling averages
    """
    df=src.to_frame().copy()
    df.columns = ['val']

    df['left'] = df.index - DEPTH_WINDOW
    df['roll_max'] = df['val'].rolling(INDEX_WINDOW).max()
    df['roll_min'] = df['val'].rolling(INDEX_WINDOW).min()
    return ColumnDataSource(data=df)

def make_plot(source1, source2, title):
    plot = figure( plot_width=800, plot_height=800, tools="", toolbar_location=None)#x_axis_type="datetime",
    #plot = df1['GR'].plot().get_figure()
    #plot.title.text = title

    #plot.line(y='DEPT', x='val', source = source2, color=Blues4[2],  legend="W2")
    plot.quad(top='left', bottom='DEPT', left='roll_min', right='roll_max', source = source2, color=Blues4[2],  legend="W2")
    plot.line(y='DEPT', x='val', source = source1, color=Blues4[1],  legend="W1")
            
            

    """

    plot.quad(top='average_max_temp', bottom='average_min_temp', left='left', right='right',
              color=Blues4[1], source=source, legend="Average")
    plot.quad(top=''#actual_max_temp', bottom='actual_min_temp', left='left', right='right',
              color=Blues4[0], alpha=0.5, line_color="black", source=source, legend="Actual")
    """

    # fixed attributes
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Temperature (F)"
    plot.axis.axis_label_text_font_style = "bold"
    #plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.3

    return plot

def update_plot(attrname, old, new):
    city = city_select.value
    plot.title.text = "Weather data for " + city

    print('reloading ds')
    
    src1, src2 = [get_dataset(df[city]) for df in [df1,df2]]
    print('ds updated')

    source1.data.update(src1.data)
    source2.data.update(src2.data)

df1,df2 = [lasio.read(fname).df() for fname in [file1, file2]]
df1.index = -df1.index
df2.index = -df2.index

city = 'Austin'

cities = {
    'Austin': {
        'airport': 'AUS',
        'title': 'Austin, TX',
    },
    'Boston': {
        'airport': 'BOS',
        'title': 'Boston, MA',
    },
    'Seattle': {
        'airport': 'SEA',
        'title': 'Seattle, WA',
    }
}

city_select = Select(value=city, title='City', options=list(df2.columns.values))


#df = pd.read_csv(join(dirname(__file__), 'data/2015_weather.csv'))
source1, source2 = [get_dataset(df['GR']) for df in [df1,df2]]
print('dataset DONE')
plot = make_plot(source1, source2, "Weather data for " + cities[city]['title'])

city_select.on_change('value', update_plot)
#distribution_select.on_change('value', update_plot)

controls = column(city_select)#, distribution_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Weather"
