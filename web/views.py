import inspect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bokeh.embed import components
from web.charts import *

# Create your views here.
@login_required(login_url='web:login')
def index(request):
    
    # Check user group
    if request.user.groups.filter(name__in=['CHIEF EXECUTIVES']).exists():
       
        # Define plots
        plots = {
            'plot1': total_income_by_month(),
            'plot2': total_projects_by_quarter(),
            'plot3': top_ten_customer_revenue_contribution_of_all_time(),
            'plot4': top_ten_customer_revenue_contribution_last_twelve_months(),
            'plot5': income_by_location(),
            'plot6': revenue_by_salesperson_per_year(),
            'plot7': accounts_receivables_balance_by_month(),
            'plot8': accounts_receivables_turnover_by_month(),
            'plot9': top_ten_accounts_receivables_balance_by_customer(),
            'plot10': income_by_project_per_year(),
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
        ]

        # Append to context
        context = {
            'bokehjs': script,
            'bokehdiv': divlist,
        }

        return render(request, 'web/bulma_index.html', context=context)
    
    elif request.user.groups.filter(name__in=['FINANCE DEPARTMENT']).exists():
        
        # Define plots
        plots = {
            'plot1': accounts_receivables_balance_by_month(),
            'plot2': accounts_receivables_turnover_by_month(),
            'plot3': top_ten_accounts_receivables_balance_by_customer(),
            'plot4': income_by_project_per_year(),
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
        ]

        # Append to context
        context = {
            'bokehjs': script,
            'bokehdiv': divlist,
        }

        return render(request, 'web/bulma_index.html', context=context)

    elif request.user.groups.filter(name__in=['CUSTOMER SERVICE DEPARTMENT']).exists():
        
        # Define plots
        plots = {
            'plot1': income_by_location(),
            'plot2': revenue_by_salesperson_per_year(),
            'plot3': top_ten_customer_revenue_contribution_of_all_time(),
            'plot4': top_ten_customer_revenue_contribution_last_twelve_months(),
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
        ]

        # Append to context
        context = {
            'bokehjs': script,
            'bokehdiv': divlist,
        }

        return render(request, 'web/bulma_index.html', context=context)

    else:

        # Return empty page if not authorised
        return render(request, 'web/bulma_index.html')
