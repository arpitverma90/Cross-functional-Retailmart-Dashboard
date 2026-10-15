from .db_service import execute_scalar, execute_one

def get_simulator_baseline():
    """
    Retrieve authoritative baseline numbers from PostgreSQL for Contribution Margin simulator:
    Contribution Margin = Net Revenue - COGS - Total Refunds - Store Operating Expenses
    """
    baseline_sql = """
        SELECT 
            (SELECT SUM(net_total) FROM sales.orders WHERE order_status = 'Delivered') AS base_net_revenue,
            (SELECT SUM(oi.quantity * p.cost_price) 
             FROM sales.order_items oi 
             JOIN sales.orders o ON oi.order_id = o.order_id 
             JOIN products.products p ON oi.prod_id = p.product_id 
             WHERE o.order_status = 'Delivered') AS base_cogs,
            (SELECT SUM(refund_amount) FROM sales.returns) AS base_refunds,
            (SELECT SUM(amount) FROM stores.expenses) AS base_store_expenses,
            (SELECT COUNT(*) FROM sales.orders WHERE order_status = 'Delivered') AS base_delivered_orders;
    """
    row = execute_one(baseline_sql)
    
    rev = float(row.get('base_net_revenue') or 0.0)
    cogs = float(row.get('base_cogs') or 0.0)
    refunds = float(row.get('base_refunds') or 0.0)
    expenses = float(row.get('base_store_expenses') or 0.0)
    orders = int(row.get('base_delivered_orders') or 0)
    
    contribution_margin = rev - cogs - refunds - expenses
    contribution_margin_pct = (contribution_margin / rev * 100) if rev else 0.0
    
    return {
        'base_net_revenue': rev,
        'base_cogs': cogs,
        'base_refunds': refunds,
        'base_store_expenses': expenses,
        'base_delivered_orders': orders,
        'base_contribution_margin': contribution_margin,
        'base_contribution_margin_pct': round(contribution_margin_pct, 2),
        'base_cogs_rate_pct': round((cogs / rev * 100) if rev else 0.0, 2),
        'base_refund_rate_pct': round((refunds / rev * 100) if rev else 0.0, 2),
    }
