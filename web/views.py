from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge

# Create your views here.
@login_required(login_url='web:login')
def index(request):

    # Plot 1
    plot1 = figure()
    plot1.circle([1, 2], [3, 4])
    plot1.sizing_mode = 'scale_width'

    # Plot 2
    fruits = ['Apples', 'Pears', 'Nectarines',
              'Plums', 'Grapes', 'Strawberries']

    years = ['2015', '2016', '2017']

    data = {'fruits': fruits,
            '2015': [2, 1, 4, 3, 2, 4],
            '2016': [5, 3, 3, 2, 4, 6],
            '2017': [3, 2, 4, 4, 5, 3]}

    source = ColumnDataSource(data=data)

    plot2 = figure(x_range=fruits, y_range=(0, 10), toolbar_location=None)

    plot2.vbar(x=dodge('fruits', -0.25, range=plot2.x_range), top='2015', width=0.2, source=source,
        color="#c9d9d3", legend=value("2015"))

    plot2.vbar(x=dodge('fruits',  0.0,  range=plot2.x_range), top='2016', width=0.2, source=source,
        color="#718dbf", legend=value("2016"))

    plot2.vbar(x=dodge('fruits',  0.25, range=plot2.x_range), top='2017', width=0.2, source=source,
        color="#e84d60", legend=value("2017"))

    plot2.x_range.range_padding = 0.1
    plot2.xgrid.grid_line_color = None
    plot2.legend.location = "top_left"
    plot2.legend.orientation = "horizontal"
    plot2.sizing_mode = 'scale_width'

    # Summary of plots
    plots = {
        'User Discount Per Year': plot1,
        'Annual Compound Annual Growth Rate': plot2,
    }

    script, div = components(plots)

    context = {
        'bokehjs': script,
        'bokehdiv': div,
    }

    return render(request, 'web/bulma_index.html', context=context)
