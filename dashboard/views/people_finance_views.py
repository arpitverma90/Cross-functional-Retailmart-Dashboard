from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.people_finance_service import (
    get_hr_dashboard_data,
    get_finance_dashboard_data
)
from dashboard.services.filter_service import get_filter_options


@login_required
def hr_view(request):
    """HR workforce metrics, departmental headcount, roles, and labor productivity."""
    data = get_hr_dashboard_data()
    filter_options = get_filter_options()
    
    context = {
        'page_title': 'HR & Workforce Analytics Dashboard',
        'active_tab': 'hr',
        'active_suite': 'people_finance',
        'data': data,
        'filter_options': filter_options
    }
    return render(request, 'dashboard/hr.html', context)


@login_required
def finance_view(request):
    """Financial waterfall, store operating expenses, enterprise ledger, and accounts."""
    data = get_finance_dashboard_data()
    filter_options = get_filter_options()
    
    context = {
        'page_title': 'Finance & Operating Ledger Dashboard',
        'active_tab': 'finance',
        'active_suite': 'people_finance',
        'data': data,
        'filter_options': filter_options
    }
    return render(request, 'dashboard/finance.html', context)
