from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from web.models import *

# Globals
tools = "pan,wheel_zoom,box_zoom,reset,save"

# Plot 1
def test_plot1():
    plot = figure(tools=tools)
    plot.circle([1, 2], [3, 4])
    plot.sizing_mode = 'scale_width'
    return plot

def test_plot2():
    plot = figure(tools=tools)
    plot.circle([1, 2], [3, 4])
    plot.sizing_mode = 'scale_width'
    return plot