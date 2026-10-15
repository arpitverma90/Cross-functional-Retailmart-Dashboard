from .db_service import execute_query, execute_one
from .filter_service import build_sales_where_clause

def get_sales_dashboard_data(filters):
    """
    Retrieve comprehensive Sales Dashboard dataset:
    Revenue, Orders, AOV, Categories, Top SKUs, Payment Split, Regional Store Rankings.
    """
    where_clause, params = build_sales_where_clause(filters, "o")
    
    # 1. Headline Sales Summary
    headline_sql = f"""
        SELECT 
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(o.net_total), 0) AS total_net_revenue,
            COALESCE(SUM(o.gross_total), 0) AS total_gross_revenue,
            COALESCE(SUM(o.discount_amount), 0) AS total_discount,
            COALESCE(AVG(o.net_total), 0) AS avg_order_value,
            COUNT(DISTINCT o.cust_id) AS total_customers
        FROM sales.orders o
        {where_clause};
    """
    headline = execute_one(headline_sql, params)
    
    # 2. Monthly Trend with Growth
    trend_sql = f"""
        SELECT 
            TO_CHAR(DATE_TRUNC('month', o.order_date), 'Mon YYYY') AS month_name,
            DATE_TRUNC('month', o.order_date)::date AS month_date,
            COUNT(o.order_id) AS orders,
            SUM(o.net_total) AS revenue,
            ROUND(SUM(o.net_total) / 10000000.0, 2) AS revenue_crores,
            ROUND(AVG(o.net_total)::numeric, 2) AS aov
        FROM sales.orders o
        {where_clause}
        GROUP BY DATE_TRUNC('month', o.order_date)
        ORDER BY month_date ASC;
    """
    trend_rows = execute_query(trend_sql, params)
    
    # Compute MoM growth
    for idx, row in enumerate(trend_rows):
        if idx > 0 and trend_rows[idx - 1]['revenue'] > 0:
            prev_rev = trend_rows[idx - 1]['revenue']
            row['mom_growth_pct'] = round(((row['revenue'] - prev_rev) / prev_rev) * 100, 1)
        else:
            row['mom_growth_pct'] = 0.0
            
    # 3. Category Revenue & Unit Sales
    cat_sql = f"""
        SELECT 
            c.category_id,
            c.category_name,
            COUNT(DISTINCT oi.order_id) AS order_count,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.net_amount) AS net_revenue,
            ROUND(SUM(oi.net_amount) / 10000000.0, 2) AS revenue_crores,
            ROUND(AVG(oi.unit_price)::numeric, 2) AS avg_price
        FROM sales.order_items oi
        JOIN sales.orders o ON oi.order_id = o.order_id
        JOIN products.products p ON oi.prod_id = p.product_id
        JOIN core.dim_brand b ON p.brand_id = b.brand_id
        JOIN core.dim_category c ON b.category_id = c.category_id
        {where_clause}
        GROUP BY c.category_id, c.category_name
        ORDER BY net_revenue DESC;
    """
    categories = execute_query(cat_sql, params)
    
    # 4. Top 10 SKUs by Net Revenue
    sku_sql = f"""
        SELECT 
            p.product_id,
            p.product_name,
            c.category_name,
            SUM(oi.quantity) AS total_units,
            SUM(oi.net_amount) AS total_revenue,
            ROUND(SUM(oi.net_amount) / 100000.0, 2) AS revenue_lakhs
        FROM sales.order_items oi
        JOIN sales.orders o ON oi.order_id = o.order_id
        JOIN products.products p ON oi.prod_id = p.product_id
        JOIN core.dim_brand b ON p.brand_id = b.brand_id
        JOIN core.dim_category c ON b.category_id = c.category_id
        {where_clause}
        GROUP BY p.product_id, p.product_name, c.category_name
        ORDER BY total_revenue DESC
        LIMIT 10;
    """
    top_skus = execute_query(sku_sql, params)
    
    # 5. Payment Method Split
    payment_sql = f"""
        SELECT 
            pm.mode_name,
            COUNT(o.order_id) AS order_count,
            SUM(o.net_total) AS total_revenue,
            ROUND(SUM(o.net_total) / 10000000.0, 2) AS revenue_crores
        FROM sales.orders o
        JOIN finance.payment_modes pm ON o.payment_mode_id = pm.mode_id
        {where_clause}
        GROUP BY pm.mode_name
        ORDER BY total_revenue DESC;
    """
    payment_modes = execute_query(payment_sql, params)
    
    # 6. Store Hierarchy Rankings (Top 10 Stores)
    store_sql = f"""
        SELECT 
            s.store_id,
            s.store_name,
            r.region_name,
            s.city,
            COUNT(o.order_id) AS order_count,
            SUM(o.net_total) AS total_revenue,
            ROUND(SUM(o.net_total) / 10000000.0, 2) AS revenue_crores,
            ROUND(SUM(o.net_total)::numeric / NULLIF(s.square_ft, 0), 2) AS sales_per_sqft
        FROM sales.orders o
        JOIN stores.stores s ON o.store_id = s.store_id
        JOIN core.dim_region r ON s.region_id = r.region_id
        {where_clause}
        GROUP BY s.store_id, s.store_name, r.region_name, s.city, s.square_ft
        ORDER BY total_revenue DESC
        LIMIT 10;
    """
    top_stores = execute_query(store_sql, params)
    
    return {
        'headline': headline,
        'monthly_trend': trend_rows,
        'categories': categories,
        'top_skus': top_skus,
        'payment_modes': payment_modes,
        'top_stores': top_stores
    }
