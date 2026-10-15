"""
RetailMart V3 - Marketing Service Module
Provides parameterized PostgreSQL queries for Marketing Dashboard:
- Campaigns, Budgets, and Ad Spend by Platform
- Email Marketing Engagement (Sent, Opened, Clicked)
- Campaign Pacing and Budget Utilization
- Time-series Spend Trajectories
"""

from .db_service import execute_query, execute_one, execute_scalar


def get_marketing_kpis(filters):
    """
    Computes headline KPIs for the Marketing domain:
    - Total Ad Spend
    - Total Campaigns
    - Total Campaign Budget
    - Budget Utilization Rate
    - Email Open Rate
    - Email Click-Through Rate (CTR)
    """
    params = []
    where_spend = ["1=1"]
    where_campaign = ["1=1"]
    where_email = ["1=1"]
    
    if filters.get('start_date'):
        where_spend.append("spend_date >= %s")
        where_campaign.append("start_date >= %s")
        where_email.append("sent_date >= %s")
        params.append(filters['start_date'])
        
    if filters.get('end_date'):
        where_spend.append("spend_date <= %s")
        where_campaign.append("end_date <= %s")
        where_email.append("sent_date <= %s")
        params.append(filters['end_date'])

    # Total Spend & Platform Count
    spend_sql = f"""
        SELECT 
            COALESCE(SUM(amount), 0) AS total_spend,
            COUNT(DISTINCT campaign_id) AS active_campaigns_count,
            COUNT(DISTINCT platform) AS platform_count
        FROM marketing.ads_spend
        WHERE {' AND '.join(where_spend)};
    """
    spend_data = execute_one(spend_sql, params) or {}
    total_spend = spend_data.get('total_spend', 0.0)

    # Total Campaign Budget & Count
    camp_sql = f"""
        SELECT 
            COALESCE(SUM(budget), 0) AS total_budget,
            COUNT(*) AS total_campaigns
        FROM marketing.campaigns
        WHERE {' AND '.join(where_campaign)};
    """
    camp_data = execute_one(camp_sql, params) or {}
    total_budget = camp_data.get('total_budget', 0.0)
    total_campaigns = camp_data.get('total_campaigns', 0)

    # Budget Utilization %
    budget_utilization = round((total_spend / total_budget * 100), 2) if total_budget > 0 else 0.0

    # Email Engagement
    email_sql = f"""
        SELECT 
            COALESCE(SUM(emails_sent), 0) AS total_sent,
            COALESCE(SUM(emails_opened), 0) AS total_opened,
            COALESCE(SUM(emails_clicked), 0) AS total_clicked
        FROM marketing.email_clicks
        WHERE {' AND '.join(where_email)};
    """
    email_data = execute_one(email_sql, params) or {}
    total_sent = email_data.get('total_sent', 0)
    total_opened = email_data.get('total_opened', 0)
    total_clicked = email_data.get('total_clicked', 0)

    open_rate = round((total_opened / total_sent * 100), 2) if total_sent > 0 else 0.0
    ctr = round((total_clicked / total_opened * 100), 2) if total_opened > 0 else 0.0
    overall_ctr = round((total_clicked / total_sent * 100), 2) if total_sent > 0 else 0.0

    return {
        'total_spend': total_spend,
        'total_budget': total_budget,
        'total_campaigns': total_campaigns,
        'budget_utilization': budget_utilization,
        'total_sent': total_sent,
        'total_opened': total_opened,
        'total_clicked': total_clicked,
        'open_rate': open_rate,
        'ctr': ctr,
        'overall_ctr': overall_ctr,
        'platform_count': spend_data.get('platform_count', 5),
    }


def get_spend_by_platform(filters):
    """Spend and share breakdown by marketing platform."""
    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("spend_date >= %s")
        params.append(filters['start_date'])
    if filters.get('end_date'):
        where.append("spend_date <= %s")
        params.append(filters['end_date'])

    sql = f"""
        SELECT 
            platform,
            COUNT(*) AS spend_records,
            COUNT(DISTINCT campaign_id) AS campaigns_count,
            ROUND(SUM(amount)::numeric, 2) AS total_amount,
            ROUND(AVG(amount)::numeric, 2) AS avg_daily_amount
        FROM marketing.ads_spend
        WHERE {' AND '.join(where)}
        GROUP BY platform
        ORDER BY total_amount DESC;
    """
    return execute_query(sql, params)


