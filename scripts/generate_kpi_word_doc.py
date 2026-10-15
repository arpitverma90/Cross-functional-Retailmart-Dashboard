#!/usr/bin/env python3
"""
Generate the Word document (.docx) containing approved KPI and EDA SQL queries.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "project_documents", "documentation")
output_file = os.path.join(output_dir, "approved_kpi_and_eda_queries.docx")

doc = Document()

# Page title
title = doc.add_heading("RetailMart V3 Enterprise Analytics", level=0)
subtitle = doc.add_paragraph("Approved KPI & EDA SQL Query Catalogue")
subtitle.runs[0].font.size = Pt(14)
subtitle.runs[0].font.color.rgb = RGBColor(0x18, 0x3A, 0x5F)

doc.add_paragraph("Authoritative SQL Query Catalogue for Executive, Sales, Customer, Operations, and Cross-Functional Dashboards.\nDatabase: PostgreSQL 18.4 (accio_retailmart_27)")

doc.add_heading("1. Executive Summary & Sales KPIs", level=1)

queries = [
    ("KPI 1: Delivered Net Revenue (Authoritative Headline)", 
"""-- Recognized commercial net revenue on delivered orders
SELECT 
    DATE_TRUNC('month', order_date)::date AS sales_month,
    COUNT(order_id) AS delivered_orders,
    SUM(net_total) AS total_net_revenue,
    ROUND(SUM(net_total) / 10000000.0, 2) AS net_revenue_crores,
    ROUND(AVG(net_total), 2) AS aov
FROM sales.orders
WHERE order_status = 'Delivered'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY sales_month;"""),

    ("KPI 2: Product Category Contribution & Gross Margin",
"""-- Net revenue, units, and margin contribution by product category
SELECT 
    c.category_id,
    c.category_name,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.net_amount) AS net_revenue,
    SUM(oi.quantity * p.cost_price) AS cogs,
    ROUND((SUM(oi.net_amount) - SUM(oi.quantity * p.cost_price)) / NULLIF(SUM(oi.net_amount), 0) * 100, 2) AS gross_margin_pct
FROM sales.order_items oi
JOIN sales.orders o ON oi.order_id = o.order_id
JOIN products.products p ON oi.prod_id = p.product_id
JOIN core.dim_brand b ON p.brand_id = b.brand_id
JOIN core.dim_category c ON b.category_id = c.category_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_id, c.category_name
ORDER BY net_revenue DESC;"""),

    ("KPI 3: Customer RFM Segmentation & Valuation",
"""-- RFM segmentation using quintile scoring
WITH customer_orders AS (
    SELECT 
        cust_id,
        MAX(order_date) AS last_order_date,
        COUNT(order_id) AS order_frequency,
        SUM(net_total) AS monetary_value
    FROM sales.orders
    WHERE order_status = 'Delivered'
    GROUP BY cust_id
),
scored AS (
    SELECT 
        cust_id,
        ('2026-02-26'::date - last_order_date) AS recency_days,
        order_frequency,
        monetary_value,
        NTILE(5) OVER (ORDER BY ('2026-02-26'::date - last_order_date) DESC) AS r_score,
        NTILE(5) OVER (ORDER BY order_frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM customer_orders
)
SELECT 
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Recent New'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Hibernating'
        ELSE 'Potential Loyalist'
    END AS rfm_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(order_frequency), 1) AS avg_frequency,
    ROUND(SUM(monetary_value) / 10000000.0, 2) AS total_spend_crores
FROM scored
GROUP BY 1
ORDER BY total_spend_crores DESC;"""),

    ("KPI 4: Courier Delivery Lead Time & SLA Performance",
"""-- Logistics delivery fulfillment against 5-day SLA
SELECT 
    sh.courier_name,
    COUNT(sh.shipment_id) AS total_shipments,
    COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END) AS delivered_count,
    ROUND(AVG(CASE WHEN sh.status = 'Delivered' THEN sh.delivered_date - sh.shipped_date END)::numeric, 2) AS avg_lead_days,
    ROUND(
        COUNT(CASE WHEN sh.status = 'Delivered' AND (sh.delivered_date - sh.shipped_date) <= 5 THEN 1 END)::numeric 
        / NULLIF(COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END), 0) * 100, 
        2
    ) AS on_time_sla_pct
FROM sales.shipments sh
GROUP BY sh.courier_name
ORDER BY total_shipments DESC;"""),

    ("KPI 5: Store Stock-Out Risk & Shelf Availability",
"""-- Critical inventory levels by retail store and region
SELECT 
    r.region_name,
    COUNT(DISTINCT s.store_id) AS total_stores,
    COUNT(i.product_id) AS total_inventory_slots,
    COUNT(CASE WHEN i.quantity_on_hand = 0 THEN 1 END) AS out_of_stock_count,
    COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level AND i.quantity_on_hand > 0 THEN 1 END) AS low_stock_count,
    ROUND(COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END)::numeric / COUNT(i.product_id) * 100, 2) AS at_risk_pct
FROM products.inventory i
JOIN stores.stores s ON i.store_id = s.store_id
JOIN core.dim_region r ON s.region_id = r.region_id
GROUP BY r.region_name
ORDER BY at_risk_pct DESC;"""),

    ("KPI 6: Manufacturing Scrap & Rejection Quality",
"""-- Factory quality control metrics by production line
SELECT 
    pl.line_id,
    pl.line_name,
    COUNT(wo.work_order_id) AS total_batches,
    SUM(wo.quantity_produced) AS total_produced,
    SUM(wo.rejected_quantity) AS total_rejected,
    ROUND(SUM(wo.rejected_quantity)::numeric / NULLIF(SUM(wo.quantity_produced), 0) * 100, 2) AS scrap_rate_pct
FROM manufacture.work_orders wo
JOIN manufacture.production_lines pl ON wo.line_id = pl.line_id
WHERE wo.status = 'Completed'
GROUP BY pl.line_id, pl.line_name
ORDER BY scrap_rate_pct DESC;"""),

    ("KPI 7: Cross-Functional Return Impact by Reason & Category",
"""-- Customer return cost impact and reason analysis
SELECT 
    c.category_name,
    r.reason,
    COUNT(r.return_id) AS return_count,
    SUM(r.refund_amount) AS total_refund_amount,
    ROUND(AVG(r.refund_amount), 2) AS avg_refund_amount
FROM sales.returns r
JOIN products.products p ON r.prod_id = p.product_id
JOIN core.dim_brand b ON p.brand_id = b.brand_id
JOIN core.dim_category c ON b.category_id = c.category_id
GROUP BY c.category_name, r.reason
ORDER BY total_refund_amount DESC;""")
]

for q_title, q_sql in queries:
    doc.add_heading(q_title, level=2)
    p = doc.add_paragraph()
    run = p.add_run(q_sql)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x0F, 0x1F, 0x33)

doc.save(output_file)
print("Approved KPI and EDA Word document generated:", output_file)
