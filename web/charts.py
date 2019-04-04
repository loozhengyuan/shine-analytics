import math
import itertools
import collections
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.palettes import all_palettes
from bokeh.transform import dodge, factor_cmap
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from django.db.models import Sum, Count, F, Q
from web.models import *

# Globals
tools = "pan,wheel_zoom,box_zoom,reset,save"

def top_ten_accounts_receivables_balance_by_customer():
    """Returns plot for the top ten accounts receivables balance by customer"""

    # Queryset
    query = (
        Transaction
        .objects
        .values('project__custaccount__customer__name')
        .annotate(inflow=Sum('converted_amount', filter=Q(document__reference__startswith='I')), outflow=Sum('converted_amount', filter=Q(document__reference__startswith='B')), variance=F('inflow')+F('outflow'), transactions=Count('converted_amount', filter=Q(document__reference__startswith='I')))
        .exclude(variance__isnull=True)
        .order_by('-variance')[:10]
    )

    # Creating lists from Queryset
    customers = [i['project__custaccount__customer__name'] for i in query]
    custshort = ["".join([word[:1] for word in customer.split(' ')]) for customer in customers]
    transactions = [i['transactions'] for i in query]
    inflow = [i['inflow'] for i in query]
    outflow = [i['outflow'] for i in query]
    variance = [i['variance'] for i in query]

    # Create ColumnDataSource
    data = dict(
        customers=customers,
        custshort=custshort,
        variance=variance,
        inflow=inflow,
        outflow=outflow,
    )
    source = ColumnDataSource(data=data)

    # Create plot
    p = figure(
        title="Top 10 AR Balance by Customer",
        x_range=custshort,
        tools=tools,
        x_axis_label='customers',
        y_axis_label='net accounts receivables',
        tooltips=[
            ("Customer", "@customers"),
            ("Net Revenue", "@inflow{$0,0.00}"),
            ("Net Repayment", "@outflow{$0,0.00}"),
            ("Variance", "@variance{$0,0.00}"),
        ],
        height=320,
    )
    p.vbar(x='custshort', top='variance', width=0.9, source=source, fill_color='green', fill_alpha=0.3, line_color='white')
    p.xgrid.grid_line_color = None
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def bottom_ten_accounts_receivables_balance_by_customer():
    """Returns plot for the bottom ten accounts receivables balance by customer"""

    # Queryset
    query = (
        Transaction
        .objects
        .values('project__custaccount__customer__name')
        .annotate(inflow=Sum('converted_amount', filter=Q(document__reference__startswith='I')), outflow=Sum('converted_amount', filter=Q(document__reference__startswith='B')), variance=F('inflow')+F('outflow'), transactions=Count('converted_amount', filter=Q(document__reference__startswith='I')))
        .exclude(variance__isnull=True)
        .order_by('variance')[:10]
    )

    # Creating lists from Queryset
    customers = [i['project__custaccount__customer__name'] for i in query]
    custshort = ["".join([word[:1] for word in customer.split(' ')]) for customer in customers]
    transactions = [i['transactions'] for i in query]
    inflow = [i['inflow'] for i in query]
    outflow = [i['outflow'] for i in query]
    variance = [i['variance'] for i in query]

    # Create ColumnDataSource
    data = dict(
        customers=customers,
        custshort=custshort,
        variance=variance,
        inflow=inflow,
        outflow=outflow,
    )
    source = ColumnDataSource(data=data)

    # Create plot
    p = figure(
        title="Bottom 10 AR Balance by Customer",
        x_range=custshort,
        tools=tools,
        x_axis_label='customers',
        y_axis_label='net accounts receivables',
        tooltips=[
            ("Customer", "@customers"),
            ("Net Revenue", "@inflow{$0,0.00}"),
            ("Net Repayment", "@outflow{$0,0.00}"),
            ("Variance", "@variance{$0,0.00}"),
        ],
        height=320,
    )
    p.vbar(x='custshort', top='variance', width=0.9, source=source, fill_color='red', fill_alpha=0.3, line_color='white')
    p.xgrid.grid_line_color = None
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def income_by_location():
    """Returns plot for income by location"""

    # Queryset
    query = (
        Transaction
        .objects
        .filter(document__reference__startswith='I')
        .annotate(year=TruncYear('document__date'))
        .values('year', 'location__code')
        .annotate(total=Sum('converted_amount'))
        .order_by('-year')
    )

    # Creating lists from Queryset
    locations = list(collections.OrderedDict.fromkeys([i['location__code'] for i in query]))
    years = list(collections.OrderedDict.fromkeys([i['year'].strftime("%Y") for i in query]))
    revenue = {year: [i['total'] for i in query if i['year'].strftime("%Y") == year] for year in years}

    # Create ColumnDataSource
    data = dict(
        locations=locations,
        **revenue,
    )
    source = ColumnDataSource(data=data)

    # Create plot
    p = figure(
        title="Revenue By Location Per Year",
        x_range=locations,
        tools=tools,
        x_axis_label='locations',
        y_axis_label='total revenue',
        tooltips=[
            ("Location", "@locations"),
            ("Year", "$name"),
            ("Revenue", "@$name{$0,0.00}"),
        ],
        height=320,
    )

    p.vbar_stack(years, x='locations', width=0.9, color=all_palettes['Category20c'][len(years)], source=source, legend=[value(x) for x in years])
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def income_by_project_per_year():
    """Returns plot for income by project"""

    # Queryset
    query = (
        Transaction
        .objects
        .filter(document__reference__startswith='I')
        .annotate(month=TruncMonth('document__date'))
        .values('month', 'project__code')
        .annotate(total=Sum('converted_amount'))
        .order_by()
    )

    # Creating lists from Queryset
    projects = [i['project__code'] for i in query]
    months = [i['month'] for i in query]
    revenue = [i['total'] for i in query]
    data = dict(
        projects=projects,
        months=months,
        revenue=revenue,
    )
    source = ColumnDataSource(data=data)
    

    p = figure(
        title="Revenue By Projects Per Month",
        tools=tools,
        x_axis_type='datetime',
        x_axis_label='month/year',
        y_axis_label='total revenue',
        tooltips=[
            ("Month", "@months"),
            ("Project", "@projects"),
            ("Revenue", "@revenue{$0,0.00}"),
        ],
        height=320,
    )

    p.circle(x='months', y='revenue', radius=1000000000, fill_alpha=0.3, source=source)
    p.xgrid.grid_line_color = None
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def revenue_by_salesperson_per_year():
    """Returns plot for revenue by salesperson per year"""
    
    # Queryset
    query = (
        Transaction
        .objects
        .filter(document__reference__startswith='I')
        .annotate(year=TruncYear('document__date'))
        .values('year', 'project__salesperson__name')
        .annotate(total=Sum('converted_amount'))
        .order_by('-year')
    )

    # Creating lists from Queryset
    salespersons = list(collections.OrderedDict.fromkeys([i['project__salesperson__name'] for i in query]))
    years = list(collections.OrderedDict.fromkeys([i['year'].strftime("%Y") for i in query]))
    revenue = {year: [i['total'] for i in query if i['year'].strftime("%Y") == year] for year in years}

    # Create ColumnDataSource
    data = dict(
        salespersons=salespersons,
        **revenue,
    )
    source = ColumnDataSource(data=data)

    # Create plot
    p = figure(
        title="Revenue By Salesperson Per Year",
        x_range=salespersons,
        tools=tools,
        x_axis_label='salespersons',
        y_axis_label='total revenue',
        tooltips=[
            ("Salesperson", "@salespersons"),
            ("Year", "$name"),
            ("Revenue", "@$name{$0,0.00}"),
        ],
        height=320,
    )

    p.vbar_stack(years, x='salespersons', width=0.9, color=all_palettes['Category20c'][len(years)], source=source, legend=[value(x) for x in years])
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')

    return p

