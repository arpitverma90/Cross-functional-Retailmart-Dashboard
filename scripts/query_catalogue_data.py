"""
RetailMart V3 - Authoritative SQL Query Catalogue
Contains 39 Production-Grade SQL Queries strictly covering:
1. Executive Summary Dashboard KPIs (Cross-Domain Synthesis)
2. Marketing Domain KPIs & In-Depth Analytics (Spend, Platforms, Campaigns, Email)
3. Digital Domain KPIs & In-Depth Analytics (Sessions, Funnels, Device/OS, Landing Pages)
4. Logistics & Supply Chain KPIs (Carrier SLAs, Lead Times, Warehouses, Stockouts)
5. Cross-Functional Integration KPIs (MER, Digital-to-Order, Promo-Stock, Leakage)
6. Exploratory Data Analysis (EDA) Deep-Dives
"""

CATALOGUE = [
    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY DASHBOARD KPIS (9 QUERIES)
    # =========================================================================
    {
        "id": "KPI 1.1",
        "title": "Delivered Commercial Net Revenue & Order Volume",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Commercial",
        "purpose": "Authoritative commercial top-line recognized income from fulfilled customer orders.",
        "formula": "Delivered Net Revenue = SUM(net_total WHERE order_status = 'Delivered')",
        "grain": "Enterprise Portfolio Grain",
        "tables": "sales.orders",
        "action": "If realized revenue trails >5% below comparative prior period, trigger regional commercial reviews.",
        "sql": """-- KPI 1.1: Delivered Commercial Net Revenue & Order Volume
SELECT 
    COUNT(order_id) AS delivered_orders,
    ROUND(SUM(net_total), 2) AS total_net_revenue_inr,
    ROUND(SUM(net_total) / 10000000.0, 2) AS net_revenue_crores,
    ROUND(AVG(net_total), 2) AS average_order_value_inr
FROM sales.orders
WHERE order_status = 'Delivered';"""
    },
    {
        "id": "KPI 1.2",
        "title": "Total Marketing Campaign Advertising Expenditure",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Marketing",
        "purpose": "Measures total capital deployed across paid digital acquisition platforms.",
        "formula": "Total Ad Spend = SUM(amount) FROM marketing.ads_spend",
        "grain": "Marketing Spend Grain",
        "tables": "marketing.ads_spend",
        "action": "Pace ad spend against authorized budgets to avoid under-deployment or acquisition exhaustion.",
        "sql": """-- KPI 1.2: Total Marketing Campaign Advertising Expenditure
SELECT 
    COUNT(spend_id) AS total_spend_records,
    COUNT(DISTINCT campaign_id) AS funded_campaigns,
    COUNT(DISTINCT platform) AS active_platforms,
    ROUND(SUM(amount), 2) AS total_ad_spend_inr,
    ROUND(SUM(amount) / 100000.0, 2) AS total_ad_spend_lakhs
FROM marketing.ads_spend;"""
    },
    {
        "id": "KPI 1.3",
        "title": "Blended Marketing Efficiency Ratio (MER) [PROXY]",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Cross-Functional Yield",
        "purpose": "Evaluates macro top-line commercial revenue generated per rupee of advertising deployed.",
        "formula": "MER = Delivered Net Revenue / Total Ad Spend",
        "grain": "Macro Ratio Grain",
        "tables": "sales.orders, marketing.ads_spend",
        "action": "If blended MER drops below 500x, audit platform mix and reallocate budget to higher-converting channels.",
        "sql": """-- KPI 1.3: Blended Marketing Efficiency Ratio (MER) [PROXY]
WITH revenue AS (
    SELECT SUM(net_total) AS total_rev
    FROM sales.orders
    WHERE order_status = 'Delivered'
),
marketing AS (
    SELECT SUM(amount) AS total_spend
    FROM marketing.ads_spend
)
SELECT 
    ROUND(r.total_rev, 2) AS delivered_revenue_inr,
    ROUND(m.total_spend, 2) AS marketing_ad_spend_inr,
    ROUND((r.total_rev / NULLIF(m.total_spend, 0))::numeric, 2) AS blended_mer_ratio
FROM revenue r, marketing m;"""
    },
    {
        "id": "KPI 1.4",
        "title": "Digital Web Traffic & Identified Active Customer Base",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Digital",
        "purpose": "Monitors total online user engagement intensity and authenticated customer penetration.",
        "formula": "Total Sessions = COUNT(DISTINCT session_id); Identified Customers = COUNT(DISTINCT customer_id)",
        "grain": "Digital Traffic Grain",
        "tables": "web_events.page_views",
        "action": "If anonymous traffic exceeds 35%, implement account creation and registration incentives.",
        "sql": """-- KPI 1.4: Digital Web Traffic & Identified Active Customer Base
SELECT 
    COUNT(view_id) AS total_page_views,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(DISTINCT customer_id) AS identified_customers,
    ROUND(COUNT(view_id)::numeric / NULLIF(COUNT(DISTINCT session_id), 0), 2) AS avg_pages_per_session
FROM web_events.page_views;"""
    },
    {
        "id": "KPI 1.5",
        "title": "Outbound Order Dispatches & Completed Parcel Volume",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Logistics",
        "purpose": "Tracks total fulfillment throughput and delivery success rates across logistics partners.",
        "formula": "Delivery Completion Rate = (COUNT(status = 'Delivered') / Total Shipments) * 100",
        "grain": "Shipment Grain",
        "tables": "sales.shipments",
        "action": "Investigate returned and in-transit parcels when dispatch pipelines experience delivery backlogs.",
        "sql": """-- KPI 1.5: Outbound Order Dispatches & Completed Parcel Volume
SELECT 
    status AS shipment_status,
    COUNT(shipment_id) AS shipment_count,
    ROUND(COUNT(shipment_id)::numeric / SUM(COUNT(shipment_id)) OVER () * 100, 2) AS share_pct
FROM sales.shipments
GROUP BY status
ORDER BY shipment_count DESC;"""
    },
    {
        "id": "KPI 1.6",
        "title": "Carrier 5-Day On-Time Delivery (OTD) SLA Compliance Rate",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Logistics",
        "purpose": "Core carrier performance SLA measuring percentage of parcels delivered within <= 5 transit days.",
        "formula": "OTD SLA % = (COUNT(delivered_date - shipped_date <= 5) / COUNT(Delivered)) * 100",
        "grain": "Parcel Fulfillment Grain",
        "tables": "sales.shipments",
        "action": "Reallocate parcel volume away from couriers failing to maintain the 80% SLA threshold.",
        "sql": """-- KPI 1.6: Carrier 5-Day On-Time Delivery (OTD) SLA Compliance Rate
SELECT 
    COUNT(shipment_id) AS total_delivered_parcels,
    COUNT(CASE WHEN (delivered_date - shipped_date) <= 5 THEN 1 END) AS on_time_parcels,
    COUNT(CASE WHEN (delivered_date - shipped_date) > 5 THEN 1 END) AS breached_sla_parcels,
    ROUND(COUNT(CASE WHEN (delivered_date - shipped_date) <= 5 THEN 1 END)::numeric / 
          NULLIF(COUNT(shipment_id), 0) * 100, 2) AS otd_sla_compliance_pct
FROM sales.shipments
WHERE status = 'Delivered' AND delivered_date IS NOT NULL;"""
    },
    {
        "id": "KPI 1.7",
        "title": "Average Delivery Transit Lead Time (Days)",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Logistics",
        "purpose": "Measures fulfillment network velocity from warehouse dispatch to customer doorstep delivery.",
        "formula": "Average Lead Time = AVG(delivered_date - shipped_date)",
        "grain": "Parcel Transit Grain",
        "tables": "sales.shipments",
        "action": "Audit carrier sorting hubs when average lead time exceeds 4.5 days.",
        "sql": """-- KPI 1.7: Average Delivery Transit Lead Time (Days)
SELECT 
    courier_name,
    COUNT(shipment_id) AS delivered_shipments,
    ROUND(AVG(delivered_date - shipped_date)::numeric, 2) AS avg_lead_time_days,
    MIN(delivered_date - shipped_date) AS min_lead_days,
    MAX(delivered_date - shipped_date) AS max_lead_days
FROM sales.shipments
WHERE status = 'Delivered' AND delivered_date >= shipped_date
GROUP BY courier_name
ORDER BY avg_lead_time_days ASC;"""
    },
    {
        "id": "KPI 1.8",
        "title": "Retail Store Critical Inventory Stockout Vulnerability SKUs",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Logistics",
        "purpose": "Quantifies retail store merchandise lines facing imminent depletion at or below reorder levels.",
        "formula": "Stockout SKUs = COUNT(*) WHERE quantity_on_hand <= reorder_level",
        "grain": "Store-SKU Pair Grain",
        "tables": "products.inventory",
        "action": "Issue emergency replenishment pick orders to regional distribution warehouses for affected branches.",
        "sql": """-- KPI 1.8: Retail Store Critical Inventory Stockout Vulnerability SKUs
SELECT 
    COUNT(*) AS total_store_inventory_records,
    COUNT(CASE WHEN quantity_on_hand = 0 THEN 1 END) AS out_of_stock_records,
    COUNT(CASE WHEN quantity_on_hand <= reorder_level AND quantity_on_hand > 0 THEN 1 END) AS low_stock_warning_records,
    COUNT(CASE WHEN quantity_on_hand <= reorder_level THEN 1 END) AS total_critical_stockout_skus,
    ROUND(COUNT(CASE WHEN quantity_on_hand <= reorder_level THEN 1 END)::numeric / COUNT(*) * 100, 2) AS stockout_exposure_pct
FROM products.inventory;"""
    },
    {
        "id": "KPI 1.9",
        "title": "Commercial Revenue at Operational & Fulfillment Risk [PROXY]",
        "section": "1. Executive Summary Dashboard KPIs",
        "domain": "Executive Summary & Commercial Governance",
        "purpose": "Monitors total gross commercial value lost to transactional drop-offs, cancellations, and payment failures.",
        "formula": "Revenue at Risk = SUM(net_total WHERE order_status IN ('Cancelled', 'Failed'))",
        "grain": "Operational Exception Grain",
        "tables": "sales.orders",
        "action": "Form cross-functional taskforce between engineering and payment gateways to fix checkout failures.",
        "sql": """-- KPI 1.9: Commercial Revenue at Operational & Fulfillment Risk [PROXY]
SELECT 
    order_status AS risk_category,
    COUNT(order_id) AS dropped_orders_count,
    ROUND(SUM(net_total), 2) AS revenue_at_risk_inr,
    ROUND(SUM(net_total) / 10000000.0, 2) AS revenue_at_risk_crores,
    ROUND(AVG(net_total), 2) AS avg_dropped_order_value_inr
FROM sales.orders
WHERE order_status IN ('Cancelled', 'Failed')
GROUP BY order_status
ORDER BY revenue_at_risk_inr DESC;"""
    },

    # =========================================================================
    # SECTION 2: MARKETING DOMAIN KPIS & IN-DEPTH ANALYTICS (7 QUERIES)
    # =========================================================================
    {
        "id": "KPI 2.1",
        "title": "Paid Ad Spend Allocation & Share across Digital Platforms",
        "section": "2. Marketing Domain KPIs & In-Depth Analytics",
        "domain": "Marketing Intelligence",
        "purpose": "Evaluates capital distribution across Meta/Facebook, Google, Twitter, LinkedIn, and Instagram.",
        "formula": "Platform Share % = (SUM(amount per platform) / Total Spend) * 100",
        "grain": "Platform Aggregate Grain",
        "tables": "marketing.ads_spend",
        "action": "Scale budgets into top-performing channels and re-negotiate CPM contracts on lagging networks.",
        "sql": """-- KPI 2.1: Paid Ad Spend Allocation & Share across Digital Platforms
SELECT 
    platform,
    COUNT(spend_id) AS spend_events_count,
    COUNT(DISTINCT campaign_id) AS campaigns_supported,
    ROUND(SUM(amount), 2) AS total_spend_inr,
    ROUND(AVG(amount), 2) AS avg_daily_spend_inr,
    ROUND(SUM(amount)::numeric / SUM(SUM(amount)) OVER () * 100, 2) AS spend_share_pct
FROM marketing.ads_spend
GROUP BY platform
ORDER BY total_spend_inr DESC;"""
    },
    {
        "id": "KPI 2.2",
        "title": "Marketing Campaign Budget Authorization & Pacing Utilization",
        "section": "2. Marketing Domain KPIs & In-Depth Analytics",
        "domain": "Marketing Intelligence",
        "purpose": "Measures budget pacing against corporate authorized caps to prevent under-investment.",
        "formula": "Budget Utilization % = (SUM(ads_spend.amount) / SUM(campaigns.budget)) * 100",
        "grain": "Campaign Portfolio Grain",
        "tables": "marketing.campaigns, marketing.ads_spend",
        "action": "Accelerate ad deployment for strategic initiatives trailing below 50% budget utilization.",
        "sql": """-- KPI 2.2: Marketing Campaign Budget Authorization & Pacing Utilization
SELECT 
    COUNT(DISTINCT c.campaign_id) AS total_campaigns,
    ROUND(SUM(c.budget), 2) AS total_authorized_budget_inr,
    ROUND(SUM(c.budget) / 10000000.0, 2) AS total_budget_crores,
    ROUND(COALESCE(SUM(s.amount), 0), 2) AS total_realized_spend_inr,
    ROUND((COALESCE(SUM(s.amount), 0) / NULLIF(SUM(c.budget), 0) * 100)::numeric, 2) AS overall_utilization_pct
FROM marketing.campaigns c
LEFT JOIN marketing.ads_spend s ON c.campaign_id = s.campaign_id;"""
    },
    {
        "id": "KPI 2.3",
        "title": "Monthly Marketing Ad Spend Trajectory by Platform",
        "section": "2. Marketing Domain KPIs & In-Depth Analytics",
        "domain": "Marketing Intelligence",
        "purpose": "Tracks temporal spending patterns and channel diversification over calendar months.",
        "formula": "Monthly Spend = SUM(amount) GROUP BY Month, Platform",
        "grain": "Platform × Monthly Grain",
        "tables": "marketing.ads_spend",
        "action": "Align monthly ad spend surges with retail promotional calendars and festival seasons.",
        "sql": """-- KPI 2.3: Monthly Marketing Ad Spend Trajectory by Platform
SELECT 
    TO_CHAR(spend_date, 'YYYY-MM') AS spend_month,
    ROUND(SUM(amount), 2) AS total_monthly_spend_inr,
    ROUND(SUM(CASE WHEN platform = 'Facebook' THEN amount ELSE 0 END), 2) AS facebook_spend_inr,
    ROUND(SUM(CASE WHEN platform = 'Google' THEN amount ELSE 0 END), 2) AS google_spend_inr,
    ROUND(SUM(CASE WHEN platform = 'Twitter' THEN amount ELSE 0 END), 2) AS twitter_spend_inr,
    ROUND(SUM(CASE WHEN platform = 'LinkedIn' THEN amount ELSE 0 END), 2) AS linkedin_spend_inr,
    ROUND(SUM(CASE WHEN platform = 'Instagram' THEN amount ELSE 0 END), 2) AS instagram_spend_inr
FROM marketing.ads_spend
GROUP BY TO_CHAR(spend_date, 'YYYY-MM')
ORDER BY spend_month ASC;"""
    },
    {
        "id": "KPI 2.4",
        "title": "Email Marketing Outbound Reach & Open Rate Performance",
        "section": "2. Marketing Domain KPIs & In-Depth Analytics",
        "domain": "Marketing Intelligence",
        "purpose": "Measures customer attention and subject-line engagement on owned email communications.",
        "formula": "Open Rate % = (SUM(emails_opened) / SUM(emails_sent)) * 100",
        "grain": "Email Campaign Grain",
        "tables": "marketing.email_clicks",
        "action": "A/B test subject lines and optimize send times if open rate dips below the 25% benchmark.",
        "sql": """-- KPI 2.4: Email Marketing Outbound Reach & Open Rate Performance
SELECT 
    COUNT(email_id) AS email_campaign_records,
    SUM(emails_sent) AS total_emails_sent,
    SUM(emails_opened) AS total_emails_opened,
    ROUND((SUM(emails_opened)::numeric / NULLIF(SUM(emails_sent), 0) * 100), 2) AS aggregate_open_rate_pct,
    ROUND(AVG(emails_sent), 0) AS avg_emails_per_blast,
    ROUND(AVG(emails_opened), 0) AS avg_opens_per_blast
FROM marketing.email_clicks;"""
    },
    {
        "id": "KPI 2.5",
        "title": "Email Click-Through Rate (CTR) & Reader Interaction",
        "section": "2. Marketing Domain KPIs & In-Depth Analytics",
        "domain": "Marketing Intelligence",
        "purpose": "Measures creative effectiveness and customer purchase intent from opened emails.",
        "formula": "CTR on Opens % = (SUM(emails_clicked) / SUM(emails_opened)) * 100",
        "grain": "Email Interaction Grain",
        "tables": "marketing.email_clicks",
        "action": "Refine email body copy, call-to-action buttons, and landing page URLs for under-performing blasts.",
        "sql": """-- KPI 2.5: Email Click-Through Rate (CTR) & Reader Interaction
SELECT 
    COUNT(email_id) AS total_blasts,
    SUM(emails_opened) AS total_opens,
    SUM(emails_clicked) AS total_clicks,
    ROUND((SUM(emails_clicked)::numeric / NULLIF(SUM(emails_opened), 0) * 100), 2) AS click_to_open_rate_pct,
    ROUND((SUM(emails_clicked)::numeric / NULLIF(SUM(emails_sent), 0) * 100), 2) AS overall_campaign_ctr_pct
FROM marketing.email_clicks;"""
    },
    {
        "id": "KPI 2.6",
        "title": "Top 10 High-Investment Marketing Campaigns & Pacing Audit",
        "section": "2. Marketing Domain KPIs & In-Depth Analytics",
        "domain": "Marketing Intelligence",
        "purpose": "Highlights major strategic campaign initiatives by cumulative investment and budget realization.",
        "formula": "Pacing % = (Total Spend / Budget) * 100",
        "grain": "Campaign Master Grain",
        "tables": "marketing.campaigns, marketing.ads_spend",
        "action": "Conduct executive review of initiatives with >15% utilization to gauge attributed brand uplift.",
        "sql": """-- KPI 2.6: Top 10 High-Investment Marketing Campaigns & Pacing Audit
SELECT 
    c.campaign_id,
    c.campaign_name,
    c.start_date,
    c.end_date,
    ROUND(c.budget, 2) AS authorized_budget_inr,
    ROUND(COALESCE(SUM(s.amount), 0), 2) AS realized_spend_inr,
    ROUND((COALESCE(SUM(s.amount), 0) / NULLIF(c.budget, 0) * 100)::numeric, 2) AS pacing_pct,
    COUNT(DISTINCT s.platform) AS platform_presence
FROM marketing.campaigns c
LEFT JOIN marketing.ads_spend s ON c.campaign_id = s.campaign_id
GROUP BY c.campaign_id, c.campaign_name, c.start_date, c.end_date, c.budget
ORDER BY realized_spend_inr DESC
LIMIT 10;"""
    },
    {
        "id": "KPI 2.7",
        "title": "Monthly Email Marketing Engagement Pacing & Seasonality",
        "section": "2. Marketing Domain KPIs & In-Depth Analytics",
        "domain": "Marketing Intelligence",
        "purpose": "Evaluates email engagement stability and seasonal trends across monthly communication cycles.",
        "formula": "Monthly Open Rate % = (Opened / Sent) * 100; Click Rate % = (Clicked / Opened) * 100",
        "grain": "Monthly Email Grain",
        "tables": "marketing.email_clicks",
        "action": "Adjust email frequency and cadence during months exhibiting audience fatigue.",
        "sql": """-- KPI 2.7: Monthly Email Marketing Engagement Pacing & Seasonality
SELECT 
    TO_CHAR(sent_date, 'YYYY-MM') AS email_month,
    SUM(emails_sent) AS sent_volume,
    SUM(emails_opened) AS opened_volume,
    SUM(emails_clicked) AS clicked_volume,
    ROUND((SUM(emails_opened)::numeric / NULLIF(SUM(emails_sent), 0) * 100), 2) AS monthly_open_rate_pct,
    ROUND((SUM(emails_clicked)::numeric / NULLIF(SUM(emails_opened), 0) * 100), 2) AS monthly_ctr_pct
FROM marketing.email_clicks
GROUP BY TO_CHAR(sent_date, 'YYYY-MM')
ORDER BY email_month ASC;"""
    },

    # =========================================================================
    # SECTION 3: DIGITAL DOMAIN KPIS & IN-DEPTH ANALYTICS (7 QUERIES)
    # =========================================================================
    {
        "id": "KPI 3.1",
        "title": "Total Digital Browsing Sessions & Page View Engagement Depth",
        "section": "3. Digital Domain KPIs & In-Depth Analytics",
        "domain": "Digital Experience",
        "purpose": "Monitors digital store visit volume and browsing depth per visitor session.",
        "formula": "Depth = COUNT(view_id) / COUNT(DISTINCT session_id)",
        "grain": "Digital Aggregate Grain",
        "tables": "web_events.page_views",
        "action": "If depth falls below 4.0 pages/session, improve on-site product recommendation carousels.",
        "sql": """-- KPI 3.1: Total Digital Browsing Sessions & Page View Engagement Depth
SELECT 
    COUNT(view_id) AS total_page_views,
    COUNT(DISTINCT session_id) AS total_unique_sessions,
    COUNT(DISTINCT customer_id) AS logged_in_customers,
    ROUND(COUNT(view_id)::numeric / NULLIF(COUNT(DISTINCT session_id), 0), 2) AS pages_per_session
FROM web_events.page_views;"""
    },
    {
        "id": "KPI 3.2",
        "title": "Device Ecosystem Distribution: Mobile vs Desktop Penetration",
        "section": "3. Digital Domain KPIs & In-Depth Analytics",
        "domain": "Digital Experience",
        "purpose": "Evaluates user traffic split across Mobile and Desktop form factors to guide UI optimization.",
        "formula": "Device Share % = (Views per Device / Total Views) * 100",
        "grain": "Device Form Factor Grain",
        "tables": "web_events.page_views",
        "action": "Prioritize mobile-first checkout flows when mobile penetration exceeds 55% of all traffic.",
        "sql": """-- KPI 3.2: Device Ecosystem Distribution: Mobile vs Desktop Penetration
SELECT 
    device_type,
    COUNT(view_id) AS total_page_views,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(DISTINCT customer_id) AS identified_customers,
    ROUND(COUNT(view_id)::numeric / SUM(COUNT(view_id)) OVER () * 100, 2) AS traffic_share_pct
FROM web_events.page_views
GROUP BY device_type
ORDER BY total_page_views DESC;"""
    },
    {
        "id": "KPI 3.3",
        "title": "Operating System Adoption & Digital Compatibility Matrix",
        "section": "3. Digital Domain KPIs & In-Depth Analytics",
        "domain": "Digital Experience",
        "purpose": "Surfaces client runtime environments to guarantee cross-browser and OS rendering compatibility.",
        "formula": "OS Share % = (Views per OS / Total Views) * 100",
        "grain": "Operating System Grain",
        "tables": "web_events.page_views",
        "action": "Target automated browser QA testing on Linux, Windows, MacOS, Android, and iOS releases.",
        "sql": """-- KPI 3.3: Operating System Adoption & Digital Compatibility Matrix
SELECT 
    os AS operating_system,
    device_type,
    COUNT(view_id) AS total_views,
    COUNT(DISTINCT session_id) AS unique_sessions,
    ROUND(COUNT(view_id)::numeric / SUM(COUNT(view_id)) OVER () * 100, 2) AS os_share_pct
FROM web_events.page_views
GROUP BY os, device_type
ORDER BY total_views DESC;"""
    },
    {
        "id": "KPI 3.4",
        "title": "Monthly Digital Traffic Velocity & Authenticated Visitor Trajectory",
        "section": "3. Digital Domain KPIs & In-Depth Analytics",
        "domain": "Digital Experience",
        "purpose": "Monitors monthly digital footfall and growth trends in authenticated customer sessions.",
        "formula": "Monthly Views & Sessions = COUNT(*) GROUP BY Month",
        "grain": "Monthly Traffic Grain",
        "tables": "web_events.page_views",
        "action": "Ensure web hosting capacity and CDN auto-scaling are configured for peak traffic months.",
        "sql": """-- KPI 3.4: Monthly Digital Traffic Velocity & Authenticated Visitor Trajectory
SELECT 
    TO_CHAR(view_timestamp, 'YYYY-MM') AS traffic_month,
    COUNT(view_id) AS monthly_views,
    COUNT(DISTINCT session_id) AS monthly_sessions,
    COUNT(DISTINCT customer_id) AS active_authenticated_users,
    ROUND(COUNT(view_id)::numeric / NULLIF(COUNT(DISTINCT session_id), 0), 2) AS monthly_depth
FROM web_events.page_views
GROUP BY TO_CHAR(view_timestamp, 'YYYY-MM')
ORDER BY traffic_month ASC;"""
    },
    {
        "id": "KPI 3.5",
        "title": "Digital Conversion Funnel: Product Browse to Checkout Progression",
        "section": "3. Digital Domain KPIs & In-Depth Analytics",
        "domain": "Digital Experience",
        "purpose": "Maps step-by-step conversion funnel progression from product browsing to cart checkout.",
        "formula": "Funnel Progression % = (Current Stage Volume / Preceding Stage Volume) * 100",
        "grain": "Funnel Stage Grain",
        "tables": "web_events.page_views, web_events.events",
        "action": "Streamline cart page and eliminate unnecessary checkout fields when cart drop-off exceeds 60%.",
        "sql": """-- KPI 3.5: Digital Conversion Funnel: Product Browse to Checkout Progression
WITH funnel AS (
    SELECT 
        COUNT(CASE WHEN page_url LIKE '/product%%' THEN 1 END) AS product_views,
        COUNT(CASE WHEN page_url = '/cart' THEN 1 END) AS cart_views,
        COUNT(CASE WHEN page_url = '/checkout' THEN 1 END) AS checkout_views
    FROM web_events.page_views
),
events AS (
    SELECT COUNT(*) AS add_to_cart_clicks
    FROM web_events.events
    WHERE element_id = 'btn_add_to_cart'
)
SELECT 
    f.product_views,
    e.add_to_cart_clicks,
    f.cart_views,
    f.checkout_views,
    ROUND(e.add_to_cart_clicks::numeric / NULLIF(f.product_views, 0) * 100, 2) AS browse_to_cart_pct,
    ROUND(f.checkout_views::numeric / NULLIF(f.cart_views, 0) * 100, 2) AS cart_to_checkout_pct
FROM funnel f, events e;"""
    },
    {
        "id": "KPI 3.6",
        "title": "Top 10 High-Traffic Landing Pages & Product Destinations",
        "section": "3. Digital Domain KPIs & In-Depth Analytics",
        "domain": "Digital Experience",
        "purpose": "Identifies most heavily trafficked destination URLs to prioritize on-page merchandising.",
        "formula": "URL Share % = (Views per URL / Total Views) * 100",
        "grain": "Page URL Grain",
        "tables": "web_events.page_views",
        "action": "Optimize core Web Vitals and load speeds for the top 10 highest-traffic destination pages.",
        "sql": """-- KPI 3.6: Top 10 High-Traffic Landing Pages & Product Destinations
SELECT 
    page_url,
    COUNT(view_id) AS total_views,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(COUNT(view_id)::numeric / 500000.0 * 100, 2) AS traffic_share_pct
FROM web_events.page_views
GROUP BY page_url
ORDER BY total_views DESC
LIMIT 10;"""
    },
    {
        "id": "KPI 3.7",
        "title": "UI Component Event Interactions by Element and Action Type",
        "section": "3. Digital Domain KPIs & In-Depth Analytics",
        "domain": "Digital Experience",
        "purpose": "Surfaces granular user interaction behavior across buttons, search inputs, forms, and menus.",
        "formula": "Interactions = COUNT(*) GROUP BY Element, Event Type",
        "grain": "UI Element Interaction Grain",
        "tables": "web_events.events",
        "action": "Redesign UI elements experiencing high click volume but low form submission completion.",
        "sql": """-- KPI 3.7: UI Component Event Interactions by Element and Action Type
SELECT 
    element_id,
    COUNT(event_id) AS total_interactions,
    COUNT(CASE WHEN event_type = 'click' THEN 1 END) AS click_count,
    COUNT(CASE WHEN event_type = 'submit' THEN 1 END) AS submit_count,
    COUNT(CASE WHEN event_type = 'scroll' THEN 1 END) AS scroll_count,
    COUNT(CASE WHEN event_type = 'hover' THEN 1 END) AS hover_count
FROM web_events.events
GROUP BY element_id
ORDER BY total_interactions DESC;"""
    },

    # =========================================================================
    # SECTION 4: LOGISTICS & SUPPLY CHAIN KPIS (7 QUERIES)
    # =========================================================================
    {
        "id": "KPI 4.1",
        "title": "Courier Partner Delivery Volume & 5-Day SLA Benchmark",
        "section": "4. Logistics & Supply Chain Dashboard KPIs",
        "domain": "Logistics & Fulfillment",
        "purpose": "Compares delivery performance, SLA adherence, and lead times across primary courier partners.",
        "formula": "Carrier OTD SLA % = (Parcels Delivered in <= 5 Days / Total Delivered) * 100",
        "grain": "Carrier Grain",
        "tables": "sales.shipments",
        "action": "Enforce penalty deductions or reduce dispatches to carriers breaching agreed SLA thresholds.",
        "sql": """-- KPI 4.1: Courier Partner Delivery Volume & 5-Day SLA Benchmark
SELECT 
    courier_name,
    COUNT(shipment_id) AS total_dispatches,
    COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_count,
    COUNT(CASE WHEN status = 'Shipped' THEN 1 END) AS in_transit_count,
    COUNT(CASE WHEN status = 'Returned' THEN 1 END) AS returned_count,
    ROUND(AVG(CASE WHEN status = 'Delivered' THEN delivered_date - shipped_date END)::numeric, 2) AS avg_lead_days,
    ROUND(COUNT(CASE WHEN status = 'Delivered' AND (delivered_date - shipped_date) <= 5 THEN 1 END)::numeric / 
          NULLIF(COUNT(CASE WHEN status = 'Delivered' THEN 1 END), 0) * 100, 2) AS otd_sla_compliance_pct
FROM sales.shipments
GROUP BY courier_name
ORDER BY delivered_count DESC;"""
    },
    {
        "id": "KPI 4.2",
        "title": "Delivery Lead Time Transit Day Distribution Breakdown",
        "section": "4. Logistics & Supply Chain Dashboard KPIs",
        "domain": "Logistics & Fulfillment",
        "purpose": "Measures the full distribution spectrum of transit durations from next-day to breached SLA.",
        "formula": "Bracket Count = COUNT(*) GROUP BY (delivered_date - shipped_date)",
        "grain": "Lead Time Bracket Grain",
        "tables": "sales.shipments",
        "action": "Investigate logistics bottlenecks responsible for shipments exceeding 5 days in transit.",
        "sql": """-- KPI 4.2: Delivery Lead Time Transit Day Distribution Breakdown
SELECT 
    CASE 
        WHEN (delivered_date - shipped_date) <= 1 THEN '1 Day (Next Day)'
        WHEN (delivered_date - shipped_date) = 2 THEN '2 Days'
        WHEN (delivered_date - shipped_date) = 3 THEN '3 Days'
        WHEN (delivered_date - shipped_date) = 4 THEN '4 Days'
        WHEN (delivered_date - shipped_date) = 5 THEN '5 Days (SLA Cap)'
        ELSE '6+ Days (Breached SLA)'
    END AS transit_bracket,
    COUNT(shipment_id) AS parcel_volume,
    ROUND(COUNT(shipment_id)::numeric / SUM(COUNT(shipment_id)) OVER () * 100, 2) AS volume_pct
FROM sales.shipments
WHERE status = 'Delivered' AND delivered_date >= shipped_date
GROUP BY 1
ORDER BY parcel_volume DESC;"""
    },
    {
        "id": "KPI 4.3",
        "title": "Carrier Transit Lead Time Percentiles (Median P50 & Tail P90)",
        "section": "4. Logistics & Supply Chain Dashboard KPIs",
        "domain": "Logistics & Fulfillment",
        "purpose": "Calculates robust median and 90th percentile delivery latencies to detect long-tail delays.",
        "formula": "P50 = PERCENTILE_CONT(0.5); P90 = PERCENTILE_CONT(0.9)",
        "grain": "Carrier Statistical Grain",
        "tables": "sales.shipments",
        "action": "Audit carrier sorting networks where P90 lead time diverges significantly from P50 median.",
        "sql": """-- KPI 4.3: Carrier Transit Lead Time Percentiles (Median P50 & Tail P90)
SELECT 
    courier_name,
    COUNT(shipment_id) AS evaluated_parcels,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY (delivered_date - shipped_date))::numeric, 1) AS median_lead_time_p50,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY (delivered_date - shipped_date))::numeric, 1) AS tail_lead_time_p90,
    ROUND(AVG(delivered_date - shipped_date)::numeric, 2) AS mean_lead_time_days
FROM sales.shipments
WHERE status = 'Delivered' AND delivered_date >= shipped_date
GROUP BY courier_name
ORDER BY median_lead_time_p50 ASC;"""
    },
    {
        "id": "KPI 4.4",
        "title": "Regional Warehouse Storage Capacity & Snapshot Stock Units",
        "section": "4. Logistics & Supply Chain Dashboard KPIs",
        "domain": "Logistics & Warehousing",
        "purpose": "Evaluates facility storage utilization across the 5 distribution centers.",
        "formula": "Stock Density = Total Snapshot Units / Capacity SqFt",
        "grain": "Warehouse Facility Grain",
        "tables": "supply_chain.warehouses, supply_chain.inventory_snapshots",
        "action": "Rebalance inventory from over-utilized fulfillment hubs to under-utilized regional warehouses.",
        "sql": """-- KPI 4.4: Regional Warehouse Storage Capacity & Snapshot Stock Units
WITH latest_snapshot AS (
    SELECT warehouse_id, MAX(snapshot_date) AS max_date
    FROM supply_chain.inventory_snapshots
    GROUP BY warehouse_id
),
stock AS (
    SELECT s.warehouse_id, SUM(s.quantity_on_hand) AS total_units, COUNT(DISTINCT s.product_id) AS skus_stocked
    FROM supply_chain.inventory_snapshots s
    JOIN latest_snapshot ls ON s.warehouse_id = ls.warehouse_id AND s.snapshot_date = ls.max_date
    GROUP BY s.warehouse_id
)
SELECT 
    w.warehouse_id,
    w.name AS warehouse_name,
    w.region,
    w.capacity_sqft,
    COALESCE(st.total_units, 0) AS units_on_hand,
    COALESCE(st.skus_stocked, 0) AS active_skus,
    ROUND((COALESCE(st.total_units, 0)::numeric / NULLIF(w.capacity_sqft, 0)), 2) AS units_per_sqft
FROM supply_chain.warehouses w
LEFT JOIN stock st ON w.warehouse_id = st.warehouse_id
ORDER BY w.warehouse_id ASC;"""
    },
    {
        "id": "KPI 4.5",
        "title": "Inbound Supplier Procurement Status & Delivery Delay Tracking",
        "section": "4. Logistics & Supply Chain Dashboard KPIs",
        "domain": "Logistics & Procurement",
        "purpose": "Tracks factory procurement receipts, in-transit purchase orders, and delayed supplier shipments.",
        "formula": "Supplier Delay Rate % = (Delayed Lots / Total Lots) * 100",
        "grain": "Procurement Lot Grain",
        "tables": "supply_chain.shipments",
        "action": "Issue formal vendor quality alerts to suppliers with repeat shipment delays.",
        "sql": """-- KPI 4.5: Inbound Supplier Procurement Status & Delivery Delay Tracking
SELECT 
    status AS procurement_status,
    COUNT(shipment_id) AS shipment_lots,
    SUM(quantity) AS total_units_procured,
    ROUND(AVG(COALESCE(arrival_date, CURRENT_DATE) - shipped_date)::numeric, 1) AS avg_procurement_lead_days,
    ROUND(COUNT(shipment_id)::numeric / SUM(COUNT(shipment_id)) OVER () * 100, 2) AS share_pct
FROM supply_chain.shipments
GROUP BY status
ORDER BY shipment_lots DESC;"""
    },
    {
        "id": "KPI 4.6",
        "title": "Retail Store Stockout Vulnerability by Merchandise Category",
        "section": "4. Logistics & Supply Chain Dashboard KPIs",
        "domain": "Logistics & Inventory",
        "purpose": "Identifies retail product categories with highest critical stockout exposure across store shelves.",
        "formula": "Stockout Rate % = (Stockout SKUs / Total SKUs) * 100",
        "grain": "Category Inventory Grain",
        "tables": "products.inventory, products.products, core.dim_brand, core.dim_category",
        "action": "Prioritize direct warehouse-to-store express replenishment for categories with stockout rates >20%.",
        "sql": """-- KPI 4.6: Retail Store Stockout Vulnerability by Merchandise Category
SELECT 
    c.category_name,
    COUNT(i.product_id) AS store_sku_lines,
    COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END) AS stockout_risk_lines,
    ROUND(COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END)::numeric / 
          NULLIF(COUNT(i.product_id), 0) * 100, 2) AS stockout_vulnerability_pct,
    SUM(i.quantity_on_hand) AS total_shelf_units
FROM products.inventory i
JOIN products.products p ON i.product_id = p.product_id
JOIN core.dim_brand b ON p.brand_id = b.brand_id
JOIN core.dim_category c ON b.category_id = c.category_id
GROUP BY c.category_name
ORDER BY stockout_risk_lines DESC;"""
    },
    {
        "id": "KPI 4.7",
        "title": "Order Fulfillment Pipeline: Processing vs Active In-Transit Parcels",
        "section": "4. Logistics & Supply Chain Dashboard KPIs",
        "domain": "Logistics & Fulfillment",
        "purpose": "Monitors order backlog awaiting fulfillment versus parcels currently moving through carrier networks.",
        "formula": "Pipeline = Orders in Processing + Parcels in Shipped status",
        "grain": "Fulfillment Pipeline Grain",
        "tables": "sales.orders, sales.shipments",
        "action": "Add warehouse picking staff when processing order count exceeds 20,000 units.",
        "sql": """-- KPI 4.7: Order Fulfillment Pipeline: Processing vs Active In-Transit Parcels
WITH processing AS (
    SELECT COUNT(*) AS orders_awaiting_dispatch
    FROM sales.orders
    WHERE order_status = 'Processing'
),
in_transit AS (
    SELECT COUNT(*) AS parcels_in_transit
    FROM sales.shipments
    WHERE status = 'Shipped'
)
SELECT 
    p.orders_awaiting_dispatch,
    t.parcels_in_transit,
    (p.orders_awaiting_dispatch + t.parcels_in_transit) AS total_active_fulfillment_pipeline
FROM processing p, in_transit t;"""
    },

    # =========================================================================
    # SECTION 5: CROSS-FUNCTIONAL INTEGRATION KPIS (6 QUERIES)
    # =========================================================================
    {
        "id": "KPI 5.1",
        "title": "Monthly Commercial Alignment: Delivered Revenue vs Marketing Ad Spend",
        "section": "5. Cross-Functional Integration KPIs",
        "domain": "Cross-Functional Yield",
        "purpose": "Audits monthly synchronization between advertising spend and commercial net revenue realization.",
        "formula": "Monthly MER = Monthly Net Revenue / Monthly Ad Spend",
        "grain": "Monthly Cross-Domain Grain",
        "tables": "sales.orders, marketing.ads_spend",
        "action": "Ensure ad spend expansion produces commensurate delivered revenue lift with positive marginal returns.",
        "sql": """-- KPI 5.1: Monthly Commercial Alignment: Delivered Revenue vs Marketing Ad Spend
WITH monthly_rev AS (
    SELECT TO_CHAR(order_date, 'YYYY-MM') AS month_year, ROUND(SUM(net_total), 2) AS revenue
    FROM sales.orders WHERE order_status = 'Delivered' GROUP BY 1
),
monthly_spend AS (
    SELECT TO_CHAR(spend_date, 'YYYY-MM') AS month_year, ROUND(SUM(amount), 2) AS spend
    FROM marketing.ads_spend GROUP BY 1
)
SELECT 
    COALESCE(r.month_year, s.month_year) AS month_year,
    COALESCE(r.revenue, 0) AS delivered_revenue_inr,
    COALESCE(s.spend, 0) AS ad_spend_inr,
    ROUND((COALESCE(r.revenue, 0) / NULLIF(COALESCE(s.spend, 0), 0))::numeric, 2) AS monthly_mer
FROM monthly_rev r
FULL OUTER JOIN monthly_spend s ON r.month_year = s.month_year
ORDER BY month_year ASC;"""
    },
    {
        "id": "KPI 5.2",
        "title": "Digital Identified Web Visitors to Delivered Order Conversion Rate",
        "section": "5. Cross-Functional Integration KPIs",
        "domain": "Cross-Functional Journey",
        "purpose": "Measures commercial conversion yield from identified online web visitors into delivered paying buyers.",
        "formula": "Visitor Conversion % = (Unique Buyers / Unique Identified Web Visitors) * 100",
        "grain": "Customer Conversion Grain",
        "tables": "web_events.page_views, sales.orders",
        "action": "Trigger targeted retargeting emails and discount vouchers for active web visitors who have not purchased.",
        "sql": """-- KPI 5.2: Digital Identified Web Visitors to Delivered Order Conversion Rate
WITH visitors AS (
    SELECT COUNT(DISTINCT customer_id) AS identified_web_visitors
    FROM web_events.page_views
    WHERE customer_id IS NOT NULL
),
buyers AS (
    SELECT COUNT(DISTINCT cust_id) AS active_delivered_buyers
    FROM sales.orders
    WHERE order_status = 'Delivered'
)
SELECT 
    v.identified_web_visitors,
    b.active_delivered_buyers,
    ROUND((b.active_delivered_buyers::numeric / NULLIF(v.identified_web_visitors, 0) * 100), 2) AS visitor_to_buyer_conversion_pct
FROM visitors v, buyers b;"""
    },
    {
        "id": "KPI 5.3",
        "title": "Active Promotional Campaigns & Discount Depth Overview",
        "section": "5. Cross-Functional Integration KPIs",
        "domain": "Cross-Functional Merchandising",
        "purpose": "Audits active retail discount promotions and promotional duration across sales channels.",
        "formula": "Promo Duration Days = (end_date - start_date)",
        "grain": "Promotion Master Grain",
        "tables": "products.promotions",
        "action": "Verify warehouse inventory buffers before launching promotions with discount depth >= 15%.",
        "sql": """-- KPI 5.3: Active Promotional Campaigns & Discount Depth Overview
SELECT 
    promo_id,
    promo_name,
    discount_percent,
    start_date,
    end_date,
    (end_date - start_date) AS promo_duration_days,
    active
FROM products.promotions
WHERE active = true
ORDER BY discount_percent DESC, start_date DESC
LIMIT 10;"""
    },
    {
        "id": "KPI 5.4",
        "title": "Customer Product Return Rate & Commercial Refund Outflow",
        "section": "5. Cross-Functional Integration KPIs",
        "domain": "Cross-Functional Quality",
        "purpose": "Quantifies revenue erosion and customer dissatisfaction from merchandise returns.",
        "formula": "Return Rate % = (Unique Returned Orders / Total Delivered Orders) * 100",
        "grain": "Return Item Grain",
        "tables": "sales.returns, sales.orders",
        "action": "Audit supplier quality controls for products generating return rates exceeding 7%.",
        "sql": """-- KPI 5.4: Customer Product Return Rate & Commercial Refund Outflow
WITH totals AS (
    SELECT COUNT(DISTINCT order_id) AS total_delivered_orders
    FROM sales.orders
    WHERE order_status = 'Delivered'
),
returns AS (
    SELECT 
        COUNT(return_id) AS total_returned_items,
        COUNT(DISTINCT order_id) AS returned_orders_count,
        ROUND(SUM(refund_amount), 2) AS total_refund_inflow_inr,
        ROUND(AVG(refund_amount), 2) AS avg_refund_amount_inr
    FROM sales.returns
)
SELECT 
    t.total_delivered_orders,
    r.returned_orders_count,
    r.total_returned_items,
    r.total_refund_inflow_inr,
    ROUND((r.returned_orders_count::numeric / NULLIF(t.total_delivered_orders, 0) * 100), 2) AS order_return_rate_pct
FROM totals t, returns r;"""
    },
    {
        "id": "KPI 5.5",
        "title": "Product Return Root-Cause Defect Analysis by Merchandise Category",
        "section": "5. Cross-Functional Integration KPIs",
        "domain": "Cross-Functional Quality",
        "purpose": "Identifies category-specific return drivers (defects, sizing, late delivery) eroding revenue.",
        "formula": "Refund Cost = SUM(refund_amount) GROUP BY Category, Reason",
        "grain": "Category × Return Reason Grain",
        "tables": "sales.returns, products.products, core.dim_brand, core.dim_category",
        "action": "Mandate vendor quality re-inspections for categories where 'Defective' represents >30% of refunds.",
        "sql": """-- KPI 5.5: Product Return Root-Cause Defect Analysis by Merchandise Category
SELECT 
    c.category_name,
    r.reason AS return_reason,
    COUNT(r.return_id) AS return_count,
    ROUND(SUM(r.refund_amount), 2) AS total_refund_cost_inr,
    ROUND(AVG(r.refund_amount), 2) AS avg_refund_inr
FROM sales.returns r
JOIN products.products p ON r.prod_id = p.product_id
JOIN core.dim_brand b ON p.brand_id = b.brand_id
JOIN core.dim_category c ON b.category_id = c.category_id
GROUP BY c.category_name, r.reason
ORDER BY total_refund_cost_inr DESC
LIMIT 12;"""
    },
    {
        "id": "KPI 5.6",
        "title": "Operational Commercial Realization vs Order Pipeline Leakage",
        "section": "5. Cross-Functional Integration KPIs",
        "domain": "Cross-Functional Governance",
        "purpose": "Analyzes realization of gross commercial potential versus order cancellations and failures.",
        "formula": "State Share % = (Value per Status / Total Potential Value) * 100",
        "grain": "Order Fulfillment State Grain",
        "tables": "sales.orders",
        "action": "Implement automated SMS re-engagement for payment-failed orders to recover dropped revenue.",
        "sql": """-- KPI 5.6: Operational Commercial Realization vs Order Pipeline Leakage
SELECT 
    order_status,
    COUNT(order_id) AS order_count,
    ROUND(SUM(net_total), 2) AS net_value_inr,
    ROUND(SUM(net_total) / 10000000.0, 2) AS net_value_crores,
    ROUND(SUM(net_total)::numeric / SUM(SUM(net_total)) OVER () * 100, 2) AS value_share_pct
FROM sales.orders
GROUP BY order_status
ORDER BY net_value_inr DESC;"""
    },

    # =========================================================================
    # SECTION 6: EXPLORATORY DATA ANALYSIS (EDA) DEEP-DIVES (8 QUERIES)
    # =========================================================================
    {
        "id": "EDA 6.1",
        "title": "Marketing Spend Seasonality & Platform Investment Sensitivity",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Marketing Pacing",
        "purpose": "Evaluates platform spend variance across quarters to detect acquisition cost swings.",
        "formula": "Quarterly Spend = SUM(amount) GROUP BY Quarter, Platform",
        "grain": "Quarterly Platform Grain",
        "tables": "marketing.ads_spend",
        "action": "Establish quarter-specific budget pacing guidelines to protect ad yield.",
        "sql": """-- EDA 6.1: Marketing Spend Seasonality & Platform Investment Sensitivity
SELECT 
    EXTRACT(YEAR FROM spend_date) AS spend_year,
    EXTRACT(QUARTER FROM spend_date) AS spend_quarter,
    platform,
    COUNT(spend_id) AS spend_events,
    ROUND(SUM(amount), 2) AS quarterly_spend_inr,
    ROUND(AVG(amount), 2) AS avg_daily_spend_inr
FROM marketing.ads_spend
GROUP BY EXTRACT(YEAR FROM spend_date), EXTRACT(QUARTER FROM spend_date), platform
ORDER BY spend_year ASC, spend_quarter ASC, quarterly_spend_inr DESC;"""
    },
    {
        "id": "EDA 6.2",
        "title": "Digital Funnel Drop-off Friction Analysis (Cart to Checkout Abandonment)",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Digital Funnel",
        "purpose": "Calculates funnel leakages at checkout initiation to locate UX friction points.",
        "formula": "Abandonment Rate % = (1 - Checkout Views / Cart Views) * 100",
        "grain": "Digital Funnel Grain",
        "tables": "web_events.page_views",
        "action": "Introduce guest checkout and one-click payment to reduce cart abandonment.",
        "sql": """-- EDA 6.2: Digital Funnel Drop-off Friction Analysis (Cart to Checkout Abandonment)
SELECT 
    COUNT(CASE WHEN page_url = '/cart' THEN 1 END) AS cart_views,
    COUNT(CASE WHEN page_url = '/checkout' THEN 1 END) AS checkout_views,
    (COUNT(CASE WHEN page_url = '/cart' THEN 1 END) - COUNT(CASE WHEN page_url = '/checkout' THEN 1 END)) AS abandoned_carts,
    ROUND((1 - COUNT(CASE WHEN page_url = '/checkout' THEN 1 END)::numeric / 
           NULLIF(COUNT(CASE WHEN page_url = '/cart' THEN 1 END), 0)) * 100, 2) AS cart_abandonment_rate_pct
FROM web_events.page_views;"""
    },
    {
        "id": "EDA 6.3",
        "title": "Mobile vs Desktop Digital Experience & Interaction Depth",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Digital UX",
        "purpose": "Examines engagement intensity differences between mobile handheld and desktop shoppers.",
        "formula": "Depth = Total Views / Unique Sessions per Device",
        "grain": "Device Segmentation Grain",
        "tables": "web_events.page_views",
        "action": "Optimize responsive mobile menus if mobile sessions exhibit shallower browsing depth.",
        "sql": """-- EDA 6.3: Mobile vs Desktop Digital Experience & Interaction Depth
SELECT 
    device_type,
    COUNT(view_id) AS total_views,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(DISTINCT customer_id) AS identified_customers,
    ROUND(COUNT(view_id)::numeric / NULLIF(COUNT(DISTINCT session_id), 0), 2) AS pages_per_session,
    ROUND(COUNT(DISTINCT customer_id)::numeric / NULLIF(COUNT(DISTINCT session_id), 0) * 100, 2) AS auth_user_ratio_pct
FROM web_events.page_views
GROUP BY device_type;"""
    },
    {
        "id": "EDA 6.4",
        "title": "Carrier SLA Lead Time Bottlenecks & Tail Delay Outliers",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Logistics Reliability",
        "purpose": "Identifies severe shipping delays (>= 8 transit days) to highlight systemic courier failures.",
        "formula": "Severe Delay Rate = (Parcels with Lead Days >= 8 / Total Parcels) * 100",
        "grain": "Courier Outlier Grain",
        "tables": "sales.shipments",
        "action": "Issue formal breach penalties to carriers with severe delay rates > 2%.",
        "sql": """-- EDA 6.4: Carrier SLA Lead Time Bottlenecks & Tail Delay Outliers
SELECT 
    courier_name,
    COUNT(shipment_id) AS delivered_parcels,
    COUNT(CASE WHEN (delivered_date - shipped_date) >= 8 THEN 1 END) AS severe_delay_parcels,
    ROUND(COUNT(CASE WHEN (delivered_date - shipped_date) >= 8 THEN 1 END)::numeric / 
          NULLIF(COUNT(shipment_id), 0) * 100, 2) AS severe_delay_pct,
    MAX(delivered_date - shipped_date) AS worst_case_transit_days
FROM sales.shipments
WHERE status = 'Delivered' AND delivered_date >= shipped_date
GROUP BY courier_name
ORDER BY severe_delay_pct DESC;"""
    },
    {
        "id": "EDA 6.5",
        "title": "Inbound Supplier Procurement Transit Days by Supplier",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Supply Chain",
        "purpose": "Evaluates supplier fulfillment velocity and reliability across manufacturing vendors.",
        "formula": "Avg Inbound Lead Days = AVG(arrival_date - shipped_date)",
        "grain": "Supplier Inbound Grain",
        "tables": "supply_chain.shipments, products.suppliers",
        "action": "Reallocate procurement POs to vendors with consistently shorter lead times.",
        "sql": """-- EDA 6.5: Inbound Supplier Procurement Transit Days by Supplier
SELECT 
    sup.supplier_id,
    sup.supplier_name,
    sup.city,
    COUNT(s.shipment_id) AS total_lots_shipped,
    COUNT(CASE WHEN s.status = 'Delayed' THEN 1 END) AS delayed_lots,
    ROUND(AVG(COALESCE(s.arrival_date, CURRENT_DATE) - s.shipped_date)::numeric, 1) AS avg_transit_days
FROM supply_chain.shipments s
JOIN products.suppliers sup ON s.supplier_id = sup.supplier_id
GROUP BY sup.supplier_id, sup.supplier_name, sup.city
ORDER BY delayed_lots DESC, total_lots_shipped DESC
LIMIT 10;"""
    },
    {
        "id": "EDA 6.6",
        "title": "Store Stockout Vulnerability Concentration across Retail Regions",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Inventory Exposure",
        "purpose": "Locates regional retail territories facing the highest stockout exposure.",
        "formula": "Regional Stockout % = (Critical SKUs / Total SKUs in Region) * 100",
        "grain": "Region Inventory Grain",
        "tables": "products.inventory, stores.stores, core.dim_region",
        "action": "Prioritize direct inter-store transfers within vulnerable retail regions.",
        "sql": """-- EDA 6.6: Store Stockout Vulnerability Concentration across Retail Regions
SELECT 
    r.region_name,
    r.country,
    COUNT(DISTINCT s.store_id) AS retail_stores,
    COUNT(i.product_id) AS total_store_skus,
    COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END) AS critical_stockout_skus,
    ROUND(COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END)::numeric / 
          NULLIF(COUNT(i.product_id), 0) * 100, 2) AS regional_stockout_pct
FROM products.inventory i
JOIN stores.stores s ON i.store_id = s.store_id
JOIN core.dim_region r ON s.region_id = r.region_id
GROUP BY r.region_name, r.country
ORDER BY critical_stockout_skus DESC;"""
    },
    {
        "id": "EDA 6.7",
        "title": "Order Payment Mode Adoption & Commercial Failure Rates",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Commercial Leakage",
        "purpose": "Evaluates which payment methods experience highest payment drop-offs and failure rates.",
        "formula": "Failure Rate % = (Failed Orders / Total Orders) * 100",
        "grain": "Payment Mode Grain",
        "tables": "sales.orders, finance.payment_modes",
        "action": "Implement redundant payment gateways for payment tenders showing failure rates > 6%.",
        "sql": """-- EDA 6.7: Order Payment Mode Adoption & Commercial Failure Rates
SELECT 
    pm.mode_name AS payment_mode,
    COUNT(o.order_id) AS total_orders,
    COUNT(CASE WHEN o.order_status = 'Delivered' THEN 1 END) AS successful_orders,
    COUNT(CASE WHEN o.order_status = 'Failed' THEN 1 END) AS failed_orders,
    ROUND(COUNT(CASE WHEN o.order_status = 'Failed' THEN 1 END)::numeric / 
          NULLIF(COUNT(o.order_id), 0) * 100, 2) AS payment_failure_rate_pct,
    ROUND(SUM(o.net_total), 2) AS total_order_value_inr
FROM sales.orders o
JOIN finance.payment_modes pm ON o.payment_mode_id = pm.mode_id
GROUP BY pm.mode_name
ORDER BY total_orders DESC;"""
    },
    {
        "id": "EDA 6.8",
        "title": "Merchandise Return Reasons Impact by Product Price Quintiles",
        "section": "6. Exploratory Data Analysis (EDA) Deep-Dive Questions",
        "domain": "EDA & Product Economics",
        "purpose": "Examines whether high-ticket luxury merchandise suffers higher return propensities.",
        "formula": "Return Rate across Price Quintiles NTILE(5)",
        "grain": "Product Price Quintile Grain",
        "tables": "sales.returns, products.products",
        "action": "Enhance product sizing guides and premium packaging for top-quintile luxury items.",
        "sql": """-- EDA 6.8: Merchandise Return Reasons Impact by Product Price Quintiles
WITH priced_products AS (
    SELECT 
        product_id,
        price,
        NTILE(5) OVER (ORDER BY price ASC) AS price_quintile
    FROM products.products
)
SELECT 
    pp.price_quintile,
    COUNT(r.return_id) AS returned_items_count,
    ROUND(MIN(pp.price), 2) AS min_quintile_price,
    ROUND(MAX(pp.price), 2) AS max_quintile_price,
    ROUND(SUM(r.refund_amount), 2) AS total_refunds_inr,
    ROUND(AVG(r.refund_amount), 2) AS avg_refund_per_return
FROM sales.returns r
JOIN priced_products pp ON r.prod_id = pp.product_id
GROUP BY pp.price_quintile
ORDER BY pp.price_quintile ASC;"""
    }
]
