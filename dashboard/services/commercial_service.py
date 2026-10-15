"""
Commercial & Customer Operations Analytics Service:
Powers Sales, Customer RFM Intelligence, and Physical Operations & Manufacturing Dashboards.
"""

from dashboard.services.db_service import execute_query, execute_one
from dashboard.services.filter_service import build_sales_where_clause


def get_sales_dashboard_data(filters=None):
    """Aggregate commercial sales, revenue velocity, category Pareto, and brand rankings."""
    filters = filters or {}
    where_sql, params = build_sales_where_clause(filters, alias="o")
    
    # 1. Headline Sales KPIs
    kpi_sql = f"""
        SELECT 
            COUNT(o.order_id) AS delivered_orders,
            ROUND(SUM(o.net_total), 2) AS total_net_revenue,
            ROUND(SUM(o.net_total) / 10000000.0, 2) AS revenue_crores,
            ROUND(AVG(o.net_total), 2) AS aov,
            ROUND(SUM(o.gross_total), 2) AS total_gross_revenue,
            ROUND(SUM(o.discount_amount), 2) AS total_discounts
        FROM sales.orders o
        {where_sql};
    """
    kpis = execute_one(kpi_sql, params)
    
    # 2. Monthly Revenue Velocity & MoM Trend
    monthly_sql = """
        WITH monthly_rev AS (
            SELECT 
                DATE_TRUNC('month', order_date)::date AS sales_month,
                COUNT(order_id) AS delivered_orders,
                SUM(net_total) AS net_revenue
            FROM sales.orders
            WHERE order_status = 'Delivered'
            GROUP BY DATE_TRUNC('month', order_date)
        )
        SELECT 
            sales_month,
            delivered_orders,
            ROUND(net_revenue, 2) AS net_revenue,
            ROUND(LAG(net_revenue) OVER (ORDER BY sales_month), 2) AS prev_month_revenue,
            ROUND(
                ((net_revenue - LAG(net_revenue) OVER (ORDER BY sales_month)) 
                 / NULLIF(LAG(net_revenue) OVER (ORDER BY sales_month), 0)) * 100, 
                2
            ) AS mom_growth_pct
        FROM monthly_rev
        ORDER BY sales_month;
    """
    monthly_rows = execute_query(monthly_sql)
    
    # 3. Product Category Contribution & Gross Margins
    cat_sql = """
        SELECT 
            c.category_id,
            c.category_name,
            COUNT(DISTINCT oi.order_id) AS order_count,
            SUM(oi.quantity) AS total_units_sold,
            ROUND(SUM(oi.net_amount), 2) AS net_revenue,
            ROUND(SUM(oi.quantity * p.cost_price), 2) AS cogs,
            ROUND(SUM(oi.net_amount) - SUM(oi.quantity * p.cost_price), 2) AS gross_profit,
            ROUND(
                (SUM(oi.net_amount) - SUM(oi.quantity * p.cost_price)) 
                / NULLIF(SUM(oi.net_amount), 0) * 100, 
                2
            ) AS gross_margin_pct
        FROM sales.order_items oi
        JOIN sales.orders o ON oi.order_id = o.order_id
        JOIN products.products p ON oi.prod_id = p.product_id
        JOIN core.dim_brand b ON p.brand_id = b.brand_id
        JOIN core.dim_category c ON b.category_id = c.category_id
        WHERE o.order_status = 'Delivered'
        GROUP BY c.category_id, c.category_name
        ORDER BY net_revenue DESC;
    """
    category_rows = execute_query(cat_sql)
    
    # 4. Top 10 Best-Selling Brands
    brand_sql = """
        SELECT 
            b.brand_name,
            c.category_name,
            COUNT(DISTINCT oi.order_id) AS order_count,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.net_amount), 2) AS brand_revenue
        FROM sales.order_items oi
        JOIN sales.orders o ON oi.order_id = o.order_id
        JOIN products.products p ON oi.prod_id = p.product_id
        JOIN core.dim_brand b ON p.brand_id = b.brand_id
        JOIN core.dim_category c ON b.category_id = c.category_id
        WHERE o.order_status = 'Delivered'
        GROUP BY b.brand_name, c.category_name
        ORDER BY brand_revenue DESC
        LIMIT 10;
    """
    brand_rows = execute_query(brand_sql)
    
    # 5. Top 10 Regional Stores
    store_sql = """
        SELECT 
            s.store_id,
            s.store_name,
            s.city,
            r.region_name,
            COUNT(o.order_id) AS delivered_orders,
            ROUND(SUM(o.net_total), 2) AS store_revenue,
            ROUND(AVG(o.net_total), 2) AS aov
        FROM sales.orders o
        JOIN stores.stores s ON o.store_id = s.store_id
        JOIN core.dim_region r ON s.region_id = r.region_id
        WHERE o.order_status = 'Delivered'
        GROUP BY s.store_id, s.store_name, s.city, r.region_name
        ORDER BY store_revenue DESC
        LIMIT 10;
    """
    store_rows = execute_query(store_sql)
    
    return {
        'kpis': {
            'delivered_orders': int(kpis.get('delivered_orders') or 0),
            'total_net_revenue': float(kpis.get('total_net_revenue') or 0),
            'revenue_crores': float(kpis.get('revenue_crores') or 0),
            'aov': float(kpis.get('aov') or 0),
            'total_gross_revenue': float(kpis.get('total_gross_revenue') or 0),
            'total_discounts': float(kpis.get('total_discounts') or 0)
        },
        'monthly_trend': monthly_rows,
        'categories': category_rows,
        'brands': brand_rows,
        'stores': store_rows
    }


