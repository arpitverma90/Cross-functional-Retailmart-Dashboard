-- ============================================================================
-- RetailMart V3 - Analytical Reconciliation Queries
-- Independent SQL scripts to verify analytical aggregates against base tables
-- ============================================================================

-- 1. Delivered Commercial Net Revenue Reconciliation
-- Expected Result: Exactly ₹6,769,536,004.48 on 82,540 orders
SELECT 
    'sales.orders' AS source,
    COUNT(order_id) AS delivered_orders,
    SUM(net_total) AS total_net_revenue,
    SUM(gross_total) AS total_gross_revenue,
    SUM(discount_amount) AS total_discounts
FROM sales.orders
WHERE order_status = 'Delivered';

-- 2. Line-Item Net Revenue Reconciliation
-- Expected Result: Exactly ₹6,769,536,004.48 across 206,365 delivered items
SELECT 
    'sales.order_items (delivered)' AS source,
    COUNT(oi.order_item_id) AS total_items,
    SUM(oi.net_amount) AS total_net_amount
FROM sales.order_items oi
JOIN sales.orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered';

-- 3. Monthly Sales Aggregate Reconciliation
-- Sum of all months in vw_monthly_sales_summary must equal total delivered revenue
SELECT 
    'analytics.vw_monthly_sales_summary' AS source,
    SUM(total_orders) AS sum_orders,
    SUM(total_net_revenue) AS sum_revenue
FROM analytics.vw_monthly_sales_summary;

-- 4. Returns & Refund Cost Reconciliation
-- Total refund amount across all returns
SELECT 
    'sales.returns' AS source,
    COUNT(return_id) AS total_returns,
    COUNT(DISTINCT order_id) AS returned_orders,
    SUM(refund_amount) AS total_refund_amount
FROM sales.returns;

-- 5. Outbound Customer Shipments Reconciliation
-- Status distribution and transit counts
SELECT 
    status,
    COUNT(shipment_id) AS shipment_count,
    COUNT(delivered_date) AS delivered_count
FROM sales.shipments
GROUP BY status
ORDER BY shipment_count DESC;

-- 6. Store Inventory Stock-Out Reconciliation
-- Out of stock and reorder risk SKU counts
SELECT 
    COUNT(*) AS total_inventory_records,
    COUNT(CASE WHEN quantity_on_hand = 0 THEN 1 END) AS out_of_stock_records,
    COUNT(CASE WHEN quantity_on_hand <= reorder_level THEN 1 END) AS at_or_below_reorder_records
FROM products.inventory;
