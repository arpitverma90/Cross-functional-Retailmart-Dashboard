from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.marketing_service import (
    get_marketing_kpis,
    get_spend_by_platform,
    get_monthly_spend_trend,
    get_top_campaigns,
    get_email_engagement_trend,
)


@login_required
def marketing_dashboard_view(request):
    """Marketing Dashboard Controller (/business-dashboard/marketing/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    
    kpis = get_marketing_kpis(filters)
    platform_spend = get_spend_by_platform(filters)
    spend_trend = get_monthly_spend_trend(filters)
    top_campaigns = get_top_campaigns(filters, limit=10)
    email_trend = get_email_engagement_trend(filters)

    context = {
        'page_title': 'Marketing Dashboard',
        'active_tab': 'marketing',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': kpis,
        'platform_spend': platform_spend,
        'spend_trend': spend_trend,
        'top_campaigns': top_campaigns,
        'email_trend': email_trend,
    }
    return render(request, 'dashboard/marketing.html', context)
