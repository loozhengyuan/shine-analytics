import math
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.palettes import Spectral10
from bokeh.transform import dodge, factor_cmap
from django.db.models.functions import TruncMonth, TruncQuarter
from django.db.models import Sum, Count, F, Q
from web.models import *

# Globals
tools = "pan,wheel_zoom,box_zoom,reset,save"

# Plot 1
def test_plot1():
    p = figure(tools=tools)
    p.circle([1, 2], [3, 4])
    p.sizing_mode = 'scale_width'
    return p

def accounts_receivables_balance_by_month():
    """Returns plot for the accounts receivables balance by month"""

    # Queryset
    query = (
        Transaction
        .objects
        .annotate(month=TruncMonth('document__date'))
        .values('month')
        .annotate(inflow=Sum('converted_amount', filter=Q(document__reference__startswith='I')), outflow=Sum('converted_amount', filter=Q(document__reference__startswith='B')))
        .annotate(variance=F('inflow')+F('outflow'))
        .order_by('month')
    )

    # Axis data
    month = [i['month'].strftime("%b '%y") for i in query]
    variance = [i['variance'] for i in query]
    source = ColumnDataSource(data=dict(month=month, variance=variance))

    # Create plot
    p = figure(
        title="Accounts Receivables Balance by Month",
        x_range=month,
        tools=tools,
        x_axis_label='month/year',
        y_axis_label='net accounts receivables',
        tooltips=[
            ("Month", "@month"),
            ("Variance", "@variance{$0,0.00}"),
        ],
        height=320,
    )
    p.vbar(x='month', top='variance', width=0.9, source=source)
    p.xgrid.grid_line_color = None
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def top_ten_customer_revenue_contribution_of_all_time():
    """Returns plot for top ten customer revenue contribution of all-time"""
    
    # Queryset
    query = (
        Transaction
        .objects
        .filter(document__reference__startswith='I')
        .values('customer__name')
        .annotate(total=Sum('converted_amount'))
        .order_by('-total')[:10]
    )

    # Data source
    customer = [i['customer__name'] for i in query]
    revenue = [round(i['total'], 2) for i in query]
    source = ColumnDataSource(data=dict(customer=customer, revenue=revenue))

    # Create plot
    p = figure(
        title="Top 10 Customer Revenue Contribution of All-Time",
        x_range=customer,
        tools=tools,
        x_axis_label='customer',
        y_axis_label='total revenue',
        tooltips=[
            ("Customer Name", "@customer"),
            ("Total Revenue", "@revenue{$0,0.00}"),
        ],
        height=320,
    )
    p.vbar(x='customer', top='revenue', width=0.9, source=source, line_color='white', fill_color=factor_cmap('customer', palette=Spectral10, factors=customer))
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def top_ten_customer_revenue_contribution_last_twelve_months():
    """Returns plot for top ten customer revenue contribution in the last twelve months"""

    # Queryset
    latest = Transaction.objects.order_by('document__date').last()
    query = (
        Transaction
        .objects
        .filter(document__reference__startswith='I', document__date__range=(latest.document.date - relativedelta(years=1), latest.document.date))
        .values('customer__name')
        .annotate(total=Sum('converted_amount'))
        .order_by('-total')[:10]
    )

    # Data source
    customer = [i['customer__name'] for i in query]
    revenue = [round(i['total'], 2) for i in query]
    source = ColumnDataSource(data=dict(customer=customer, revenue=revenue))

    # Create plot
    p = figure(
        title="Top 10 Customer Revenue Contribution In The Last 12 Months",
        x_range=customer,
        tools=tools,
        x_axis_label='customer',
        y_axis_label='total revenue',
        tooltips=[
            ("Customer Name", "@customer"),
            ("Total Revenue", "@revenue{$0,0.00}"),
        ],
        height=320,
    )
    p.vbar(x='customer', top='revenue', width=0.9, source=source, line_color='white', fill_color=factor_cmap('customer', palette=Spectral10, factors=customer))
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def total_projects_by_quarter():
    """Returns plot for the total projects by quarter"""

    # Queryset
    query = (
        Transaction
        .objects
        .annotate(quarter=TruncQuarter('document__date'))
        .values('quarter')
        .annotate(total=Count('project_id'))
        .order_by()
    )

    # Data source
    quarter = [i['quarter'].strftime("%b '%y") for i in query]
    total = [round(i['total'], 2) for i in query]
    source = ColumnDataSource(data=dict(quarter=quarter, total=total))
    
    # Create plot
    p = figure(
        title="Total Projects by Quarter",
        x_range=quarter,
        tools=tools,
        x_axis_label='quarter',
        y_axis_label='total projects',
        tooltips=[
            ("Quarter", "@quarter"),
            ("Projects", "@total"),
        ],
        height=320,
    )
    p.vbar(x='quarter', top='total', width=0.9, source=source)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.sizing_mode = 'scale_width'
    p.xaxis.major_label_orientation = math.pi/3

    return p

def total_income_by_month():
    """Returns plot for the total income by month"""

    # Queryset
    query = (
        Transaction
        .objects
        .filter(document__reference__startswith='I')
        .annotate(month=TruncMonth('document__date'))
        .values('month')
        .annotate(total=Sum('converted_amount'))
        .order_by()
    )

    # Axis data
    month = [i['month'].strftime("%b '%y") for i in query]
    total = [round(i['total'], 2) for i in query]
    source = ColumnDataSource(data=dict(month=month, total=total))

    # Create plot
    p = figure(
        title="Total Income by Month",
        x_range=month,
        tools=tools,
        x_axis_label='month/year',
        y_axis_label='income ($)',
        tooltips=[
            ("Month", "@month"),
            ("Total Income", "@total{$0,0.00}"),
        ],
        height=150,
    )
    p.vbar(x='month', top='total', width=0.9, source=source)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')
    p.xaxis.major_label_orientation = math.pi/3

    return p