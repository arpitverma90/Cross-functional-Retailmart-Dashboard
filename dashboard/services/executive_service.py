from datetime import datetime, timedelta
from .db_service import execute_one, execute_query, execute_scalar
from .filter_service import build_sales_where_clause

def get_executive_summary_data(filters):
    """
    Generate authoritative Executive Summary dataset:
    8-12 validated headline KPIs with prior-period comparison,
    trends, positive/negative drivers, and management attention items.
    """
    start_dt = datetime.strptime(filters['start_date'], '%Y-%m-%d').date()
    end_dt = datetime.strptime(filters['end_date'], '%Y-%m-%d').date()
    duration_days = (end_dt - start_dt).days + 1
    
    prior_end_dt = start_dt - timedelta(days=1)
    prior_start_dt = prior_end_dt - timedelta(days=duration_days - 1)
    
    current_where, current_params = build_sales_where_clause(filters, "o")
    
    prior_filters = dict(filters)
    prior_filters['start_date'] = prior_start_dt.isoformat()
    prior_filters['end_date'] = prior_end_dt.isoformat()
    prior_where, prior_params = build_sales_where_clause(prior_filters, "o")
    
    # 1. Sales & Commercial KPIs (Current Period)
    curr_sales_sql = f"""
        SELECT 
            COUNT(o.order_id) AS orders_count,
            COALESCE(SUM(o.net_total), 0) AS net_revenue,
            COALESCE(SUM(o.gross_total), 0) AS gross_revenue,
            COALESCE(SUM(o.discount_amount), 0) AS discount_amount,
            COALESCE(AVG(o.net_total), 0) AS aov,
            COUNT(DISTINCT o.cust_id) AS active_customers
        FROM sales.orders o
        {current_where};
    """
    curr_sales = execute_one(curr_sales_sql, current_params)
    
    # 2. Sales & Commercial KPIs (Prior Period)
    prior_sales_sql = f"""
        SELECT 
            COUNT(o.order_id) AS orders_count,
            COALESCE(SUM(o.net_total), 0) AS net_revenue,
            COALESCE(AVG(o.net_total), 0) AS aov,
            COUNT(DISTINCT o.cust_id) AS active_customers
        FROM sales.orders o
        {prior_where};
    """
    prior_sales = execute_one(prior_sales_sql, prior_params)
    
    # 3. Logistics & Fulfilment KPIs (Filter-Aware)
    ops_conditions = ["sh.shipped_date >= %s", "sh.shipped_date <= %s"]
    ops_params = [filters['start_date'], filters['end_date']]
    if filters.get('store_id'):
        ops_conditions.append("sh.order_id IN (SELECT order_id FROM sales.orders WHERE store_id = %s)")
        ops_params.append(filters['store_id'])
    elif filters.get('region_id'):
        ops_conditions.append("sh.order_id IN (SELECT order_id FROM sales.orders WHERE store_id IN (SELECT store_id FROM stores.stores WHERE region_id = %s))")
        ops_params.append(filters['region_id'])
    if filters.get('category_id'):
        ops_conditions.append("sh.order_id IN (SELECT oi.order_id FROM sales.order_items oi JOIN products.products p ON oi.prod_id = p.product_id JOIN core.dim_brand b ON p.brand_id = b.brand_id WHERE b.category_id = %s)")
        ops_params.append(filters['category_id'])
        
    ops_sql = f"""
        SELECT 
            COUNT(sh.shipment_id) AS total_shipments,
            COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END) AS delivered_shipments,
            ROUND(AVG(CASE WHEN sh.status = 'Delivered' THEN sh.delivered_date - sh.shipped_date END)::numeric, 2) AS avg_lead_days,
            ROUND(
                COUNT(CASE WHEN sh.status = 'Delivered' AND (sh.delivered_date - sh.shipped_date) <= 5 THEN 1 END)::numeric 
                / NULLIF(COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END), 0) * 100, 2
            ) AS on_time_sla_pct,
            COUNT(CASE WHEN sh.status = 'Shipped' AND sh.delivered_date IS NULL THEN 1 END) AS pending_shipments
        FROM sales.shipments sh
        WHERE {' AND '.join(ops_conditions)};
    """
    curr_ops = execute_one(ops_sql, ops_params)
    
    # 4. Inventory Risk (Filter-Aware)
    inv_conditions = []
    inv_params = []
    if filters.get('store_id'):
        inv_conditions.append("store_id = %s")
        inv_params.append(filters['store_id'])
    elif filters.get('region_id'):
        inv_conditions.append("store_id IN (SELECT store_id FROM stores.stores WHERE region_id = %s)")
        inv_params.append(filters['region_id'])
    if filters.get('category_id'):
        inv_conditions.append("product_id IN (SELECT p.product_id FROM products.products p JOIN core.dim_brand b ON p.brand_id = b.brand_id WHERE b.category_id = %s)")
        inv_params.append(filters['category_id'])
    inv_where = f"WHERE {' AND '.join(inv_conditions)}" if inv_conditions else ""
    inv_sql = f"""
        SELECT 
            COUNT(DISTINCT product_id) AS total_skus,
            COUNT(CASE WHEN quantity_on_hand = 0 THEN 1 END) AS out_of_stock_skus,
            COUNT(CASE WHEN quantity_on_hand <= reorder_level AND quantity_on_hand > 0 THEN 1 END) AS low_stock_skus
        FROM products.inventory
        {inv_where};
    """
    curr_inv = execute_one(inv_sql, inv_params)
    
    # 5. Returns & Refunds (Filter-Aware)
    ret_conditions = ["r.return_date >= %s", "r.return_date <= %s"]
    ret_params = [filters['start_date'], filters['end_date']]
    if filters.get('store_id'):
        ret_conditions.append("r.order_id IN (SELECT order_id FROM sales.orders WHERE store_id = %s)")
        ret_params.append(filters['store_id'])
    elif filters.get('region_id'):
        ret_conditions.append("r.order_id IN (SELECT order_id FROM sales.orders WHERE store_id IN (SELECT store_id FROM stores.stores WHERE region_id = %s))")
        ret_params.append(filters['region_id'])
    if filters.get('category_id'):
        ret_conditions.append("r.prod_id IN (SELECT p.product_id FROM products.products p JOIN core.dim_brand b ON p.brand_id = b.brand_id WHERE b.category_id = %s)")
        ret_params.append(filters['category_id'])
    returns_sql = f"""
        SELECT 
            COUNT(r.return_id) AS return_count,
            COALESCE(SUM(r.refund_amount), 0) AS total_refunds
        FROM sales.returns r
        WHERE {' AND '.join(ret_conditions)};
    """
    curr_returns = execute_one(returns_sql, ret_params)
    
    # 6. Customer Repeat Rate
    repeat_sql = f"""
        WITH customer_order_counts AS (
            SELECT cust_id, COUNT(order_id) AS ord_cnt
            FROM sales.orders o
            {current_where}
            GROUP BY cust_id
        )
        SELECT 
            COUNT(CASE WHEN ord_cnt >= 2 THEN 1 END)::numeric / NULLIF(COUNT(*), 0) * 100 AS repeat_rate_pct
        FROM customer_order_counts;
    """
    repeat_rate = execute_scalar(repeat_sql, current_params, default=0.0)
    
    # KPI Calculations & Variances
    net_rev_curr = curr_sales.get('net_revenue', 0.0)
    net_rev_prior = prior_sales.get('net_revenue', 0.0)
    rev_var_pct = ((net_rev_curr - net_rev_prior) / net_rev_prior * 100) if net_rev_prior else 0.0
    
    orders_curr = curr_sales.get('orders_count', 0)
    orders_prior = prior_sales.get('orders_count', 0)
    orders_var_pct = ((orders_curr - orders_prior) / orders_prior * 100) if orders_prior else 0.0
    
    aov_curr = curr_sales.get('aov', 0.0)
    aov_prior = prior_sales.get('aov', 0.0)
    aov_var_pct = ((aov_curr - aov_prior) / aov_prior * 100) if aov_prior else 0.0
    
    active_cust_curr = curr_sales.get('active_customers', 0)
    active_cust_prior = prior_sales.get('active_customers', 0)
    cust_var_pct = ((active_cust_curr - active_cust_prior) / active_cust_prior * 100) if active_cust_prior else 0.0
    
    gross_curr = curr_sales.get('gross_revenue', 0.0)
    disc_curr = curr_sales.get('discount_amount', 0.0)
    disc_rate_pct = (disc_curr / gross_curr * 100) if gross_curr else 0.0
    
    ret_cnt = curr_returns.get('return_count', 0)
    return_rate_pct = (ret_cnt / orders_curr * 100) if orders_curr else 0.0
    
    # 7. Monthly Revenue Trend (Filter-Aware)
    trend_sql = f"""
        SELECT 
            TO_CHAR(DATE_TRUNC('month', o.order_date), 'Mon YYYY') AS month_label,
            COUNT(o.order_id) AS total_orders,
            SUM(o.net_total) AS total_net_revenue,
            ROUND(SUM(o.net_total) / 10000000.0, 2) AS revenue_crores
        FROM sales.orders o
        {current_where}
        GROUP BY DATE_TRUNC('month', o.order_date)
        ORDER BY DATE_TRUNC('month', o.order_date) ASC;
    """
    monthly_trend = execute_query(trend_sql, current_params)
    
    # 8. Category Performance (Filter-Aware)
    cat_sql = f"""
        SELECT 
            c.category_name, 
            SUM(oi.net_amount) AS net_revenue, 
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.net_amount) / 10000000.0, 2) AS revenue_crores
        FROM sales.order_items oi
        JOIN sales.orders o ON oi.order_id = o.order_id
        JOIN products.products p ON oi.prod_id = p.product_id
        JOIN core.dim_brand b ON p.brand_id = b.brand_id
        JOIN core.dim_category c ON b.category_id = c.category_id
        {current_where}
        GROUP BY c.category_name
        ORDER BY net_revenue DESC
        LIMIT 6;
    """
    top_categories = execute_query(cat_sql, current_params)
    
    # 9. Regional Performance (Filter-Aware)
    reg_sql = f"""
        SELECT 
            r.region_name, 
            SUM(o.net_total) AS net_revenue, 
            COUNT(o.order_id) AS order_count,
            ROUND(SUM(o.net_total) / 10000000.0, 2) AS revenue_crores
        FROM sales.orders o
        JOIN stores.stores s ON o.store_id = s.store_id
        JOIN core.dim_region r ON s.region_id = r.region_id
        {current_where}
        GROUP BY r.region_name
        ORDER BY net_revenue DESC;
    """
    regional_performance = execute_query(reg_sql, current_params)
    
    # 10. Management Attention Exceptions
    attention_items = [
        {
            'area': 'Operations',
            'issue': f"{curr_inv.get('out_of_stock_skus', 0):,d} SKUs are completely Out of Stock across store branches.",
            'severity': 'critical',
            'action': 'Expedite replenishment transfers from regional warehouses to affected retail stores.',
            'drill_url': '/business-dashboard/operations/'
        },
        {
            'area': 'Logistics',
            'issue': f"Delivery SLA compliance is {curr_ops.get('on_time_sla_pct', 0)}% with {curr_ops.get('pending_shipments', 0):,d} parcels currently in-transit.",
            'severity': 'warning' if float(curr_ops.get('on_time_sla_pct', 0) or 0) >= 90 else 'critical',
            'action': 'Review courier performance thresholds and reroute parcels from lagging carriers.',
            'drill_url': '/business-dashboard/operations/'
        },
        {
            'area': 'Customer Retention',
            'issue': f"Customer Repeat Purchase Rate stands at {repeat_rate:.1f}%.",
            'severity': 'warning' if repeat_rate < 30 else 'info',
            'action': 'Engage silver/bronze loyalty tier members with targeted reorder promotions.',
            'drill_url': '/business-dashboard/customers/'
        },
        {
            'area': 'Commercial Returns',
            'issue': f"Processed {ret_cnt:,d} customer returns resulting in ₹{curr_returns.get('total_refunds', 0)/1e7:.2f} Cr in refund payouts.",
            'severity': 'warning',
            'action': 'Audit top returned SKUs with supplier QA teams for defective manufacturing runs.',
            'drill_url': '/business-dashboard/cross-functional/'
        }
    ]
    
    return {
        'reporting_period': f"{filters['start_date']} to {filters['end_date']}",
        'prior_period': f"{prior_start_dt.isoformat()} to {prior_end_dt.isoformat()}",
        'kpis': {
            'net_revenue': {'current': net_rev_curr, 'prior': net_rev_prior, 'var_pct': rev_var_pct},
            'order_volume': {'current': orders_curr, 'prior': orders_prior, 'var_pct': orders_var_pct},
            'aov': {'current': aov_curr, 'prior': aov_prior, 'var_pct': aov_var_pct},
            'active_customers': {'current': active_cust_curr, 'prior': active_cust_prior, 'var_pct': cust_var_pct},
            'discount_rate_pct': round(float(disc_rate_pct or 0.0), 2),
            'return_rate_pct': round(float(return_rate_pct or 0.0), 2),
            'repeat_rate_pct': round(float(repeat_rate or 0.0), 2),
            'on_time_sla_pct': round(float(curr_ops.get('on_time_sla_pct', 0) or 0.0), 2),
            'avg_lead_days': round(float(curr_ops.get('avg_lead_days', 0) or 0.0), 1),
            'out_of_stock_skus': int(curr_inv.get('out_of_stock_skus', 0) or 0),
            'low_stock_skus': int(curr_inv.get('low_stock_skus', 0) or 0),
            'pending_shipments': int(curr_ops.get('pending_shipments', 0) or 0),
        },
        'monthly_trend': monthly_trend,
        'top_categories': top_categories,
        'regional_performance': regional_performance,
        'attention_items': attention_items,
        'refresh_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    }
