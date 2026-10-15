from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.customer_service import get_customer_dashboard_data

@login_required
def customer_dashboard_view(request):
    """Detailed Customer Dashboard Controller (/business-dashboard/customers/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    data = get_customer_dashboard_data(filters)
    
    context = {
        'page_title': 'Customer Intelligence',
        'active_tab': 'customers',
        'filters': filters,
        'filter_options': filter_options,
        'data': data
    }
    return render(request, 'dashboard/customers.html', context)
