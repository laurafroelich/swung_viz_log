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

filen = "{}well_log_data.txt".format(DATA_PATH)
import json
import pandas as pd

with open(filen, 'r') as f:
    j_data = json.load(f)

for i, item in enumerate(j_data):
    if i == 0:
        p_data = pd.DataFrame(item)
    else:
        p_data = p_data.append(pd.DataFrame(item))







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
    df=df.sort_index()
    df.index = -df.index

    #depth_step = np.mean((df.index.values[:-1] - df.index.values[1:]))
    #depth_window_size = window_size * depth_step

    #df['left'] = df.index - depth_window_size
    #df['roll_max'] = df['val'].rolling(window_size).max()
    #df['roll_min'] = df['val'].rolling(window_size).min()
    return ColumnDataSource(data=df)

def make_plot(current,  curve, plot_width=800, plot_height=1000):
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
    
    #plot.quad(top='left', bottom='Depth', left='roll_min', right='roll_max', source=average, color=Blues4[2],  legend="Average")
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
    #global group_select
    curve = curve_select.value
    group = group_select.value
    filee = well_select.value

    group_file = "{}EAGE_Hackathon_2018_{}{}{}".format(DATA_PATH,"Well_", filee,".csv")
    group_df = pd.read_csv(group_file)
    group_df = group_df[group_df['Surface']=='group']
    #print(list(group_df['name'].unique()))
    #group_select = Select(value=curve, title='Group', options= list(group_df['name'].unique()))


    if group!='All':

         base_top = group_df[group_df['name'] == group]

         top = base_top[base_top['Obs#']=='Top'].values
         base = base_top[base_top['Obs#']=='Base'].values
         
         if len(top)>0:
             top = base_top[base_top['Obs#']=='Top']['MD'].values[0]
         else:
            top=0
            
         if len(base)>0:
            base = base_top[base_top['Obs#']=='Base']['MD'].values[0]
         else:
            base=5000
    else:
        base=5000
        top=0




    plot.title.text = curve
    plot.xaxis.axis_label = curve


    df_small1=df1[(df1['Depth']>top) & (df1['Depth']<base)]
    #df_small2=df2[(df2['Depth']>top) & (df2['Depth']<base)]



    src1 = get_dataset(df_small1[['Depth',curve]]) 

    source1.data.update(src1.data)

    small_df = df_small1[curve]
    
    update_text(small_df.max(), small_df.min(), small_df.mean(), small_df.std())

def update_text(maxVal, minVal, meanVal, stdVal):
    maxs.text = "Max {0:.2f}".format(maxVal)
    mins.text = "Min {0:.2f}".format(minVal)
    mean.text = "Mean {0:.2f}".format(meanVal)
    std.text = "Std {0:.2f}".format(stdVal)




#print(p_data['Well'].unique())
#df1 = (p_data[p_data['File_Name'] == 'GR_RES_Well-I_A.LAS']).copy()
df1 = (p_data[p_data['Well'] == 'A']).copy()

#df1,df2 = [lasio.read(fname).df() for fname in [file1, file2]]
#df1.index = -df1.index
#df2.index = -df2.index

group_file = "{}EAGE_Hackathon_2018_{}".format(DATA_PATH, "Well_I_A.csv")
group_df = pd.read_csv(group_file)
group_df = group_df[group_df['Surface']=='group']
group_select = Select(value='AA', title='Group', options= list(group_df['name'].unique())+['All'])


curve = 'Gamma'
well = 'A'
curve_select = Select(value=curve, title='Curve', options= ['Gamma', 'Res'])
print(p_data.columns)
print(group_df['Surface'].unique())
well_select = Select(value='A', title='Well', options= list(p_data['Well'].unique()))



#df = pd.read_csv(join(dirname(__file__), 'data/2015_weather.csv'))
source1 = get_dataset(df1[['Depth','Gamma']])
plot = make_plot(source1, curve)

##
WIDTH = 500
HEIGHT = 1



maxs = PreText(text='Max ', width=WIDTH, height=HEIGHT)
mins = PreText(text='Min ', width=WIDTH, height=HEIGHT)
mean = PreText(text='Mean ', width=WIDTH, height=HEIGHT)
std = PreText(text='Std ', width=WIDTH, height=HEIGHT)

curve_select.on_change('value', update_plot)
group_select.on_change('value', update_plot)
well_select.on_change('value', update_plot)
#distribution_select.on_change('value', update_plot)

controls = column(curve_select, group_select, well_select,maxs, mins, mean, std)#, distribution_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Log quality visualisation"