def accounts_receivables_ratio_by_month():
    """Returns plot for the cumulative net accounts receivables balance by month"""

    # Queryset
    query = (
        Transaction
        .objects
        .annotate(month=TruncMonth('document__date'))
        .values('month')
        .annotate(inflow=Sum('converted_amount', filter=Q(document__reference__startswith='I')), outflow=Sum('converted_amount', filter=Q(document__reference__startswith='B')), variance=F('inflow')+F('outflow'))
        .exclude(variance__isnull=True)
        .order_by('month')
    )

    # Creating lists from Queryset
    month = [i['month'].strftime("%b '%y") for i in query]
    inflow = [i['inflow'] for i in query]
    variance = [i['variance'] for i in query]
    cumvar = [i for i in itertools.accumulate(variance)]
    varratio = [v/i for v, i in zip(variance, inflow)]
    cumvarratio = [c/i for c, i in zip(cumvar, inflow)]


    # Create ColumnDataSource
    data = dict(
        month=month,
        variance=variance,
        cumvar=cumvar,
        varratio=varratio,
        cumvarratio=cumvarratio,
    )
    source = ColumnDataSource(data=data)

    # Create plot
    p = figure(
        title="Accounts Receivables Ratio by Month",
        x_range=month,
        tools=tools,
        x_axis_label='month/year',
        y_axis_label='net accounts receivables',
        tooltips=[
            ("Month", "@month"),
            ("Variance", "@variance{$0,0.00}"),
            ("Cumulative Variance", "@cumvar{$0,0.00}"),
            ("AR Ratio", "@varratio{0.000}"),
            ("Cum. AR Ratio", "@cumvarratio{0.000}"),
        ],
        height=320,
    )
    p.line(x='month', y='varratio', source=source, legend="discrete", line_width=2, line_color="indigo")
    p.circle(x='month', y='varratio', source=source, legend="discrete", fill_color=None, line_color="indigo")
    p.line(x='month', y='cumvarratio', source=source, legend="cumulative", line_width=2, line_color="tomato")
    p.circle(x='month', y='cumvarratio', source=source, legend="cumulative", fill_color=None, line_color="tomato")
    p.xgrid.grid_line_color = None
    p.sizing_mode = 'scale_width'
    p.legend.location = "top_left"
    p.xaxis.major_label_orientation = math.pi/3

    return p

