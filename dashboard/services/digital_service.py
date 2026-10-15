"""
RetailMart V3 - Digital Service Module
Provides parameterized PostgreSQL queries for Digital Dashboard:
- Web Sessions, Page Views, and Identified Visitors
- Device and Operating System Mix
- URL Performance and Digital Conversion Funnels
- Interactive Element Event Analysis
"""

from .db_service import execute_query, execute_one, execute_scalar


def get_digital_kpis(filters):
    """
    Computes headline KPIs for the Digital domain:
    - Total Sessions
    - Total Page Views
    - Identified Active Customers
    - Pages per Session
    - Mobile Traffic Share %
    - Total User Events
    """
    where_pv = ["1=1"]
    where_ev = ["1=1"]
    params_pv = []
    params_ev = []

    if filters.get('start_date'):
        where_pv.append("view_timestamp >= %s::timestamp")
        where_ev.append("event_timestamp >= %s::timestamp")
        params_pv.append(f"{filters['start_date']} 00:00:00")
        params_ev.append(f"{filters['start_date']} 00:00:00")

    if filters.get('end_date'):
        where_pv.append("view_timestamp <= %s::timestamp")
        where_ev.append("event_timestamp <= %s::timestamp")
        params_pv.append(f"{filters['end_date']} 23:59:59")
        params_ev.append(f"{filters['end_date']} 23:59:59")

    pv_sql = f"""
        SELECT 
            COUNT(DISTINCT session_id) AS total_sessions,
            COUNT(view_id) AS total_page_views,
            COUNT(DISTINCT customer_id) AS identified_customers,
            ROUND(COUNT(view_id)::numeric / NULLIF(COUNT(DISTINCT session_id), 0), 2) AS pages_per_session,
            ROUND(COUNT(CASE WHEN device_type = 'Mobile' THEN 1 END)::numeric / NULLIF(COUNT(view_id), 0) * 100, 2) AS mobile_share_pct
        FROM web_events.page_views
        WHERE {' AND '.join(where_pv)};
    """
    pv_data = execute_one(pv_sql, params_pv) or {}

    ev_sql = f"""
        SELECT 
            COUNT(*) AS total_events,
            COUNT(CASE WHEN event_type = 'submit' THEN 1 END) AS submit_events,
            COUNT(CASE WHEN event_type = 'click' THEN 1 END) AS click_events
        FROM web_events.events
        WHERE {' AND '.join(where_ev)};
    """
    ev_data = execute_one(ev_sql, params_ev) or {}

    total_sessions = pv_data.get('total_sessions', 0)
    total_page_views = pv_data.get('total_page_views', 0)
    identified_customers = pv_data.get('identified_customers', 0)
    pages_per_session = pv_data.get('pages_per_session', 0.0)
    mobile_share_pct = pv_data.get('mobile_share_pct', 0.0)
    total_events = ev_data.get('total_events', 0)

    return {
        'total_sessions': total_sessions,
        'total_page_views': total_page_views,
        'identified_customers': identified_customers,
        'pages_per_session': pages_per_session,
        'mobile_share_pct': mobile_share_pct,
        'total_events': total_events,
        'submit_events': ev_data.get('submit_events', 0),
        'click_events': ev_data.get('click_events', 0),
    }


def get_device_os_mix(filters):
    """Device type and Operating System matrix."""
    is_default_range = (filters.get('start_date') == '2024-01-01' and filters.get('end_date') == '2026-02-26')
    if is_default_range:
        return execute_query("SELECT * FROM analytics.mv_web_device_os ORDER BY view_count DESC;")

    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("view_timestamp >= %s::timestamp")
        params.append(f"{filters['start_date']} 00:00:00")
    if filters.get('end_date'):
        where.append("view_timestamp <= %s::timestamp")
        params.append(f"{filters['end_date']} 23:59:59")

    sql = f"""
        SELECT 
            device_type,
            os,
            COUNT(*) AS view_count,
            COUNT(DISTINCT session_id) AS session_count,
            ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS traffic_share_pct
        FROM web_events.page_views
        WHERE {' AND '.join(where)}
        GROUP BY device_type, os
        ORDER BY view_count DESC;
    """
    return execute_query(sql, params)


def get_web_traffic_trend(filters):
    """Monthly trend of web page views and unique sessions."""
    is_default_range = (filters.get('start_date') == '2024-01-01' and filters.get('end_date') == '2026-02-26')
    if is_default_range:
        return execute_query("SELECT * FROM analytics.mv_web_traffic_monthly ORDER BY month_year ASC;")

    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("view_timestamp >= %s::timestamp")
        params.append(f"{filters['start_date']} 00:00:00")
    if filters.get('end_date'):
        where.append("view_timestamp <= %s::timestamp")
        params.append(f"{filters['end_date']} 23:59:59")

    sql = f"""
        SELECT 
            TO_CHAR(view_timestamp, 'YYYY-MM') AS month_year,
            COUNT(view_id) AS page_views,
            COUNT(DISTINCT session_id) AS unique_sessions,
            COUNT(DISTINCT customer_id) AS active_users,
            COUNT(CASE WHEN device_type = 'Mobile' THEN 1 END) AS mobile_views,
            COUNT(CASE WHEN device_type = 'Desktop' THEN 1 END) AS desktop_views
        FROM web_events.page_views
        WHERE {' AND '.join(where)}
        GROUP BY TO_CHAR(view_timestamp, 'YYYY-MM')
        ORDER BY month_year ASC;
    """
    return execute_query(sql, params)


