from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.sales_service import get_sales_dashboard_data

@login_required
def sales_dashboard_view(request):
    """Detailed Sales Dashboard Controller (/business-dashboard/sales/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    data = get_sales_dashboard_data(filters)
    
    context = {
        'page_title': 'Sales Intelligence',
        'active_tab': 'sales',
        'filters': filters,
        'filter_options': filter_options,
        'data': data
    }
    return render(request, 'dashboard/sales.html', context)
