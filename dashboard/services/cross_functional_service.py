from .db_service import execute_query, execute_one

def get_cross_functional_dashboard_data(filters):
    """
    Retrieve Cross-Functional Analytics:
    1. Delivery Transit Time vs Customer Review Rating & Return Propensity
    2. Demand-Inventory Velocity & Stockout Gap
    3. Return Cost Impact (Category x Return Reason)
    4. Production Output vs Realized Sales Demand
    5. Revenue at Risk Analysis
    """
    start_date = filters.get('start_date', '2024-01-01')
    end_date = filters.get('end_date', '2026-02-26')
    
    # 1. Delivery Transit Speed vs Customer Review Rating (Pre-aggregated)
    lead_time_impact_sql = """
        WITH cust_ratings AS (
            SELECT customer_id, AVG(rating) AS avg_cust_rating
            FROM customers.reviews
            GROUP BY customer_id
        ),
        order_delivery AS (
            SELECT 
                o.order_id,
                (sh.delivered_date - sh.shipped_date) AS lead_days,
                cr.avg_cust_rating AS rating
            FROM sales.orders o
            JOIN sales.shipments sh ON o.order_id = sh.order_id
            JOIN cust_ratings cr ON o.cust_id = cr.customer_id
            WHERE o.order_status = 'Delivered' AND sh.delivered_date IS NOT NULL
        )
        SELECT 
            CASE 
                WHEN lead_days <= 2 THEN '1-2 Days (Fast)'
                WHEN lead_days <= 5 THEN '3-5 Days (Standard SLA)'
                WHEN lead_days <= 8 THEN '6-8 Days (Delayed)'
                ELSE '9+ Days (Critical Delay)'
            END AS transit_bucket,
            COUNT(DISTINCT order_id) AS order_sample,
            ROUND(AVG(rating)::numeric, 2) AS avg_customer_rating
        FROM order_delivery
        GROUP BY 1
        ORDER BY avg_customer_rating DESC;
    """
    lead_time_impact = execute_query(lead_time_impact_sql)
    
    # 2. Return Cost Impact by Category & Reason
    returns_reason_sql = """
        SELECT 
            c.category_name,
            r.reason,
            COUNT(r.return_id) AS return_count,
            SUM(r.refund_amount) AS total_refund_cost,
            ROUND(SUM(r.refund_amount) / 100000.0, 2) AS refund_lakhs
        FROM sales.returns r
        JOIN products.products p ON r.prod_id = p.product_id
        JOIN core.dim_brand b ON p.brand_id = b.brand_id
        JOIN core.dim_category c ON b.category_id = c.category_id
        GROUP BY c.category_name, r.reason
        ORDER BY total_refund_cost DESC
        LIMIT 12;
    """
    returns_by_reason = execute_query(returns_reason_sql)
    
    # 3. Production Output vs Commercial Sales Velocity
    mfg_sales_align_sql = """
        WITH sales_vol AS (
            SELECT 
                p.product_id,
                c.category_name,
                SUM(oi.quantity) AS units_sold
            FROM sales.order_items oi
            JOIN sales.orders o ON oi.order_id = o.order_id
            JOIN products.products p ON oi.prod_id = p.product_id
            JOIN core.dim_brand b ON p.brand_id = b.brand_id
            JOIN core.dim_category c ON b.category_id = c.category_id
            WHERE o.order_status = 'Delivered'
            GROUP BY p.product_id, c.category_name
        ),
        mfg_vol AS (
            SELECT 
                product_id,
                SUM(quantity_produced - rejected_quantity) AS net_produced_units
            FROM manufacture.work_orders
            WHERE status = 'Completed'
            GROUP BY product_id
        )
        SELECT 
            s.category_name,
            SUM(s.units_sold) AS total_units_sold,
            COALESCE(SUM(m.net_produced_units), 0) AS total_units_manufactured,
            (COALESCE(SUM(m.net_produced_units), 0) - SUM(s.units_sold)) AS production_surplus_deficit
        FROM sales_vol s
        LEFT JOIN mfg_vol m ON s.product_id = m.product_id
        GROUP BY s.category_name
        ORDER BY total_units_sold DESC;
    """
    mfg_sales_alignment = execute_query(mfg_sales_align_sql)
    
    # 4. Revenue at Risk Breakdown (Proxy Metric)
    risk_sql = """
        SELECT 
            order_status AS risk_source,
            COUNT(order_id) AS order_count,
            SUM(net_total) AS revenue_at_risk,
            ROUND(SUM(net_total) / 10000000.0, 2) AS risk_crores
        FROM sales.orders
        WHERE order_status IN ('Cancelled', 'Failed', 'Returned')
        GROUP BY order_status
        ORDER BY revenue_at_risk DESC;
    """
    revenue_at_risk_breakdown = execute_query(risk_sql)
    
    total_risk = sum(r['revenue_at_risk'] for r in revenue_at_risk_breakdown)
    
    # 5. Perfect Order Rate KPI
    perfect_order_sql = """
        SELECT 
            COUNT(*) AS total_delivered_orders,
            SUM(CASE WHEN sh.delivered_date <= sh.shipped_date + INTERVAL '5 days' AND NOT EXISTS (SELECT 1 FROM sales.returns r WHERE r.order_id = o.order_id) THEN 1 ELSE 0 END) AS perfect_orders_count,
            ROUND(SUM(CASE WHEN sh.delivered_date <= sh.shipped_date + INTERVAL '5 days' AND NOT EXISTS (SELECT 1 FROM sales.returns r WHERE r.order_id = o.order_id) THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 2) AS perfect_order_rate_pct
        FROM sales.orders o
        LEFT JOIN sales.shipments sh ON o.order_id = sh.order_id
        WHERE o.order_status = 'Delivered';
    """
    perfect_order = execute_one(perfect_order_sql)
    
    return {
        'lead_time_impact': lead_time_impact,
        'returns_by_reason': returns_by_reason,
        'mfg_sales_alignment': mfg_sales_alignment,
        'revenue_at_risk_breakdown': revenue_at_risk_breakdown,
        'total_revenue_at_risk': total_risk,
        'perfect_order': perfect_order
    }
