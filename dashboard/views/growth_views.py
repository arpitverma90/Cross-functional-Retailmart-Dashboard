from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.growth_logistics_service import (
    get_marketing_dashboard_data,
    get_digital_dashboard_data,
    get_logistics_dashboard_data
)
from dashboard.services.filter_service import get_filter_options


@login_required
def marketing_view(request):
    """Marketing campaigns, platform ad spend, and email engagement analytics."""
    data = get_marketing_dashboard_data()
    filter_options = get_filter_options()
    
    context = {
        'page_title': 'Marketing Analytics Dashboard',
        'active_tab': 'marketing',
        'active_suite': 'growth',
        'data': data,
        'filter_options': filter_options
    }
    return render(request, 'dashboard/marketing.html', context)


@login_required
def digital_view(request):
    """Digital traffic, session page views, devices, and web events funnel."""
    data = get_digital_dashboard_data()
    filter_options = get_filter_options()
    
    context = {
        'page_title': 'Digital Web Events Dashboard',
        'active_tab': 'digital',
        'active_suite': 'growth',
        'data': data,
        'filter_options': filter_options
    }
    return render(request, 'dashboard/digital.html', context)


@login_required
def logistics_view(request):
    """Logistics, courier SLA performance, transit lead times, and warehouse capacity."""
    data = get_logistics_dashboard_data()
    filter_options = get_filter_options()
    
    context = {
        'page_title': 'Logistics & Supply Chain Dashboard',
        'active_tab': 'logistics',
        'active_suite': 'growth',
        'data': data,
        'filter_options': filter_options
    }
    return render(request, 'dashboard/logistics.html', context)
