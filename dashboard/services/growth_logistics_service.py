"""
Growth & Logistics Analytics Service:
Powers Marketing, Digital Web Events, and Logistics & Supply Chain Dashboards.
"""

from dashboard.services.db_service import execute_query


def get_marketing_dashboard_data(start_date=None, end_date=None):
    """Aggregate marketing performance, platform ad spend, and email campaign engagement."""
    
    # 1. Headline KPIs
    kpi_query = """
        SELECT 
            (SELECT COUNT(*) FROM marketing.campaigns) AS total_campaigns,
            (SELECT COALESCE(SUM(budget), 0) FROM marketing.campaigns) AS total_budget,
            (SELECT COALESCE(SUM(amount), 0) FROM marketing.ads_spend) AS total_ad_spend,
            (SELECT COALESCE(SUM(emails_sent), 0) FROM marketing.email_clicks) AS total_emails_sent,
            (SELECT COALESCE(SUM(emails_opened), 0) FROM marketing.email_clicks) AS total_emails_opened,
            (SELECT COALESCE(SUM(emails_clicked), 0) FROM marketing.email_clicks) AS total_emails_clicked;
    """
    kpis = execute_query(kpi_query)[0]
    
    total_sent = kpis['total_emails_sent'] or 1
    total_opened = kpis['total_emails_opened'] or 1
    total_clicked = kpis['total_emails_clicked'] or 0
    
    open_rate = round((total_opened / total_sent) * 100, 2)
    ctr_rate = round((total_clicked / total_opened) * 100, 2)
    budget_variance = float(kpis['total_budget']) - float(kpis['total_ad_spend'])
    
    # 2. Spend by Platform
    platform_query = """
        SELECT 
            platform,
            COUNT(spend_id) AS spend_count,
            ROUND(SUM(amount), 2) AS total_spend,
            ROUND(AVG(amount), 2) AS avg_spend,
            ROUND(SUM(amount) / SUM(SUM(amount)) OVER () * 100, 2) AS platform_share_pct
        FROM marketing.ads_spend
        GROUP BY platform
        ORDER BY total_spend DESC;
    """
    platform_rows = execute_query(platform_query)
    
    # 3. Top Performing Campaigns
    campaigns_query = """
        SELECT 
            c.campaign_id,
            c.campaign_name,
            c.start_date,
            c.end_date,
            ROUND(c.budget, 2) AS budget,
            COALESCE(ROUND(SUM(a.amount), 2), 0) AS actual_spend,
            COALESCE(SUM(ec.emails_clicked), 0) AS total_clicks
        FROM marketing.campaigns c
        LEFT JOIN marketing.ads_spend a ON c.campaign_id = a.campaign_id
        LEFT JOIN marketing.email_clicks ec ON c.campaign_id = ec.campaign_id
        GROUP BY c.campaign_id, c.campaign_name, c.start_date, c.end_date, c.budget
        ORDER BY actual_spend DESC
        LIMIT 10;
    """
    campaign_rows = execute_query(campaigns_query)
    
    # 4. Monthly Ad Spend Velocity
    monthly_query = """
        SELECT 
            DATE_TRUNC('month', spend_date)::date AS spend_month,
            ROUND(SUM(amount), 2) AS monthly_spend,
            COUNT(spend_id) AS ad_count
        FROM marketing.ads_spend
        GROUP BY DATE_TRUNC('month', spend_date)
        ORDER BY spend_month;
    """
    monthly_rows = execute_query(monthly_query)

    return {
        'kpis': {
            'total_campaigns': kpis['total_campaigns'],
            'total_budget': float(kpis['total_budget']),
            'total_ad_spend': float(kpis['total_ad_spend']),
            'budget_variance': budget_variance,
            'total_emails_sent': kpis['total_emails_sent'],
            'open_rate_pct': open_rate,
            'click_through_rate_pct': ctr_rate
        },
        'platforms': platform_rows,
        'campaigns': campaign_rows,
        'monthly_spend': [
            {'month': str(r['spend_month']), 'spend': float(r['monthly_spend']), 'count': r['ad_count']}
            for r in monthly_rows
        ]
    }