def accounts_receivables_balance_by_month():
    """Returns plot for the cumulative net accounts receivables balance by month"""

    # Queryset
    query = (
        Transaction
        .objects
        .annotate(month=TruncMonth('document__date'))
        .values('month')
        .annotate(inflow=Sum('converted_amount', filter=Q(document__reference__startswith='I')), outflow=Sum('converted_amount', filter=Q(document__reference__startswith='B')), variance=F('inflow')+F('outflow'))
        .exclude(variance__isnull=True)
        .order_by('month')
    )

    # Creating lists from Queryset
    month = [i['month'].strftime("%b '%y") for i in query]
    variance = [i['variance'] for i in query]
    cumvar = [i for i in itertools.accumulate(variance)]

    # Create ColumnDataSource
    data = dict(
        month=month,
        variance=variance,
        cumvar=cumvar,
    )
    source = ColumnDataSource(data=data)

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
            ("Cumulative Variance", "@cumvar{$0,0.00}"),
        ],
        height=320,
    )
    p.line(x='month', y='variance', source=source, legend="discrete", line_width=2, line_color="indigo")
    p.circle(x='month', y='variance', source=source, legend="discrete", fill_color=None, line_color="indigo")
    p.line(x='month', y='cumvar', source=source, legend="cumulative", line_width=2, line_color="tomato")
    p.circle(x='month', y='cumvar', source=source, legend="cumulative", fill_color=None, line_color="tomato")
    p.xgrid.grid_line_color = None
    p.sizing_mode = 'scale_width'
    p.legend.location = "top_left"
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')
    p.xaxis.major_label_orientation = math.pi/3

    return p

def top_ten_customer_revenue_contribution_of_all_time():
    """Returns plot for top ten customer revenue contribution of all-time"""
    
    # Queryset
    query = (
        Transaction
        .objects
        .filter(document__reference__startswith='I')
        .values('project__custaccount__customer__name')
        .annotate(total=Sum('converted_amount'))
        .order_by('-total')[:10]
    )

    # Creating lists from Queryset
    customers = [i['project__custaccount__customer__name'] for i in query]
    custshort = ["".join([word[:1] for word in customer.split(' ')]) for customer in customers]
    revenue = [round(i['total'], 2) for i in query]

    # Create ColumnDataSource
    data = dict(
        customers=customers,
        custshort=custshort,
        revenue=revenue,
    )
    source = ColumnDataSource(data=data)

    # Create plot
    p = figure(
        title="Top 10 Customer Revenue Contribution of All-Time",
        x_range=custshort,
        tools=tools,
        x_axis_label='customer',
        y_axis_label='total revenue',
        tooltips=[
            ("Customer Name", "@customers"),
            ("Total Revenue", "@revenue{$0,0.00}"),
        ],
        height=320,
    )
    p.vbar(x='custshort', top='revenue', width=0.9, source=source, line_color='white', fill_color=factor_cmap('customers', palette=all_palettes['Spectral'][10], factors=customers))
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
        .values('project__custaccount__customer__name')
        .annotate(total=Sum('converted_amount'))
        .order_by('-total')[:10]
    )

    # Creating lists from Queryset
    customers = [i['project__custaccount__customer__name'] for i in query]
    custshort = ["".join([word[:1] for word in customer.split(' ')]) for customer in customers]
    revenue = [round(i['total'], 2) for i in query]
    
    # Create ColumnDataSource
    data = dict(
        customers=customers,
        custshort=custshort,
        revenue=revenue,
    )
    source = ColumnDataSource(data=data)

    # Create plot
    p = figure(
        title="Top 10 Customer Revenue Contribution In The Last 12 Months",
        x_range=custshort,
        tools=tools,
        x_axis_label='customer',
        y_axis_label='total revenue',
        tooltips=[
            ("Customer Name", "@customers"),
            ("Total Revenue", "@revenue{$0,0.00}"),
        ],
        height=320,
    )
    p.vbar(x='custshort', top='revenue', width=0.9, source=source, line_color='white', fill_color=factor_cmap('customers', palette=all_palettes['Spectral'][10], factors=customers))
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

    # Creating lists from Queryset
    quarter = [i['quarter'].strftime("%b '%y") for i in query]
    total = [round(i['total'], 2) for i in query]
    
    # Create ColumnDataSource
    data = dict(
        quarter=quarter,
        total=total,
    )
    source = ColumnDataSource(data=data)
    
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

    # Creating lists from Queryset
    month = [i['month'].strftime("%b '%y") for i in query]
    total = [round(i['total'], 2) for i in query]
    
    # Create ColumnDataSource
    data = dict(
        month=month,
        total=total,
    )
    source = ColumnDataSource(data=data)

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
        height=320,
    )
    p.vbar(x='month', top='total', width=0.9, source=source)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.sizing_mode = 'scale_width'
    p.yaxis.formatter = NumeralTickFormatter(format='$0a')
    p.xaxis.major_label_orientation = math.pi/3

    return p