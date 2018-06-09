import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
from flask import make_response, render_template
import base64
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8




def plot_two_columns(df, column1, column2):
    plt.scatter(df[column1], df[column2])

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    figdata_png = figfile.getvalue().decode('latin1')
    #figdata_png = base64.b64encode(figfile)



#fig = Figure()
    #axis = fig.add_subplot(1,1,1)
    #axis.plot(df[column1], df[column2])
    #canvas = FigureCanvas(fig)
    #output = BytesIO()
    #response = base64.b64encode(output.getvalue())
    #response = make_response(figdata_png)
    #response.mimetype = 'image/png'

    return figdata_png


def plot_bokeh():

    # chart defaults
    color = '#FF0000'
    start = 0
    finish = 10

    # Create a polynomial line graph with those arguments
    x = list(range(start, finish + 1))
    fig = figure(title='Polynomial')
    fig.line(x, [i ** 2 for i in x], color=color, line_width=2)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)

    return script, div, js_resources, css_resources

