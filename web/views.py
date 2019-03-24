from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bokeh.embed import components
from web.charts import *

# Create your views here.
@login_required(login_url='web:login')
def index(request):

    # Define plots
    plots = {
        'User Discount Per Year': test_plot1(),
        'Annual Compound Annual Growth Rate': test_plot2(),
    }

    # Create components and embed to context
    script, div = components(plots)
    context = {
        'bokehjs': script,
        'bokehdiv': div,
    }

    return render(request, 'web/bulma_index.html', context=context)
