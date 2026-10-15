"""
RetailMart V3 - Commercial & Customer Operations Domain Views
Handles request routing, filter parsing, and context assembling for:
- Sales: Revenue velocity, Gross vs Net, Category Pareto & Margins, Top Brands, Top Stores
- Customers: RFM segmentation distribution, loyalty tiers, repeat purchase cohorts
- Operations: Store inventory health, stockout risks, manufacturing work orders & scrap rates
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services import commercial_service


@login_required
def sales_dashboard_view(request):
    """Commercial Sales & Revenue Analytics Controller (/business-dashboard/sales/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))

    data = commercial_service.get_sales_dashboard_data(filters)

    # Format data for charts
    monthly_trend_json = json.dumps([
        {
            'month': r['sales_month'].strftime('%b %Y') if hasattr(r['sales_month'], 'strftime') else str(r['sales_month']),
            'orders': int(r['delivered_orders'] or 0),
            'revenue': float(r['net_revenue'] or 0),
            'mom_pct': float(r['mom_growth_pct'] or 0)
        }
        for r in data['monthly_trend']
    ])

    category_mix_json = json.dumps([
        {
            'category': r['category_name'],
            'revenue': float(r['net_revenue'] or 0),
            'margin_pct': float(r['gross_margin_pct'] or 0),
            'units': int(r['total_units_sold'] or 0)
        }
        for r in data['categories']
    ])

    context = {
        'page_title': 'Commercial Sales & Revenue Intelligence',
        'active_tab': 'sales',
        'active_suite': 'commercial',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': data['kpis'],
        'monthly_trend': data['monthly_trend'],
        'categories': data['categories'],
        'brands': data['brands'],
        'stores': data['stores'],
        'monthly_trend_json': monthly_trend_json,
        'category_mix_json': category_mix_json,
    }
    return render(request, 'dashboard/sales.html', context)


@login_required
def customer_dashboard_view(request):
    """Customer RFM Intelligence & Retention Controller (/business-dashboard/customers/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))

    data = commercial_service.get_customer_dashboard_data(filters)

    rfm_json = json.dumps([
        {
            'segment': r['rfm_segment'],
            'count': int(r['customer_count'] or 0),
            'share_pct': float(r['customer_share_pct'] or 0),
            'spend': float(r['total_spend'] or 0),
            'avg_recency': float(r['avg_recency_days'] or 0)
        }
        for r in data['rfm_segments']
    ])

    tier_json = json.dumps([
        {
            'tier': r['tier'],
            'members': int(r['total_members'] or 0),
            'active': int(r['active_purchasers'] or 0),
            'spend': float(r['total_tier_spend'] or 0),
            'aov': float(r['aov'] or 0)
        }
        for r in data['tiers']
    ])

    context = {
        'page_title': 'Customer RFM Intelligence & Retention',
        'active_tab': 'customers',
        'active_suite': 'commercial',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': data['kpis'],
        'rfm_segments': data['rfm_segments'],
        'tiers': data['tiers'],
        'repeat_cohorts': data['repeat_cohorts'],
        'rfm_json': rfm_json,
        'tier_json': tier_json,
    }
    return render(request, 'dashboard/customers.html', context)


@login_required
def operations_dashboard_view(request):
    """Store Inventory & Manufacturing Quality Controller (/business-dashboard/operations/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))

    data = commercial_service.get_operations_dashboard_data(filters)

    health_json = json.dumps([
        {
            'status': r['stock_health_status'],
            'slots': int(r['inventory_slot_count'] or 0),
            'share_pct': float(r['percentage_share'] or 0),
            'units': int(r['total_units_on_hand'] or 0)
        }
        for r in data['health']
    ])

    regional_json = json.dumps([
        {
            'region': r['region_name'],
            'stores': int(r['active_stores'] or 0),
            'oos': int(r['out_of_stock_count'] or 0),
            'low_stock': int(r['low_stock_count'] or 0),
            'risk_pct': float(r['regional_at_risk_pct'] or 0)
        }
        for r in data['regional_risk']
    ])

    line_json = json.dumps([
        {
            'line': r['line_name'],
            'produced': int(r.get('total_units_produced') or 0),
            'rejected': int(r.get('total_units_rejected') or r.get('total_rejected_units') or 0),
            'scrap_pct': float(r.get('scrap_rate_pct') or 0)
        }
        for r in data['lines']
    ])

    context = {
        'page_title': 'Operations, Inventory & Manufacturing Quality',
        'active_tab': 'operations',
        'active_suite': 'commercial',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': data['kpis'],
        'health': data['health'],
        'regional_risk': data['regional_risk'],
        'lines': data['lines'],
        'health_json': health_json,
        'regional_json': regional_json,
        'line_json': line_json,
    }
    return render(request, 'dashboard/operations.html', context)
