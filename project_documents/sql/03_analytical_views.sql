-- ============================================================================
-- RetailMart V3 - Analytical Semantic Views (PostgreSQL 18)
-- Clean, parameterizable views providing analytical aggregates for Django services
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS analytics;

-- 1. Monthly Delivered Sales & Trends
DROP VIEW IF EXISTS analytics.vw_monthly_sales_summary CASCADE;
CREATE VIEW analytics.vw_monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', o.order_date)::date AS sales_month,
    COUNT(o.order_id) AS total_orders,
    SUM(o.net_total) AS total_net_revenue,
    SUM(o.gross_total) AS total_gross_revenue,
    SUM(o.discount_amount) AS total_discounts,
    ROUND(AVG(o.net_total)::numeric, 2) AS aov,
    COUNT(DISTINCT o.cust_id) AS active_customers
FROM sales.orders o
WHERE o.order_status = 'Delivered'
GROUP BY DATE_TRUNC('month', o.order_date);

-- 2. Category Sales Performance
DROP VIEW IF EXISTS analytics.vw_sales_by_category CASCADE;
CREATE VIEW analytics.vw_sales_by_category AS
SELECT 
    c.category_id,
    c.category_name,
    COUNT(DISTINCT oi.order_id) AS order_count,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.net_amount) AS net_revenue,
    ROUND(SUM(oi.net_amount)::numeric / NULLIF(SUM(oi.quantity), 0), 2) AS avg_selling_price
FROM sales.order_items oi
JOIN sales.orders o ON oi.order_id = o.order_id
JOIN products.products p ON oi.prod_id = p.product_id
JOIN core.dim_brand b ON p.brand_id = b.brand_id
JOIN core.dim_category c ON b.category_id = c.category_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_id, c.category_name;

-- 3. Regional Sales Performance
DROP VIEW IF EXISTS analytics.vw_sales_by_region CASCADE;
CREATE VIEW analytics.vw_sales_by_region AS
SELECT 
    r.region_id,
    r.region_name,
    r.state,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.net_total) AS net_revenue,
    ROUND(AVG(o.net_total)::numeric, 2) AS aov,
    COUNT(DISTINCT o.cust_id) AS unique_customers
FROM sales.orders o
JOIN stores.stores s ON o.store_id = s.store_id
JOIN core.dim_region r ON s.region_id = r.region_id
WHERE o.order_status = 'Delivered'
GROUP BY r.region_id, r.region_name, r.state;

-- 4. Payment Mode Distribution
DROP VIEW IF EXISTS analytics.vw_sales_by_payment_mode CASCADE;
CREATE VIEW analytics.vw_sales_by_payment_mode AS
SELECT 
    pm.mode_id,
    pm.mode_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.net_total) AS net_revenue,
    ROUND(AVG(o.net_total)::numeric, 2) AS aov
FROM sales.orders o
JOIN finance.payment_modes pm ON o.payment_mode_id = pm.mode_id
WHERE o.order_status = 'Delivered'
GROUP BY pm.mode_id, pm.mode_name;

-- 5. Customer RFM Scoring
DROP VIEW IF EXISTS analytics.vw_customer_rfm_scores CASCADE;
CREATE VIEW analytics.vw_customer_rfm_scores AS
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
    s.*,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Recent New'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Hibernating'
        ELSE 'Potential Loyalist'
    END AS rfm_segment
FROM scored s;

-- 6. Courier Delivery SLA & Transit Performance
DROP VIEW IF EXISTS analytics.vw_courier_sla_performance CASCADE;
CREATE VIEW analytics.vw_courier_sla_performance AS
SELECT 
    sh.courier_name,
    COUNT(sh.shipment_id) AS total_shipments,
    COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END) AS delivered_shipments,
    ROUND(AVG(CASE WHEN sh.status = 'Delivered' THEN sh.delivered_date - sh.shipped_date END)::numeric, 2) AS avg_lead_days,
    ROUND(
        COUNT(CASE WHEN sh.status = 'Delivered' AND (sh.delivered_date - sh.shipped_date) <= 5 THEN 1 END)::numeric 
        / NULLIF(COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END), 0) * 100, 
        2
    ) AS on_time_sla_pct
FROM sales.shipments sh
GROUP BY sh.courier_name;

-- 7. Store Inventory Availability & Stock-out Risk
DROP VIEW IF EXISTS analytics.vw_store_inventory_risk CASCADE;
CREATE VIEW analytics.vw_store_inventory_risk AS
SELECT 
    s.store_id,
    s.store_name,
    r.region_name,
    COUNT(i.product_id) AS total_tracked_skus,
    COUNT(CASE WHEN i.quantity_on_hand = 0 THEN 1 END) AS out_of_stock_skus,
    COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level AND i.quantity_on_hand > 0 THEN 1 END) AS low_stock_skus,
    SUM(i.quantity_on_hand) AS total_units_on_hand
FROM products.inventory i
JOIN stores.stores s ON i.store_id = s.store_id
JOIN core.dim_region r ON s.region_id = r.region_id
GROUP BY s.store_id, s.store_name, r.region_name;

-- 8. Factory Quality & Scrap Analysis
DROP VIEW IF EXISTS analytics.vw_mfg_quality_metrics CASCADE;
CREATE VIEW analytics.vw_mfg_quality_metrics AS
SELECT 
    pl.line_id,
    pl.line_name,
    COUNT(wo.work_order_id) AS total_batches,
    SUM(wo.quantity_produced) AS total_produced,
    SUM(wo.rejected_quantity) AS total_rejected,
    ROUND(SUM(wo.rejected_quantity)::numeric / NULLIF(SUM(wo.quantity_produced), 0) * 100, 2) AS rejection_rate_pct
FROM manufacture.work_orders wo
JOIN manufacture.production_lines pl ON wo.line_id = pl.line_id
WHERE wo.status = 'Completed'
GROUP BY pl.line_id, pl.line_name;

-- 9. Cross-Functional Return Impact by Category & Courier
DROP VIEW IF EXISTS analytics.vw_cross_return_cost_impact CASCADE;
CREATE VIEW analytics.vw_cross_return_cost_impact AS
SELECT 
    c.category_name,
    sh.courier_name,
    COUNT(DISTINCT o.order_id) AS total_delivered_orders,
    COUNT(DISTINCT r.return_id) AS total_returns,
    ROUND(COUNT(DISTINCT r.return_id)::numeric / NULLIF(COUNT(DISTINCT o.order_id), 0) * 100, 2) AS return_rate_pct,
    SUM(COALESCE(r.refund_amount, 0)) AS total_refund_cost
FROM sales.orders o
JOIN sales.shipments sh ON o.order_id = sh.order_id
JOIN sales.order_items oi ON o.order_id = oi.order_id
JOIN products.products p ON oi.prod_id = p.product_id
JOIN core.dim_brand b ON p.brand_id = b.brand_id
JOIN core.dim_category c ON b.category_id = c.category_id
LEFT JOIN sales.returns r ON oi.order_id = r.order_id AND oi.prod_id = r.prod_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_name, sh.courier_name;
