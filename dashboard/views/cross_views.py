from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.cross_functional_service import get_cross_functional_dashboard_data
from dashboard.services.simulator_service import get_simulator_baseline

@login_required
def cross_functional_dashboard_view(request):
    """Detailed Cross-Functional Dashboard Controller (/business-dashboard/cross-functional/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    data = get_cross_functional_dashboard_data(filters)
    simulator_baseline = get_simulator_baseline()
    
    context = {
        'page_title': 'Cross-Functional Insights',
        'active_tab': 'cross_functional',
        'filters': filters,
        'filter_options': filter_options,
        'data': data,
        'simulator_baseline': simulator_baseline
    }
    return render(request, 'dashboard/cross_functional.html', context)


@login_required
def simulator_view(request):
    """Scenario Simulator Dedicated Page (/business-dashboard/simulator/)"""
    baseline = get_simulator_baseline()
    context = {
        'page_title': 'Contribution Margin Scenario Simulator',
        'active_tab': 'simulator',
        'baseline': baseline
    }
    return render(request, 'dashboard/simulator.html', context)
