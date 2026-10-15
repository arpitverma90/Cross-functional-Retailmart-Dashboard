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

-- 10. HR Attendance & Compliance Summary
DROP VIEW IF EXISTS analytics.vw_hr_attendance_summary CASCADE;
CREATE VIEW analytics.vw_hr_attendance_summary AS
WITH emp_monthly AS (
    SELECT 
        DATE_TRUNC('month', attendance_date)::date AS attend_month,
        employee_id,
        COUNT(*) AS days_present,
        ROUND((COUNT(*)::numeric / 22.0 * 100), 2) AS attendance_pct,
        ROUND(AVG(EXTRACT(EPOCH FROM (check_out - check_in)) / 3600.0)::numeric, 2) AS avg_hours_per_day
    FROM hr.attendance
    WHERE check_in IS NOT NULL AND check_out IS NOT NULL
    GROUP BY DATE_TRUNC('month', attendance_date), employee_id
)
SELECT 
    attend_month,
    employee_id,
    days_present,
    attendance_pct,
    avg_hours_per_day
FROM emp_monthly;

-- 11. Departmental Payroll Cost Breakdown
DROP VIEW IF EXISTS analytics.vw_payroll_department_cost CASCADE;
CREATE VIEW analytics.vw_payroll_department_cost AS
SELECT 
    d.dept_name AS department,
    COUNT(DISTINCT ps.employee_id) AS employees_paid,
    ROUND(SUM(ps.basic_salary)::numeric, 2) AS total_basic,
    ROUND(SUM(ps.hra)::numeric, 2) AS total_hra,
    ROUND(SUM(ps.other_allowances)::numeric, 2) AS total_allowances,
    ROUND(SUM(ps.gross_salary)::numeric, 2) AS total_gross,
    ROUND(SUM(ps.pf)::numeric, 2) AS total_pf,
    ROUND(SUM(ps.professional_tax)::numeric, 2) AS total_prof_tax,
    ROUND(SUM(ps.income_tax)::numeric, 2) AS total_income_tax,
    ROUND((SUM(ps.pf) + SUM(ps.professional_tax) + SUM(ps.income_tax))::numeric, 2) AS total_deductions,
    ROUND(SUM(ps.net_salary)::numeric, 2) AS total_net,
    ROUND(((SUM(ps.pf) + SUM(ps.professional_tax) + SUM(ps.income_tax)) / NULLIF(SUM(ps.gross_salary), 0) * 100)::numeric, 2) AS deduction_pct
FROM payroll.pay_slips ps
JOIN stores.employees e ON ps.employee_id = e.employee_id
JOIN core.dim_department d ON e.dept_id = d.dept_id
GROUP BY d.dept_name;

-- 12. HR Salary Payment History
DROP VIEW IF EXISTS analytics.vw_hr_salary_payment_history CASCADE;
CREATE VIEW analytics.vw_hr_salary_payment_history AS
SELECT 
    TO_CHAR(payment_date, 'Mon YYYY') AS month_name,
    DATE_TRUNC('month', payment_date)::date AS payment_month,
    status AS payment_status,
    COUNT(payment_id) AS payment_count,
    COUNT(DISTINCT employee_id) AS employees,
    ROUND(SUM(amount)::numeric, 2) AS total_amount,
    ROUND((SUM(amount) / 10000000.0)::numeric, 2) AS amount_crores
FROM hr.salary_history
GROUP BY DATE_TRUNC('month', payment_date), TO_CHAR(payment_date, 'Mon YYYY'), status;

