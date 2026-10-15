from .db_service import execute_query, execute_one, execute_scalar
from .filter_service import build_sales_where_clause

def get_customer_dashboard_data(filters):
    """
    Retrieve comprehensive Customer Dashboard dataset:
    Active vs New vs Repeat, RFM Segmentation, CLV Tiers, Loyalty Tiers, Churn Risk.
    """
    where_clause, params = build_sales_where_clause(filters, "o")
    
    # 1. Customer Overview Metrics
    overview_sql = f"""
        WITH customer_stats AS (
            SELECT 
                cust_id,
                COUNT(order_id) AS orders_count,
                SUM(net_total) AS total_spend
            FROM sales.orders o
            {where_clause}
            GROUP BY cust_id
        )
        SELECT 
            COUNT(cust_id) AS total_active_customers,
            ROUND(AVG(total_spend), 2) AS arpu,
            ROUND(AVG(orders_count), 2) AS avg_frequency,
            COUNT(CASE WHEN orders_count >= 2 THEN 1 END) AS repeat_customers,
            ROUND(COUNT(CASE WHEN orders_count >= 2 THEN 1 END)::numeric / NULLIF(COUNT(cust_id), 0) * 100, 2) AS repeat_rate_pct
        FROM customer_stats;
    """
    overview = execute_one(overview_sql, params)
    
    # 2. Customer Tier Mix
    tier_sql = """
        SELECT 
            tier,
            COUNT(customer_id) AS customer_count,
            ROUND(COUNT(customer_id)::numeric / (SELECT COUNT(*) FROM customers.customers) * 100, 1) AS pct_of_total
        FROM customers.customers
        GROUP BY tier
        ORDER BY customer_count DESC;
    """
    tiers = execute_query(tier_sql)
    
    # 3. RFM Segment Breakdown (Filter-Aware)
    rfm_conditions = ["rfm_segment IS NOT NULL"]
    if filters.get('customer_tier'):
        rfm_conditions.append(f"cust_id IN (SELECT customer_id FROM customers.customers WHERE tier = '{filters['customer_tier']}')")
    if filters.get('store_id'):
        rfm_conditions.append(f"cust_id IN (SELECT DISTINCT cust_id FROM sales.orders WHERE store_id = {filters['store_id']})")
    elif filters.get('region_id'):
        rfm_conditions.append(f"cust_id IN (SELECT DISTINCT cust_id FROM sales.orders WHERE store_id IN (SELECT store_id FROM stores.stores WHERE region_id = {filters['region_id']}))")
    rfm_where = f"WHERE {' AND '.join(rfm_conditions)}"
    
    rfm_sql = f"""
        SELECT 
            rfm_segment,
            COUNT(*) AS customer_count,
            ROUND(AVG(recency_days), 1) AS avg_recency_days,
            ROUND(AVG(order_frequency), 1) AS avg_frequency,
            ROUND(SUM(monetary_value) / 10000000.0, 2) AS total_spend_crores,
            ROUND(AVG(monetary_value), 2) AS avg_spend_per_customer
        FROM analytics.vw_customer_rfm_scores
        {rfm_where}
        GROUP BY rfm_segment
        ORDER BY total_spend_crores DESC;
    """
    rfm_segments = execute_query(rfm_sql)
    
    # 4. Loyalty Club Members & Points
    loyalty_sql = """
        SELECT 
            t.tier_name,
            COUNT(m.customer_id) AS member_count,
            SUM(m.points_balance) AS total_points_balance,
            ROUND(AVG(m.points_balance), 0) AS avg_points
        FROM loyalty.members m
        JOIN loyalty.tiers t ON m.tier_id = t.tier_id
        GROUP BY t.tier_name
        ORDER BY member_count DESC;
    """
    loyalty_stats = execute_query(loyalty_sql)
    
    # 5. Customer Review Ratings Distribution
    review_sql = """
        SELECT 
            rating,
            COUNT(review_id) AS review_count,
            ROUND(COUNT(review_id)::numeric / (SELECT COUNT(*) FROM customers.reviews) * 100, 1) AS pct
        FROM customers.reviews
        GROUP BY rating
        ORDER BY rating DESC;
    """
    reviews = execute_query(review_sql)
    
    # 6. High-Priority Churn Risk VIP Customers
    churn_sql = """
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            c.tier,
            s.recency_days,
            s.order_frequency,
            s.monetary_value,
            ROUND(s.monetary_value / 100000.0, 2) AS spend_lakhs,
            'Send VIP Reactivation Offer' AS recommended_action
        FROM analytics.vw_customer_rfm_scores s
        JOIN customers.customers c ON s.cust_id = c.customer_id
        WHERE s.rfm_segment = 'At Risk'
        ORDER BY s.monetary_value DESC
        LIMIT 10;
    """
    churn_risk_vips = execute_query(churn_sql)
    
    return {
        'overview': overview,
        'tiers': tiers,
        'rfm_segments': rfm_segments,
        'loyalty_stats': loyalty_stats,
        'reviews': reviews,
        'churn_risk_vips': churn_risk_vips
    }
