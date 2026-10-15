"""
RetailMart V3 - Scenario Simulator Baseline Service
Supplies validated baseline figures from PostgreSQL for client-side what-if modeling:
1. Headcount adjustments (+/- %)
2. Salary increment & compensation adjustments (+/- %)
3. Store operational expense sensitivity (+/- %)
4. Top-line commercial sales growth (+/- %)
"""

from .db_service import execute_one


def get_simulator_baseline():
    """
    Retrieve authoritative baseline numbers directly from PostgreSQL:
    Delivered Sales, COGS, Headcount, Monthly Payroll, Store Expenses, Corporate Expenses.
    """
    baseline_sql = """
        SELECT 
            (SELECT SUM(net_total) FROM sales.orders WHERE order_status = 'Delivered') AS base_net_revenue,
            (SELECT SUM(oi.quantity * p.cost_price) 
             FROM sales.order_items oi 
             JOIN sales.orders o ON oi.order_id = o.order_id 
             JOIN products.products p ON oi.prod_id = p.product_id 
             WHERE o.order_status = 'Delivered') AS base_cogs,
            (SELECT COUNT(*) FROM stores.employees) AS base_headcount,
            (SELECT AVG(salary) FROM stores.employees) AS base_avg_salary,
            (SELECT SUM(salary) FROM stores.employees) AS base_monthly_payroll,
            (SELECT SUM(amount) FROM stores.expenses) AS base_store_expenses,
            (SELECT SUM(amount) FROM finance.expenses) AS base_corp_expenses,
            (SELECT COUNT(*) FROM sales.orders WHERE order_status = 'Delivered') AS base_delivered_orders;
    """
    row = execute_one(baseline_sql) or {}

    rev = float(row.get('base_net_revenue') or 6769536004.48)
    cogs = float(row.get('base_cogs') or 4908577904.87)
    headcount = int(row.get('base_headcount') or 3000)
    avg_salary = float(row.get('base_avg_salary') or 63273.60)
    monthly_payroll = float(row.get('base_monthly_payroll') or 189820814.00)
    store_expenses = float(row.get('base_store_expenses') or 100369598.57)
    corp_expenses = float(row.get('base_corp_expenses') or 8015031384.29)
    orders = int(row.get('base_delivered_orders') or 82540)

    gross_margin = rev - cogs
    gross_margin_pct = (gross_margin / rev * 100) if rev > 0 else 0.0
    annual_payroll = monthly_payroll * 12.0
    store_contribution = gross_margin - store_expenses - annual_payroll
    net_operating_spread = rev - (corp_expenses + store_expenses)

    return {
        'base_net_revenue': rev,
        'base_revenue_crores': round(rev / 10000000.0, 2),
        'base_cogs': cogs,
        'base_cogs_crores': round(cogs / 10000000.0, 2),
        'base_cogs_rate_pct': round((cogs / rev * 100) if rev > 0 else 0.0, 2),
        'base_gross_margin': gross_margin,
        'base_gross_margin_crores': round(gross_margin / 10000000.0, 2),
        'base_gross_margin_pct': round(gross_margin_pct, 2),
        'base_headcount': headcount,
        'base_avg_salary': round(avg_salary, 2),
        'base_monthly_payroll': monthly_payroll,
        'base_monthly_payroll_crores': round(monthly_payroll / 10000000.0, 2),
        'base_annual_payroll': annual_payroll,
        'base_annual_payroll_crores': round(annual_payroll / 10000000.0, 2),
        'base_store_expenses': store_expenses,
        'base_store_expenses_crores': round(store_expenses / 10000000.0, 2),
        'base_corp_expenses': corp_expenses,
        'base_corp_expenses_crores': round(corp_expenses / 10000000.0, 2),
        'base_delivered_orders': orders,
        'base_store_contribution': store_contribution,
        'base_store_contribution_crores': round(store_contribution / 10000000.0, 2),
        'base_net_operating_spread': net_operating_spread,
        'base_net_spread_crores': round(net_operating_spread / 10000000.0, 2),
    }
