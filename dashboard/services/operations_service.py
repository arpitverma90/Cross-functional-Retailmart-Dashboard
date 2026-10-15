from .db_service import execute_query, execute_one

def get_operations_dashboard_data(filters):
    """
    Retrieve comprehensive Operations Dashboard dataset covering:
    1. Fulfilment & Shipments
    2. Courier Performance & Delivery SLA
    3. Retail Store Inventory Availability
    4. Warehouses & Inbound Supply Chain
    5. Manufacturing Work Orders & Quality
    6. Store Operations & Productivity
    """
    start_date = filters.get('start_date', '2024-01-01')
    end_date = filters.get('end_date', '2026-02-26')
    
    # 1. Fulfilment & Outbound Shipments Summary (Filter-Aware)
    ship_conditions = ["sh.shipped_date >= %s", "sh.shipped_date <= %s"]
    ship_params = [start_date, end_date]
    if filters.get('store_id'):
        ship_conditions.append("sh.order_id IN (SELECT order_id FROM sales.orders WHERE store_id = %s)")
        ship_params.append(filters['store_id'])
    elif filters.get('region_id'):
        ship_conditions.append("sh.order_id IN (SELECT order_id FROM sales.orders WHERE store_id IN (SELECT store_id FROM stores.stores WHERE region_id = %s))")
        ship_params.append(filters['region_id'])
    if filters.get('category_id'):
        ship_conditions.append("sh.order_id IN (SELECT oi.order_id FROM sales.order_items oi JOIN products.products p ON oi.prod_id = p.product_id JOIN core.dim_brand b ON p.brand_id = b.brand_id WHERE b.category_id = %s)")
        ship_params.append(filters['category_id'])

    shipment_summary_sql = f"""
        SELECT 
            COUNT(sh.shipment_id) AS total_shipments,
            COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END) AS delivered_count,
            COUNT(CASE WHEN sh.status = 'Shipped' AND sh.delivered_date IS NULL THEN 1 END) AS pending_transit_count,
            COUNT(CASE WHEN sh.status = 'Returned' THEN 1 END) AS returned_count,
            ROUND(AVG(CASE WHEN sh.status = 'Delivered' THEN sh.delivered_date - sh.shipped_date END)::numeric, 2) AS avg_transit_days,
            ROUND(
                COUNT(CASE WHEN sh.status = 'Delivered' AND (sh.delivered_date - sh.shipped_date) <= 5 THEN 1 END)::numeric 
                / NULLIF(COUNT(CASE WHEN sh.status = 'Delivered' THEN 1 END), 0) * 100, 2
            ) AS overall_on_time_sla_pct
        FROM sales.shipments sh
        WHERE {' AND '.join(ship_conditions)};
    """
    shipment_summary = execute_one(shipment_summary_sql, ship_params)
    
    # 2. Courier SLA & Performance Comparison
    courier_sql = """
        SELECT 
            courier_name,
            total_shipments,
            delivered_shipments,
            avg_lead_days,
            on_time_sla_pct
        FROM analytics.vw_courier_sla_performance
        ORDER BY total_shipments DESC;
    """
    couriers = execute_query(courier_sql)
    
    # 3. Store Inventory Availability & Stock-Out Risk (Filter-Aware)
    inv_conditions = []
    inv_params = []
    if filters.get('store_id'):
        inv_conditions.append("store_id = %s")
        inv_params.append(filters['store_id'])
    elif filters.get('region_id'):
        inv_conditions.append("store_id IN (SELECT store_id FROM stores.stores WHERE region_id = %s)")
        inv_params.append(filters['region_id'])
    if filters.get('category_id'):
        inv_conditions.append("product_id IN (SELECT p.product_id FROM products.products p JOIN core.dim_brand b ON p.brand_id = b.brand_id WHERE b.category_id = %s)")
        inv_params.append(filters['category_id'])
    inv_where = f"WHERE {' AND '.join(inv_conditions)}" if inv_conditions else ""
    
    inventory_sql = f"""
        SELECT 
            COUNT(DISTINCT product_id) AS total_monitored_products,
            COALESCE(SUM(quantity_on_hand), 0) AS total_units_in_stores,
            COUNT(CASE WHEN quantity_on_hand = 0 THEN 1 END) AS out_of_stock_slots,
            COUNT(CASE WHEN quantity_on_hand <= reorder_level AND quantity_on_hand > 0 THEN 1 END) AS low_stock_slots,
            ROUND(COUNT(CASE WHEN quantity_on_hand <= reorder_level THEN 1 END)::numeric / NULLIF(COUNT(*), 0) * 100, 2) AS stock_risk_pct
        FROM products.inventory
        {inv_where};
    """
    inventory_summary = execute_one(inventory_sql, inv_params)
    
    # 4. Regional Distribution Centers (Warehouses)
    warehouse_sql = """
        WITH ship_agg AS (
            SELECT warehouse_id, SUM(quantity) AS total_inbound_units, COUNT(shipment_id) AS inbound_shipment_batches
            FROM supply_chain.shipments
            GROUP BY warehouse_id
        )
        SELECT 
            w.warehouse_id,
            w.name AS warehouse_name,
            w.location_city,
            w.region,
            w.capacity_sqft,
            w.manager_name,
            COALESCE(s.total_inbound_units, 0) AS total_inbound_units,
            COALESCE(s.inbound_shipment_batches, 0) AS inbound_shipment_batches
        FROM supply_chain.warehouses w
        LEFT JOIN ship_agg s ON w.warehouse_id = s.warehouse_id
        ORDER BY w.capacity_sqft DESC;
    """
    warehouses = execute_query(warehouse_sql)
    
    # 5. Manufacturing Assembly Lines & Quality Scrap
    mfg_sql = """
        SELECT 
            line_id,
            line_name,
            total_batches,
            total_produced,
            total_rejected,
            rejection_rate_pct
        FROM analytics.vw_mfg_quality_metrics
        ORDER BY total_produced DESC;
    """
    mfg_lines = execute_query(mfg_sql)
    
    # 6. Store Operations & Productivity (Grain-Safe CTE Aggregations)
    store_ops_sql = """
        WITH emp_agg AS (
            SELECT store_id, COUNT(employee_id) AS employee_count
            FROM stores.employees
            GROUP BY store_id
        ),
        exp_agg AS (
            SELECT store_id, SUM(amount) AS total_operating_expenses
            FROM stores.expenses
            GROUP BY store_id
        ),
        ord_agg AS (
            SELECT store_id, SUM(net_total) AS store_revenue
            FROM sales.orders
            WHERE order_status = 'Delivered'
            GROUP BY store_id
        )
        SELECT 
            s.store_id,
            s.store_name,
            s.city,
            s.square_ft,
            COALESCE(e.employee_count, 0) AS employee_count,
            COALESCE(ex.total_operating_expenses, 0) AS total_operating_expenses,
            ROUND(COALESCE(o.store_revenue, 0) / NULLIF(s.square_ft, 0), 2) AS sales_per_sqft
        FROM stores.stores s
        LEFT JOIN emp_agg e ON s.store_id = e.store_id
        LEFT JOIN exp_agg ex ON s.store_id = ex.store_id
        LEFT JOIN ord_agg o ON s.store_id = o.store_id
        """ + (f"WHERE s.store_id = {filters['store_id']}" if filters.get('store_id') else (f"WHERE s.region_id = {filters['region_id']}" if filters.get('region_id') else "")) + """
        ORDER BY sales_per_sqft DESC NULLS LAST
        LIMIT 10;
    """
    top_productive_stores = execute_query(store_ops_sql)
    
    return {
        'shipment_summary': shipment_summary,
        'couriers': couriers,
        'inventory_summary': inventory_summary,
        'warehouses': warehouses,
        'mfg_lines': mfg_lines,
        'top_productive_stores': top_productive_stores
    }