-- 13. Finance Monthly Revenue vs Expense Trend
DROP VIEW IF EXISTS analytics.vw_finance_revenue_vs_expense CASCADE;
CREATE VIEW analytics.vw_finance_revenue_vs_expense AS
WITH rev AS (
    SELECT 
        DATE_TRUNC('month', order_date)::date AS month_date,
        SUM(net_total) AS total_revenue
    FROM sales.orders
    WHERE order_status = 'Delivered'
    GROUP BY DATE_TRUNC('month', order_date)
),
fin_exp AS (
    SELECT 
        DATE_TRUNC('month', expense_date)::date AS month_date,
        SUM(amount) AS finance_expenses
    FROM finance.expenses
    GROUP BY DATE_TRUNC('month', expense_date)
),
store_exp AS (
    SELECT 
        DATE_TRUNC('month', expense_date)::date AS month_date,
        SUM(amount) AS store_expenses
    FROM stores.expenses
    GROUP BY DATE_TRUNC('month', expense_date)
),
all_months AS (
    SELECT month_date FROM rev
    UNION
    SELECT month_date FROM fin_exp
    UNION
    SELECT month_date FROM store_exp
),
combined AS (
    SELECT 
        m.month_date,
        TO_CHAR(m.month_date, 'Mon YYYY') AS month_name,
        COALESCE(r.total_revenue, 0) AS total_revenue,
        COALESCE(f.finance_expenses, 0) AS finance_expenses,
        COALESCE(s.store_expenses, 0) AS store_expenses,
        (COALESCE(f.finance_expenses, 0) + COALESCE(s.store_expenses, 0)) AS total_expenses,
        (COALESCE(r.total_revenue, 0) - (COALESCE(f.finance_expenses, 0) + COALESCE(s.store_expenses, 0))) AS net_profit
    FROM all_months m
    LEFT JOIN rev r ON m.month_date = r.month_date
    LEFT JOIN fin_exp f ON m.month_date = f.month_date
    LEFT JOIN store_exp s ON m.month_date = s.month_date
)
SELECT 
    month_date,
    month_name,
    ROUND(total_revenue::numeric, 2) AS total_revenue,
    ROUND((total_revenue / 10000000.0)::numeric, 2) AS revenue_crores,
    ROUND(finance_expenses::numeric, 2) AS finance_expenses,
    ROUND(store_expenses::numeric, 2) AS store_expenses,
    ROUND(total_expenses::numeric, 2) AS total_expenses,
    ROUND((total_expenses / 10000000.0)::numeric, 2) AS expenses_crores,
    ROUND(net_profit::numeric, 2) AS net_profit,
    ROUND((net_profit / NULLIF(total_revenue, 0) * 100)::numeric, 2) AS profit_margin_pct,
    ROUND(((total_revenue - LAG(total_revenue) OVER (ORDER BY month_date)) / NULLIF(LAG(total_revenue) OVER (ORDER BY month_date), 0) * 100)::numeric, 2) AS revenue_mom_pct
FROM combined;

-- 14. Finance Corporate Expense Category Summary
DROP VIEW IF EXISTS analytics.vw_finance_expense_summary CASCADE;
CREATE VIEW analytics.vw_finance_expense_summary AS
SELECT 
    ec.category_name AS expense_category,
    ROUND(SUM(fe.amount)::numeric, 2) AS total_spent,
    ROUND((SUM(fe.amount) / 10000000.0)::numeric, 2) AS total_spent_crores,
    COUNT(fe.expense_id) AS transaction_count,
    ROUND((SUM(fe.amount) / SUM(SUM(fe.amount)) OVER () * 100)::numeric, 2) AS pct_of_total,
    ROUND((SUM(fe.amount) / NULLIF(COUNT(DISTINCT DATE_TRUNC('month', fe.expense_date)), 0))::numeric, 2) AS avg_monthly_spend,
    RANK() OVER (ORDER BY SUM(fe.amount) DESC) AS spend_rank
FROM finance.expenses fe
JOIN core.dim_expense_category ec ON fe.exp_cat_id = ec.exp_cat_id
GROUP BY ec.category_name;

-- 15. Web Device & OS Mix View
DROP VIEW IF EXISTS analytics.mv_web_device_os CASCADE;
CREATE VIEW analytics.mv_web_device_os AS
SELECT 
    device_type,
    os,
    COUNT(*) AS view_count,
    COUNT(DISTINCT session_id) AS session_count,
    ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS traffic_share_pct
FROM web_events.page_views
GROUP BY device_type, os
ORDER BY view_count DESC;

-- 16. Web Traffic Monthly View
DROP VIEW IF EXISTS analytics.mv_web_traffic_monthly CASCADE;
CREATE VIEW analytics.mv_web_traffic_monthly AS
SELECT 
    TO_CHAR(view_timestamp, 'YYYY-MM') AS month_year,
    COUNT(view_id) AS page_views,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(DISTINCT customer_id) AS active_users,
    COUNT(CASE WHEN device_type = 'Mobile' THEN 1 END) AS mobile_views,
    COUNT(CASE WHEN device_type = 'Desktop' THEN 1 END) AS desktop_views
FROM web_events.page_views
GROUP BY TO_CHAR(view_timestamp, 'YYYY-MM')
ORDER BY month_year ASC;

-- 17. Top Pages View
DROP VIEW IF EXISTS analytics.mv_top_pages CASCADE;
CREATE VIEW analytics.mv_top_pages AS
SELECT 
    page_url,
    COUNT(*) AS views_count,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS share_pct
FROM web_events.page_views
GROUP BY page_url
ORDER BY views_count DESC;