def get_customer_dashboard_data(filters=None):
    """Aggregate customer RFM segmentation, loyalty tier spending, and retention cohorts."""
    
    # 1. Headline Customer KPIs
    kpi_sql = """
        SELECT 
            (SELECT COUNT(*) FROM customers.customers) AS total_customers,
            (SELECT COUNT(DISTINCT cust_id) FROM sales.orders WHERE order_status = 'Delivered') AS active_buyers,
            (SELECT COUNT(*) FROM analytics.vw_customer_rfm_scores WHERE rfm_segment = 'Champions') AS champions_count,
            (SELECT COUNT(*) FROM analytics.vw_customer_rfm_scores WHERE rfm_segment = 'At Risk') AS at_risk_count,
            (SELECT ROUND(AVG(net_total), 2) FROM sales.orders WHERE order_status = 'Delivered') AS avg_order_spend;
    """
    kpis = execute_one(kpi_sql)
    
    # 2. RFM Segment Distribution
    rfm_sql = """
        SELECT 
            rfm_segment,
            COUNT(*) AS customer_count,
            ROUND(AVG(recency_days), 1) AS avg_recency_days,
            ROUND(AVG(order_frequency), 1) AS avg_order_frequency,
            ROUND(SUM(monetary_value), 2) AS total_spend,
            ROUND(SUM(monetary_value) / 10000000.0, 2) AS spend_crores,
            ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS customer_share_pct
        FROM analytics.vw_customer_rfm_scores
        GROUP BY rfm_segment
        ORDER BY total_spend DESC;
    """
    rfm_rows = execute_query(rfm_sql)
    
    # 3. Customer Loyalty Tiers
    tier_sql = """
        SELECT 
            c.tier,
            COUNT(DISTINCT c.customer_id) AS total_members,
            COUNT(DISTINCT o.cust_id) AS active_purchasers,
            ROUND(COUNT(DISTINCT o.cust_id)::numeric / NULLIF(COUNT(DISTINCT c.customer_id), 0) * 100, 2) AS conversion_pct,
            ROUND(SUM(o.net_total), 2) AS total_tier_spend,
            ROUND(AVG(o.net_total), 2) AS aov
        FROM customers.customers c
        LEFT JOIN sales.orders o ON c.customer_id = o.cust_id AND o.order_status = 'Delivered'
        GROUP BY c.tier
        ORDER BY total_tier_spend DESC NULLS LAST;
    """
    tier_rows = execute_query(tier_sql)
    
    # 4. Repeat Purchase Retention Cohorts
    repeat_sql = """
        WITH customer_frequency AS (
            SELECT 
                cust_id,
                COUNT(order_id) AS lifetime_orders,
                SUM(net_total) AS lifetime_spend
            FROM sales.orders
            WHERE order_status = 'Delivered'
            GROUP BY cust_id
        )
        SELECT 
            CASE 
                WHEN lifetime_orders = 1 THEN '1 Single Purchase'
                WHEN lifetime_orders BETWEEN 2 AND 3 THEN '2-3 Repeat Purchases'
                WHEN lifetime_orders BETWEEN 4 AND 5 THEN '4-5 Regular Purchases'
                ELSE '6+ High-Frequency Purchases'
            END AS purchase_cohort,
            COUNT(cust_id) AS customer_count,
            ROUND(COUNT(cust_id)::numeric / SUM(COUNT(cust_id)) OVER () * 100, 2) AS customer_share_pct,
            ROUND(SUM(lifetime_spend), 2) AS cohort_revenue,
            ROUND(SUM(lifetime_spend) / SUM(SUM(lifetime_spend)) OVER () * 100, 2) AS revenue_share_pct
        FROM customer_frequency
        GROUP BY 1
        ORDER BY customer_count DESC;
    """
    repeat_rows = execute_query(repeat_sql)
    
    return {
        'kpis': {
            'total_customers': int(kpis.get('total_customers') or 0),
            'active_buyers': int(kpis.get('active_buyers') or 0),
            'champions_count': int(kpis.get('champions_count') or 0),
            'at_risk_count': int(kpis.get('at_risk_count') or 0),
            'penetration_pct': round(int(kpis.get('active_buyers') or 0) / max(int(kpis.get('total_customers') or 1), 1) * 100, 1),
            'avg_order_spend': float(kpis.get('avg_order_spend') or 0)
        },
        'rfm_segments': rfm_rows,
        'tiers': tier_rows,
        'repeat_cohorts': repeat_rows
    }


