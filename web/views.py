import inspect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bokeh.embed import components
from web.charts import *

# Create your views here.
@login_required(login_url='web:login')
def index(request):

    # Define plots
    plots = {
        'plot1': accounts_receivables_balance_by_month(),
        'plot2': accounts_receivables_turnover_by_month(),
        'plot3': top_ten_customer_revenue_contribution_last_twelve_months(),
        'plot4': top_ten_customer_revenue_contribution_of_all_time(),
        'plot5': total_income_by_month(),
        'plot6': total_projects_by_quarter(),
        'plot7': top_ten_accounts_receivables_balance_by_customer(),
        'plot8': bottom_ten_accounts_receivables_balance_by_customer(),
        'plot9': revenue_by_salesperson_per_year(),
        'plot10': income_by_location(),
        'plot11': income_by_project_per_year(),
    }

    # Create components
    script, div = components(plots)

    # Create containers and headers
    divlist = [
        {
            "plot1": div['plot1'],
            "plot2": div['plot2'],
        },
        {
            "plot3": div['plot3'],
            "plot4": div['plot4'],
        },
        {
            "plot5": div['plot5'],
            "plot6": div['plot6'],
        },
        {
            "plot7": div['plot7'],
            "plot8": div['plot8'],
        },
        {
            "plot9": div['plot9'],
            "plot10": div['plot10'],
        },
        {
            "plot11": div['plot11'],
            "asdas": "",
        },
    ]

    # Append to context
    context = {
        'bokehjs': script,
        'bokehdiv': divlist,
    }

    return render(request, 'web/bulma_index.html', context=context)