def get_monthly_spend_trend(filters):
    """Monthly marketing ad spend trend by platform."""
    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("spend_date >= %s")
        params.append(filters['start_date'])
    if filters.get('end_date'):
        where.append("spend_date <= %s")
        params.append(filters['end_date'])

    sql = f"""
        SELECT 
            TO_CHAR(spend_date, 'YYYY-MM') AS month_year,
            ROUND(SUM(amount)::numeric, 2) AS total_spend,
            ROUND(SUM(CASE WHEN platform = 'Facebook' THEN amount ELSE 0 END)::numeric, 2) AS facebook_spend,
            ROUND(SUM(CASE WHEN platform = 'Google' THEN amount ELSE 0 END)::numeric, 2) AS google_spend,
            ROUND(SUM(CASE WHEN platform = 'Twitter' THEN amount ELSE 0 END)::numeric, 2) AS twitter_spend,
            ROUND(SUM(CASE WHEN platform = 'LinkedIn' THEN amount ELSE 0 END)::numeric, 2) AS linkedin_spend,
            ROUND(SUM(CASE WHEN platform = 'Instagram' THEN amount ELSE 0 END)::numeric, 2) AS instagram_spend
        FROM marketing.ads_spend
        WHERE {' AND '.join(where)}
        GROUP BY TO_CHAR(spend_date, 'YYYY-MM')
        ORDER BY month_year ASC;
    """
    return execute_query(sql, params)


def get_top_campaigns(filters, limit=10):
    """Top marketing campaigns ranked by total ad spend and budget pacing."""
    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("s.spend_date >= %s")
        params.append(filters['start_date'])
    if filters.get('end_date'):
        where.append("s.spend_date <= %s")
        params.append(filters['end_date'])

    sql = f"""
        SELECT 
            c.campaign_id,
            c.campaign_name,
            c.start_date,
            c.end_date,
            ROUND(c.budget::numeric, 2) AS budget,
            ROUND(COALESCE(SUM(s.amount), 0)::numeric, 2) AS total_spend,
            ROUND((COALESCE(SUM(s.amount), 0) / NULLIF(c.budget, 0) * 100)::numeric, 2) AS utilization_pct,
            COUNT(DISTINCT s.platform) AS platform_reach
        FROM marketing.campaigns c
        LEFT JOIN marketing.ads_spend s ON c.campaign_id = s.campaign_id
        WHERE {' AND '.join(where)}
        GROUP BY c.campaign_id, c.campaign_name, c.start_date, c.end_date, c.budget
        ORDER BY total_spend DESC
        LIMIT {int(limit)};
    """
    return execute_query(sql, params)


def get_email_engagement_trend(filters):
    """Monthly email marketing engagement metrics."""
    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("sent_date >= %s")
        params.append(filters['start_date'])
    if filters.get('end_date'):
        where.append("sent_date <= %s")
        params.append(filters['end_date'])

    sql = f"""
        SELECT 
            TO_CHAR(sent_date, 'YYYY-MM') AS month_year,
            SUM(emails_sent) AS sent,
            SUM(emails_opened) AS opened,
            SUM(emails_clicked) AS clicked,
            ROUND((SUM(emails_opened)::numeric / NULLIF(SUM(emails_sent), 0) * 100), 2) AS open_rate,
            ROUND((SUM(emails_clicked)::numeric / NULLIF(SUM(emails_opened), 0) * 100), 2) AS click_rate
        FROM marketing.email_clicks
        WHERE {' AND '.join(where)}
        GROUP BY TO_CHAR(sent_date, 'YYYY-MM')
        ORDER BY month_year ASC;
    """
    return execute_query(sql, params)
