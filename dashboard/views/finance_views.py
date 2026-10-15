"""
RetailMart V3 - Finance Domain Views
Handles request routing, filter parsing, and context assembling for Finance analytics:
- Top-line delivered revenue, AOV, and orders
- Corporate and store operating expenses
- Product category gross margins
- Treasury liquidity, payment modes, and refund impacts
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services import finance_service


@login_required
def finance_dashboard_view(request):
    """Finance & Treasury Analytics Controller (/business-dashboard/finance/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))

    kpis = finance_service.get_finance_kpi_summary(filters)
    rev_exp_trend = finance_service.get_monthly_revenue_vs_expense_trend(filters)
    corp_expenses = finance_service.get_corporate_expenses_breakdown(filters)
    store_expenses = finance_service.get_store_expenses_breakdown(filters)
    category_margins = finance_service.get_product_category_margins(filters)
    treasury = finance_service.get_treasury_cash_distribution(filters)
    payment_tenders = finance_service.get_payment_tender_performance(filters)
    refund_impact = finance_service.get_refund_financial_impact(filters)
    regional_performance = finance_service.get_regional_financial_performance(filters)

    context = {
        'page_title': 'Financial Performance & Treasury Intelligence',
        'active_tab': 'finance',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': kpis,
        'rev_exp_trend': rev_exp_trend,
        'corp_expenses': corp_expenses,
        'store_expenses': store_expenses,
        'category_margins': category_margins,
        'treasury': treasury,
        'payment_tenders': payment_tenders,
        'refund_impact': refund_impact,
        'regional_performance': regional_performance,
    }
    return render(request, 'dashboard/finance.html', context)
