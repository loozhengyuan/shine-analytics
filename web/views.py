from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bokeh.embed import components
from web.charts import *

# Create your views here.
@login_required(login_url='web:login')
def index(request):

    # Define plots
    plots = {
        'plot1': top_ten_customer_revenue_contribution_of_all_time(),
        'plot2': top_ten_customer_revenue_contribution_last_twelve_months(),
        'plot3': accounts_receivables_balance_by_month(),
        'plot4': total_income_by_month(),
        'plot5': total_projects_by_quarter(),
    }

    # Create components
    script, div = components(plots)

    # Create containers and headers
    divlist = [
        {
            "Top 10 Customer Revenue Contribution of All Time": div['plot1'],
            "Top 10 Customer Revenue Contribution in the Last 12 Months": div['plot2'],
        },
        {
            "Accounts Receivales Balance by Month": div['plot3'],
            "Total Projects by Quarter": div['plot5'],
        },
        {
            "Total Income by Month": div['plot4'],
        },
    ]

    # Append to context
    context = {
        'bokehjs': script,
        'bokehdiv': divlist,
    }

    return render(request, 'web/bulma_index.html', context=context)