def get_digital_dashboard_data(start_date=None, end_date=None):
    """Aggregate digital traffic, page views, device usage, and web user interaction events."""
    
    # 1. Headline KPIs
    kpi_query = """
        SELECT 
            (SELECT COUNT(*) FROM web_events.page_views) AS total_page_views,
            (SELECT COUNT(DISTINCT session_id) FROM web_events.page_views) AS total_sessions,
            (SELECT COUNT(DISTINCT customer_id) FROM web_events.page_views) AS unique_visitors,
            (SELECT COUNT(*) FROM web_events.events) AS total_events;
    """
    kpis = execute_query(kpi_query)[0]
    
    # 2. Device Breakdown
    device_query = """
        SELECT 
            device_type,
            COUNT(view_id) AS views_count,
            ROUND(COUNT(view_id)::numeric / SUM(COUNT(view_id)) OVER () * 100, 2) AS share_pct
        FROM web_events.page_views
        GROUP BY device_type
        ORDER BY views_count DESC;
    """
    devices = execute_query(device_query)
    
    # 3. Operating System Breakdown
    os_query = """
        SELECT 
            os,
            COUNT(view_id) AS views_count,
            ROUND(COUNT(view_id)::numeric / SUM(COUNT(view_id)) OVER () * 100, 2) AS share_pct
        FROM web_events.page_views
        GROUP BY os
        ORDER BY views_count DESC;
    """
    os_data = execute_query(os_query)
    
    # 4. User Interaction Event Types
    events_query = """
        SELECT 
            event_type,
            COUNT(event_id) AS event_count,
            ROUND(COUNT(event_id)::numeric / SUM(COUNT(event_id)) OVER () * 100, 2) AS event_share_pct
        FROM web_events.events
        GROUP BY event_type
        ORDER BY event_count DESC;
    """
    event_data = execute_query(events_query)
    
    # 5. Top Page URLs
    pages_query = """
        SELECT 
            page_url,
            COUNT(view_id) AS view_count,
            COUNT(DISTINCT session_id) AS unique_sessions
        FROM web_events.page_views
        GROUP BY page_url
        ORDER BY view_count DESC
        LIMIT 10;
    """
    top_pages = execute_query(pages_query)
    
    return {
        'kpis': {
            'total_page_views': kpis['total_page_views'],
            'total_sessions': kpis['total_sessions'],
            'unique_visitors': kpis['unique_visitors'],
            'total_events': kpis['total_events'],
            'pages_per_session': round(kpis['total_page_views'] / max(kpis['total_sessions'], 1), 2)
        },
        'devices': devices,
        'operating_systems': os_data,
        'events': event_data,
        'top_pages': top_pages
    }


def get_logistics_dashboard_data(start_date=None, end_date=None):
    """Aggregate courier partner logistics, outbound fulfillment SLA, and warehouse capacity."""
    
    # 1. Headline KPIs
    kpi_query = """
        SELECT 
            COUNT(shipment_id) AS total_outbound_shipments,
            COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_count,
            COUNT(CASE WHEN status = 'Shipped' THEN 1 END) AS in_transit_count,
            COUNT(CASE WHEN status = 'Returned' THEN 1 END) AS returned_count,
            ROUND(AVG(CASE WHEN status = 'Delivered' THEN delivered_date - shipped_date END)::numeric, 2) AS avg_lead_days,
            ROUND(
                COUNT(CASE WHEN status = 'Delivered' AND (delivered_date - shipped_date) <= 5 THEN 1 END)::numeric 
                / NULLIF(COUNT(CASE WHEN status = 'Delivered' THEN 1 END), 0) * 100, 
                2
            ) AS overall_sla_pct
        FROM sales.shipments;
    """
    kpis = execute_query(kpi_query)[0]
    
    # 2. Courier SLA & Volume Comparison
    courier_query = """
        SELECT 
            courier_name,
            COUNT(shipment_id) AS total_assigned,
            COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_count,
            COUNT(CASE WHEN status = 'Returned' THEN 1 END) AS returned_count,
            ROUND(AVG(CASE WHEN status = 'Delivered' THEN (delivered_date - shipped_date) END)::numeric, 2) AS avg_lead_days,
            ROUND(
                COUNT(CASE WHEN status = 'Delivered' AND (delivered_date - shipped_date) <= 5 THEN 1 END)::numeric 
                / NULLIF(COUNT(CASE WHEN status = 'Delivered' THEN 1 END), 0) * 100, 
                2
            ) AS sla_pct
        FROM sales.shipments
        GROUP BY courier_name
        ORDER BY total_assigned DESC;
    """
    courier_rows = execute_query(courier_query)
    
    # 3. Central Regional Distribution Warehouses
    warehouse_query = """
        SELECT 
            w.warehouse_id,
            w.name,
            w.location_city,
            w.region,
            w.capacity_sqft,
            w.manager_name,
            COUNT(s.shipment_id) AS inbound_shipments_received,
            COALESCE(SUM(s.quantity), 0) AS total_units_received
        FROM supply_chain.warehouses w
        LEFT JOIN supply_chain.shipments s ON w.warehouse_id = s.warehouse_id
        GROUP BY w.warehouse_id, w.name, w.location_city, w.region, w.capacity_sqft, w.manager_name
        ORDER BY w.capacity_sqft DESC;
    """
    warehouses = execute_query(warehouse_query)
    
    # 4. Inbound Supplier Freight Pipeline
    inbound_query = """
        SELECT 
            status,
            COUNT(shipment_id) AS shipments_count,
            SUM(quantity) AS units_count
        FROM supply_chain.shipments
        GROUP BY status
        ORDER BY shipments_count DESC;
    """
    inbound_status = execute_query(inbound_query)
    
    return {
        'kpis': {
            'total_outbound_shipments': kpis['total_outbound_shipments'],
            'delivered_count': kpis['delivered_count'],
            'in_transit_count': kpis['in_transit_count'],
            'returned_count': kpis['returned_count'],
            'avg_lead_days': float(kpis['avg_lead_days'] or 0),
            'overall_sla_pct': float(kpis['overall_sla_pct'] or 0)
        },
        'couriers': courier_rows,
        'warehouses': warehouses,
        'inbound_pipeline': inbound_status
    }
