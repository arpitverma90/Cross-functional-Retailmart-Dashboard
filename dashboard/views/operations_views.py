from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.operations_service import get_operations_dashboard_data

@login_required
def operations_dashboard_view(request):
    """Detailed Operations Dashboard Controller (/business-dashboard/operations/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    data = get_operations_dashboard_data(filters)
    
    context = {
        'page_title': 'Operations & Logistics',
        'active_tab': 'operations',
        'filters': filters,
        'filter_options': filter_options,
        'data': data
    }
    return render(request, 'dashboard/operations.html', context)
