from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services.logistics_service import (
    get_logistics_kpis,
    get_courier_sla_breakdown,
    get_delivery_lead_time_distribution,
    get_warehouse_utilization,
    get_inbound_shipments_status,
    get_category_stockout_risks,
)


@login_required
def logistics_dashboard_view(request):
    """Logistics Dashboard Controller (/business-dashboard/logistics/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))
    
    kpis = get_logistics_kpis(filters)
    courier_sla = get_courier_sla_breakdown(filters)
    lead_time_dist = get_delivery_lead_time_distribution(filters)
    warehouses = get_warehouse_utilization(filters)
    inbound_status = get_inbound_shipments_status(filters)
    category_risks = get_category_stockout_risks()

    context = {
        'page_title': 'Logistics Dashboard',
        'active_tab': 'logistics',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': kpis,
        'courier_sla': courier_sla,
        'lead_time_dist': lead_time_dist,
        'warehouses': warehouses,
        'inbound_status': inbound_status,
        'category_risks': category_risks,
    }
    return render(request, 'dashboard/logistics.html', context)
