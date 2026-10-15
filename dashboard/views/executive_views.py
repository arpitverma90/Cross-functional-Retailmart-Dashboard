from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.executive_service import get_executive_summary_data

@login_required
def executive_summary_view(request):
    """Executive Summary Dashboard Controller (/executive-summary/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    data = get_executive_summary_data(filters)
    
    context = {
        'page_title': 'Executive Summary',
        'active_tab': 'executive',
        'filters': filters,
        'filter_options': filter_options,
        'data': data
    }
    return render(request, 'dashboard/executive_summary.html', context)
