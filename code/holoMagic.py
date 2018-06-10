from os.path import join, dirname

import pandas as pd
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, PreText
from bokeh.palettes import Blues4
from bokeh.plotting import figure

DATA_PATH = "../data/EAGE2018/"

#file names
file1 = "{}Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS".format(DATA_PATH)
file2 = "{}Well-AA_finished/HQLD_B_2C1_85-1_BHC-GR_COMPOSITED_1.LAS".format(DATA_PATH)

file = "../data/EAGE2018/well_log_data.txt"
import json
import pandas as pd

with open(file, 'r') as f:
    j_data = json.load(f)

for i, item in enumerate(j_data):
    if i == 0:
        p_data = pd.DataFrame(item)
    else:
        p_data = p_data.append(pd.DataFrame(item))

df1 = (p_data[p_data['File_Name'] == 'GR_RES_Well-X-27.las']).copy()
df2 = (p_data[p_data['File_Name'] == 'GR_RES_Well-I_A.LAS']).copy()





def get_dataset(src, window_size=100):
    """Prepare dataset for plotting

    Compute rolling averages of a src dataframe and convert to bokeh format
    # Arguments
        src: pandas dataframe to be converted
    # Returns
        A Source object containing the rolling averages
    """
    df=src.set_index('Depth').copy()
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
    
    plot.quad(top='left', bottom='Depth', left='roll_min', right='roll_max', source=average, color=Blues4[2],  legend="Average")
    plot.line(y='Depth', x='val', source=current, color=Blues4[1],  legend="Current data")
            
            

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

    
    src1, src2 = [get_dataset(df[['Depth',curve]]) for df in [df1,df2]]

    source1.data.update(src1.data)
    source2.data.update(src2.data)

    small_df = df1[new]
    
    update_text(small_df.max(), small_df.min(), small_df.mean(), small_df.std())

def update_text(maxVal, minVal, meanVal, stdVal):
    maxs.text = "Max {0:.2f}".format(maxVal)
    mins.text = "Min {0:.2f}".format(minVal)
    mean.text = "Mean {0:.2f}".format(meanVal)
    std.text = "Std {0:.2f}".format(stdVal)




#df1,df2 = [lasio.read(fname).df() for fname in [file1, file2]]
#df1.index = -df1.index
#df2.index = -df2.index

curve = 'Gamma'
curve_select = Select(value=curve, title='Curve', options= ['Gamma', 'Res'])


#df = pd.read_csv(join(dirname(__file__), 'data/2015_weather.csv'))
source1, source2 = [get_dataset(df[['Depth','Gamma']]) for df in [df1,df2]]
plot = make_plot(source1, source2, curve)

##
WIDTH = 500
HEIGHT = 1

maxs = PreText(text='Max ', width=WIDTH, height=HEIGHT)
mins = PreText(text='Min ', width=WIDTH, height=HEIGHT)
mean = PreText(text='Mean ', width=WIDTH, height=HEIGHT)
std = PreText(text='Std ', width=WIDTH, height=HEIGHT)

curve_select.on_change('value', update_plot)
#distribution_select.on_change('value', update_plot)

controls = column(curve_select, maxs, mins, mean, std)#, distribution_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Log quality visualisation"