def get_operations_dashboard_data(filters=None):
    """Aggregate retail store inventory health, stockout risks, and factory quality scrap rates."""
    
    # 1. Headline Operations KPIs
    kpi_sql = """
        SELECT 
            (SELECT COUNT(*) FROM products.inventory) AS total_inventory_slots,
            (SELECT COUNT(*) FROM products.inventory WHERE quantity_on_hand = 0) AS out_of_stock_skus,
            (SELECT COUNT(*) FROM products.inventory WHERE quantity_on_hand <= reorder_level AND quantity_on_hand > 0) AS low_stock_skus,
            (SELECT COUNT(*) FROM manufacture.work_orders WHERE status = 'Completed') AS total_work_orders,
            (SELECT SUM(quantity_produced) FROM manufacture.work_orders WHERE status = 'Completed') AS total_produced_units,
            (SELECT SUM(rejected_quantity) FROM manufacture.work_orders WHERE status = 'Completed') AS total_rejected_units,
            (SELECT ROUND(SUM(rejected_quantity)::numeric / NULLIF(SUM(quantity_produced), 0) * 100, 2) 
             FROM manufacture.work_orders WHERE status = 'Completed') AS scrap_rate_pct;
    """
    kpis = execute_one(kpi_sql)
    
    # 2. Inventory Health Matrix
    health_sql = """
        SELECT 
            CASE 
                WHEN quantity_on_hand = 0 THEN '1. Out of Stock'
                WHEN quantity_on_hand <= reorder_level THEN '2. Low Stock (At Reorder)'
                WHEN quantity_on_hand <= (reorder_level * 2) THEN '3. Adequate Stock'
                ELSE '4. Surplus Stock'
            END AS stock_health_status,
            COUNT(*) AS inventory_slot_count,
            ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS percentage_share,
            SUM(quantity_on_hand) AS total_units_on_hand
        FROM products.inventory
        GROUP BY 1
        ORDER BY 1;
    """
    health_rows = execute_query(health_sql)
    
    # 3. Regional Inventory Stockout Vulnerability
    reg_sql = """
        SELECT 
            r.region_name,
            COUNT(DISTINCT s.store_id) AS active_stores,
            COUNT(i.product_id) AS total_inventory_slots,
            COUNT(CASE WHEN i.quantity_on_hand = 0 THEN 1 END) AS out_of_stock_count,
            COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level AND i.quantity_on_hand > 0 THEN 1 END) AS low_stock_count,
            ROUND(
                COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END)::numeric 
                / NULLIF(COUNT(i.product_id), 0) * 100, 
                2
            ) AS regional_at_risk_pct
        FROM products.inventory i
        JOIN stores.stores s ON i.store_id = s.store_id
        JOIN core.dim_region r ON s.region_id = r.region_id
        GROUP BY r.region_name
        ORDER BY regional_at_risk_pct DESC;
    """
    regional_rows = execute_query(reg_sql)
    
    # 4. Manufacturing Production Lines & Quality Scrap
    line_sql = """
        SELECT 
            pl.line_id,
            pl.line_name,
            pl.supervisor_name,
            COUNT(wo.work_order_id) AS batches_completed,
            SUM(wo.quantity_produced) AS total_units_produced,
            SUM(wo.rejected_quantity) AS total_units_rejected,
            ROUND(
                SUM(wo.rejected_quantity)::numeric / NULLIF(SUM(wo.quantity_produced), 0) * 100, 
                2
            ) AS scrap_rate_pct
        FROM manufacture.work_orders wo
        JOIN manufacture.production_lines pl ON wo.line_id = pl.line_id
        WHERE wo.status = 'Completed'
        GROUP BY pl.line_id, pl.line_name, pl.supervisor_name
        ORDER BY scrap_rate_pct DESC;
    """
    line_rows = execute_query(line_sql)
    
    return {
        'kpis': {
            'total_inventory_slots': int(kpis.get('total_inventory_slots') or 0),
            'out_of_stock_skus': int(kpis.get('out_of_stock_skus') or 0),
            'low_stock_skus': int(kpis.get('low_stock_skus') or 0),
            'total_work_orders': int(kpis.get('total_work_orders') or 0),
            'total_produced_units': int(kpis.get('total_produced_units') or 0),
            'total_rejected_units': int(kpis.get('total_rejected_units') or 0),
            'scrap_rate_pct': float(kpis.get('scrap_rate_pct') or 0)
        },
        'health': health_rows,
        'regional_risk': regional_rows,
        'lines': line_rows
    }
