from os.path import join, dirname

import pandas as pd
import numpy as np
import lasio

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select
from bokeh.palettes import Blues4
from bokeh.plotting import figure

DATA_PATH = "../data/EAGE2018/"

#file names
file1 = "{}Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS".format(DATA_PATH)
file2 = "{}Well-AA_finished/HQLD_B_2C1_85-1_BHC-GR_COMPOSITED_1.LAS".format(DATA_PATH)

def get_dataset(src, window_size=100):
    """Prepare dataset for plotting

    Compute rolling averages of a src dataframe and convert to bokeh format
    # Arguments
        src: pandas dataframe to be converted
    # Returns
        A Source object containing the rolling averages
    """
    df=src.to_frame().copy()
    df.columns = ['val']

    depth_step = np.mean((df.index.values[:-1] - df.index.values[1:]))
    depth_window_size = window_size * depth_step

    df['left'] = df.index - depth_window_size
    df['roll_max'] = df['val'].rolling(window_size).max()
    df['roll_min'] = df['val'].rolling(window_size).min()
    return ColumnDataSource(data=df)

def make_plot(current, average, curve, plot_width=800, plot_height=1000):
    """Show plot of current data vs. average

    Compute plot of current data vs. averaged data for outlier detection
    # Arguments
        current: bokeh Source object containing the current data
        average: bokeh Source object containing the averaged data
        curve: curve to be plotted
    # Returns
        A Source object containing the rolling averages
    """

    plot = figure( plot_width=plot_width, plot_height=plot_height, tools="", toolbar_location=None)
    
    plot.quad(top='left', bottom='DEPT', left='roll_min', right='roll_max', source=average, color=Blues4[2],  legend="Average")
    plot.line(y='DEPT', x='val', source=current, color=Blues4[1],  legend="Current data")
            
            

    """

    plot.quad(top='average_max_temp', bottom='average_min_temp', left='left', right='right',
              color=Blues4[1], source=source, legend="Average")
    plot.quad(top=''#actual_max_temp', bottom='actual_min_temp', left='left', right='right',
              color=Blues4[0], alpha=0.5, line_color="black", source=source, legend="Actual")
    """

    # fixed attributes
    plot.xaxis.axis_label = curve
    plot.yaxis.axis_label = "Depth"
    plot.axis.axis_label_text_font_style = "bold"
    #plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.3

    return plot

def update_plot(attrname, old, new):
    curve = curve_select.value
    plot.title.text = curve
    plot.xaxis.axis_label = curve

    print('reloading ds')
    
    src1, src2 = [get_dataset(df[curve]) for df in [df1,df2]]
    print('ds updated')

    source1.data.update(src1.data)
    source2.data.update(src2.data)

df1,df2 = [lasio.read(fname).df() for fname in [file1, file2]]
df1.index = -df1.index
df2.index = -df2.index
print()

curve = 'GR'
curve_select = Select(value=curve, title='Curve', options=list(df2.columns.values))


#df = pd.read_csv(join(dirname(__file__), 'data/2015_weather.csv'))
source1, source2 = [get_dataset(df['GR']) for df in [df1,df2]]
print('dataset DONE')
plot = make_plot(source1, source2, curve)

curve_select.on_change('value', update_plot)
#distribution_select.on_change('value', update_plot)

controls = column(curve_select)#, distribution_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Weather"
