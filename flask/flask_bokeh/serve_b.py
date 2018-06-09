import numpy as np
from bokeh.layouts import column, row
import holoviews as hv
from bokeh.io import curdoc

from bokeh.io import show
from bokeh.layouts import layout
from bokeh.models import Slider, Button
from bokeh.models.widgets import Select

import lasio

renderer = hv.renderer('bokeh').instance(mode='server')

# Create the holoviews app again
def sine(phase):
    xs = np.linspace(0, np.pi*4)
    return hv.Curve((xs, np.sin(xs+phase))).options(width=800)

stream = hv.streams.Stream.define('Phase', phase=0.)()
dmap = hv.DynamicMap(sine, streams=[stream])

input_file = "../../data/EAGE2018/Well-A_finished/HQLD_B_2C1_75-1_Well-A_ISF-BHC-MSFL-GR__COMPOSIT__1.LAS"
result = lasio.read(input_file).df()
result_small = result['GR']


points = list(zip(result['GR'], -result.index.values))
dmap = hv.Curve(points, name='p1')



# Define valid function for FunctionHandler
# when deploying as script, simply attach to curdoc
def modify_doc(doc):
    # Create HoloViews plot and attach the document
    hvplot = renderer.get_plot(dmap, doc)

    # Create a slider and play buttons
    def animate_update():
        year = slider.value + 0.2
        if year > end:
            year = start
        slider.value = year

    def slider_update(attrname, old, new):
        # Notify the HoloViews stream of the slider update 
        stream.event(phase=new)
        
    start, end = 0, np.pi*2
    slider = Slider(start=start, end=end, value=start, step=0.2, title="Phase")
    slider.on_change('value', slider_update)
    
    callback_id = None
    hplot = None

    def animate(attr, old, new):
        global callback_id
        global hplot
        curdoc().clear()
        points = list(zip(result[new], -result.index.values))
        dmap = hv.Curve(points)
        print('changing')
        hplot = renderer.get_plot(dmap, doc)
        plot = layout([
        [hplot.state],
        [select]], sizing_mode='fixed', name='1')
        doc.add_root(plot)
        rootLayout = curdoc()



    button = Button(label='► Play', width=60)
    

    select = Select(title="Option:", value="GR", options=list(result.columns.values))
    #button.on_click(animate)
    select.on_change('value',animate)
    print(type(hplot))
    
    # Combine the holoviews plot and widgets in a layout
    plot = layout([
    [hvplot.state],[select]
    ], sizing_mode='fixed', name='p1')
    print(type(plot))
    
    doc.add_root(plot)
    
    #doc.add_root(plot)
    return doc

doc = modify_doc(curdoc()) 


"""
import numpy as np
import holoviews as hv
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Select
import holoviews.plotting.bokeh

renderer = hv.renderer('bokeh')

points = hv.Points(np.random.randn(1000,2 )).options(tools=['box_select', 'lasso_select'])
selection = hv.streams.Selection1D(source=points)

def selected_info(index):
    arr = points.array()[index]
    if index:
        label = 'Mean x, y: %.3f, %.3f' % tuple(arr.mean(axis=0))
    else:
        label = 'No selection'
    return points.clone(arr, label=label).options(color='red')


output_file("select.html")

select = Select(title="Option:", value="foo", options=["foo", "bar", "baz", "quux"])

def sine(phase):
    xs = np.linspace(0, np.pi*4)
    return hv.Curve((xs, np.sin(xs+phase))).options(width=800)

stream = hv.streams.Stream.define('Phase', phase=0.)()
dmap = hv.DynamicMap(sine, streams=[stream])

layout = points + hv.DynamicMap(selected_info, streams=[selection]) 

doc = renderer.server_doc(layout)

#doc = dmap#curdoc()#$renderer.server_doc(layout)


plot = layout([
    [hvplot.state],
    ], sizing_mode='fixed')



doc.add_root(plot)
doc.title = 'HoloViews App'
"""
