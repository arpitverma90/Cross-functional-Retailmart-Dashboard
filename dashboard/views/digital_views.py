from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.digital_service import (
    get_digital_kpis,
    get_device_os_mix,
    get_web_traffic_trend,
    get_digital_funnel,
    get_top_landing_pages,
    get_event_interactions,
)


@login_required
def digital_dashboard_view(request):
    """Digital Dashboard Controller (/business-dashboard/digital/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    
    kpis = get_digital_kpis(filters)
    device_os = get_device_os_mix(filters)
    traffic_trend = get_web_traffic_trend(filters)
    funnel = get_digital_funnel(filters)
    top_pages = get_top_landing_pages(filters, limit=10)
    events = get_event_interactions(filters)

    context = {
        'page_title': 'Digital Dashboard',
        'active_tab': 'digital',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': kpis,
        'device_os': device_os,
        'traffic_trend': traffic_trend,
        'funnel': funnel,
        'top_pages': top_pages,
        'events': events,
    }
    return render(request, 'dashboard/digital.html', context)