def get_digital_funnel(filters):
    """
    Web event conversion funnel steps:
    1. Product Views (Browsing)
    2. Add to Cart Interactions
    3. Cart Page Views
    4. Checkout Page Views
    """
    where_pv = ["1=1"]
    params_pv = []
    where_ev = ["1=1"]
    params_ev = []

    if filters.get('start_date'):
        where_pv.append("view_timestamp >= %s::timestamp")
        params_pv.append(f"{filters['start_date']} 00:00:00")
        where_ev.append("event_timestamp >= %s::timestamp")
        params_ev.append(f"{filters['start_date']} 00:00:00")
    if filters.get('end_date'):
        where_pv.append("view_timestamp <= %s::timestamp")
        params_pv.append(f"{filters['end_date']} 23:59:59")
        where_ev.append("event_timestamp <= %s::timestamp")
        params_ev.append(f"{filters['end_date']} 23:59:59")

    sql = f"""
        WITH funnel_counts AS (
            SELECT 
                COUNT(CASE WHEN page_url LIKE '/product%%' THEN 1 END) AS product_views,
                COUNT(CASE WHEN page_url = '/cart' THEN 1 END) AS cart_views,
                COUNT(CASE WHEN page_url = '/checkout' THEN 1 END) AS checkout_views
            FROM web_events.page_views
            WHERE {' AND '.join(where_pv)}
        ),
        cart_submits AS (
            SELECT COUNT(*) AS add_to_cart_events
            FROM web_events.events
            WHERE element_id = 'btn_add_to_cart' AND {' AND '.join(where_ev)}
        )
        SELECT 
            fc.product_views,
            cs.add_to_cart_events,
            fc.cart_views,
            fc.checkout_views
        FROM funnel_counts fc, cart_submits cs;
    """
    row = execute_one(sql, params_pv + params_ev) or {}
    
    product_views = row.get('product_views', 0)
    add_to_cart = row.get('add_to_cart_events', 0)
    cart_views = row.get('cart_views', 0)
    checkout_views = row.get('checkout_views', 0)

    stages = [
        {
            'stage': 'Product Page Views',
            'count': product_views,
            'conversion_pct': 100.0,
            'dropoff_pct': 0.0
        },
        {
            'stage': 'Add to Cart Events',
            'count': add_to_cart,
            'conversion_pct': round(add_to_cart / product_views * 100, 2) if product_views > 0 else 0.0,
            'dropoff_pct': round((1 - add_to_cart / product_views) * 100, 2) if product_views > 0 else 0.0
        },
        {
            'stage': 'Cart Page Views',
            'count': cart_views,
            'conversion_pct': round(cart_views / add_to_cart * 100, 2) if add_to_cart > 0 else 0.0,
            'dropoff_pct': round((1 - cart_views / add_to_cart) * 100, 2) if add_to_cart > 0 else 0.0
        },
        {
            'stage': 'Checkout Page Views',
            'count': checkout_views,
            'conversion_pct': round(checkout_views / cart_views * 100, 2) if cart_views > 0 else 0.0,
            'dropoff_pct': round((1 - checkout_views / cart_views) * 100, 2) if cart_views > 0 else 0.0
        }
    ]
    return stages


def get_top_landing_pages(filters, limit=10):
    """Top visited site pages and visitor volumes."""
    is_default_range = (filters.get('start_date') == '2024-01-01' and filters.get('end_date') == '2026-02-26')
    if is_default_range:
        return execute_query(f"SELECT * FROM analytics.mv_top_pages ORDER BY views_count DESC LIMIT {int(limit)};")

    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("view_timestamp >= %s::timestamp")
        params.append(f"{filters['start_date']} 00:00:00")
    if filters.get('end_date'):
        where.append("view_timestamp <= %s::timestamp")
        params.append(f"{filters['end_date']} 23:59:59")

    sql = f"""
        SELECT 
            page_url,
            COUNT(*) AS views_count,
            COUNT(DISTINCT session_id) AS unique_sessions,
            COUNT(DISTINCT customer_id) AS unique_customers,
            ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS share_pct
        FROM web_events.page_views
        WHERE {' AND '.join(where)}
        GROUP BY page_url
        ORDER BY views_count DESC
        LIMIT {int(limit)};
    """
    return execute_query(sql, params)


def get_event_interactions(filters):
    """User interaction breakdown by UI element and event type."""
    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("event_timestamp >= %s::timestamp")
        params.append(f"{filters['start_date']} 00:00:00")
    if filters.get('end_date'):
        where.append("event_timestamp <= %s::timestamp")
        params.append(f"{filters['end_date']} 23:59:59")

    sql = f"""
        SELECT 
            element_id,
            COUNT(*) AS total_interactions,
            COUNT(CASE WHEN event_type = 'click' THEN 1 END) AS click_count,
            COUNT(CASE WHEN event_type = 'submit' THEN 1 END) AS submit_count,
            COUNT(CASE WHEN event_type = 'scroll' THEN 1 END) AS scroll_count,
            COUNT(CASE WHEN event_type = 'hover' THEN 1 END) AS hover_count
        FROM web_events.events
        WHERE {' AND '.join(where)}
        GROUP BY element_id
        ORDER BY total_interactions DESC;
    """
    return execute_query(sql, params)
