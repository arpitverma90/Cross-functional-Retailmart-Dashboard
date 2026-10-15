"""
RetailMart V3 - Logistics Service Module
Provides parameterized PostgreSQL queries for Logistics Dashboard:
- Courier SLA Performance & Delivery Lead Times
- Pending Fulfillment & In-Transit Outbound Parcels
- Inbound Supplier Procurement Shipments
- Warehouse Storage Capacity & Inventory Snapshots
- Store-Level Stockout Risk SKUs
"""

from .db_service import execute_query, execute_one, execute_scalar


def get_logistics_kpis(filters):
    """
    Computes headline KPIs for the Logistics domain:
    - Delivered Outbound Shipments
    - Courier On-Time Delivery (OTD) SLA Rate (<= 5 days)
    - Average Delivery Lead Time (Days)
    - Pending & In-Transit Shipments
    - Orders Awaiting Fulfillment (Processing status)
    - Store Stockout Risk SKUs
    - Inbound Delay Rate %
    """
    where_ship = ["1=1"]
    where_ord = ["1=1"]
    where_inbound = ["1=1"]
    params_ship = []
    params_ord = []
    params_inbound = []

    if filters.get('start_date'):
        where_ship.append("shipped_date >= %s")
        where_ord.append("order_date >= %s")
        where_inbound.append("shipped_date >= %s")
        params_ship.append(filters['start_date'])
        params_ord.append(filters['start_date'])
        params_inbound.append(filters['start_date'])

    if filters.get('end_date'):
        where_ship.append("shipped_date <= %s")
        where_ord.append("order_date <= %s")
        where_inbound.append("shipped_date <= %s")
        params_ship.append(filters['end_date'])
        params_ord.append(filters['end_date'])
        params_inbound.append(filters['end_date'])

    # Outbound Carrier Shipments
    outbound_sql = f"""
        SELECT 
            COUNT(*) AS total_shipments,
            COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_shipments,
            COUNT(CASE WHEN status = 'Shipped' THEN 1 END) AS in_transit_shipments,
            COUNT(CASE WHEN status = 'Returned' THEN 1 END) AS returned_shipments,
            COUNT(CASE WHEN status = 'Delivered' AND (delivered_date - shipped_date) <= 5 THEN 1 END) AS on_time_shipments,
            ROUND(AVG(CASE WHEN status = 'Delivered' THEN (delivered_date - shipped_date) END)::numeric, 2) AS avg_lead_time_days
        FROM sales.shipments
        WHERE {' AND '.join(where_ship)};
    """
    outbound_data = execute_one(outbound_sql, params_ship) or {}
    
    delivered_count = outbound_data.get('delivered_shipments', 0)
    on_time_count = outbound_data.get('on_time_shipments', 0)
    otd_sla_rate = round((on_time_count / delivered_count * 100), 2) if delivered_count > 0 else 0.0
    avg_lead_time = outbound_data.get('avg_lead_time_days', 0.0)
    in_transit_shipments = outbound_data.get('in_transit_shipments', 0)

    # Orders Awaiting Fulfillment (Processing)
    ord_sql = f"""
        SELECT COUNT(*) AS processing_orders
        FROM sales.orders
        WHERE order_status = 'Processing' AND {' AND '.join(where_ord)};
    """
    processing_orders = execute_scalar(ord_sql, params_ord, default=0)

    # Store Inventory Stockout Risk (Items with quantity <= reorder_level)
    stockout_sql = """
        SELECT COUNT(*) AS stockout_skus
        FROM products.inventory
        WHERE quantity_on_hand <= reorder_level;
    """
    stockout_skus = execute_scalar(stockout_sql, default=0)

    # Inbound Supplier Shipments
    inbound_sql = f"""
        SELECT 
            COUNT(*) AS total_inbound,
            COUNT(CASE WHEN status = 'Delayed' THEN 1 END) AS delayed_inbound,
            COUNT(CASE WHEN status = 'In Transit' THEN 1 END) AS in_transit_inbound,
            COUNT(CASE WHEN status = 'Received' THEN 1 END) AS received_inbound
        FROM supply_chain.shipments
        WHERE {' AND '.join(where_inbound)};
    """
    inbound_data = execute_one(inbound_sql, params_inbound) or {}
    total_inbound = inbound_data.get('total_inbound', 0)
    delayed_inbound = inbound_data.get('delayed_inbound', 0)
    inbound_delay_rate = round((delayed_inbound / total_inbound * 100), 2) if total_inbound > 0 else 0.0

    return {
        'delivered_shipments': delivered_count,
        'otd_sla_rate': otd_sla_rate,
        'avg_lead_time_days': avg_lead_time,
        'in_transit_shipments': in_transit_shipments,
        'processing_orders': processing_orders,
        'stockout_skus': stockout_skus,
        'total_inbound': total_inbound,
        'delayed_inbound': delayed_inbound,
        'inbound_delay_rate': inbound_delay_rate,
    }


def get_courier_sla_breakdown(filters):
    """Courier comparison: Delivered Volume, On-Time SLA %, and Average Lead Time."""
    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("shipped_date >= %s")
        params.append(filters['start_date'])
    if filters.get('end_date'):
        where.append("shipped_date <= %s")
        params.append(filters['end_date'])

    sql = f"""
        SELECT 
            courier_name,
            COUNT(*) AS total_dispatches,
            COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_count,
            COUNT(CASE WHEN status = 'Shipped' THEN 1 END) AS in_transit_count,
            COUNT(CASE WHEN status = 'Returned' THEN 1 END) AS returned_count,
            ROUND(AVG(CASE WHEN status = 'Delivered' THEN (delivered_date - shipped_date) END)::numeric, 2) AS avg_lead_time,
            ROUND((COUNT(CASE WHEN status = 'Delivered' AND (delivered_date - shipped_date) <= 5 THEN 1 END)::numeric / 
                   NULLIF(COUNT(CASE WHEN status = 'Delivered' THEN 1 END), 0) * 100), 2) AS otd_sla_pct
        FROM sales.shipments
        WHERE {' AND '.join(where)}
        GROUP BY courier_name
        ORDER BY delivered_count DESC;
    """
    return execute_query(sql, params)


def get_delivery_lead_time_distribution(filters):
    """Histogram of delivery transit days."""
    where = ["status = 'Delivered'", "delivered_date >= shipped_date"]
    params = []
    if filters.get('start_date'):
        where.append("shipped_date >= %s")
        params.append(filters['start_date'])
    if filters.get('end_date'):
        where.append("shipped_date <= %s")
        params.append(filters['end_date'])

    sql = f"""
        SELECT 
            CASE 
                WHEN (delivered_date - shipped_date) <= 1 THEN '1 Day (Next Day)'
                WHEN (delivered_date - shipped_date) = 2 THEN '2 Days'
                WHEN (delivered_date - shipped_date) = 3 THEN '3 Days'
                WHEN (delivered_date - shipped_date) = 4 THEN '4 Days'
                WHEN (delivered_date - shipped_date) = 5 THEN '5 Days (SLA Cap)'
                ELSE '6+ Days (Breached)'
            END AS transit_bracket,
            CASE 
                WHEN (delivered_date - shipped_date) <= 1 THEN 1
                WHEN (delivered_date - shipped_date) = 2 THEN 2
                WHEN (delivered_date - shipped_date) = 3 THEN 3
                WHEN (delivered_date - shipped_date) = 4 THEN 4
                WHEN (delivered_date - shipped_date) = 5 THEN 5
                ELSE 6
            END AS sort_order,
            COUNT(*) AS shipment_count,
            ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS pct_of_total
        FROM sales.shipments
        WHERE {' AND '.join(where)}
        GROUP BY 1, 2
        ORDER BY sort_order ASC;
    """
    return execute_query(sql, params)


def get_warehouse_utilization(filters):
    """Warehouse facility capacity and latest snapshot inventory units."""
    sql = """
        WITH latest_snapshot AS (
            SELECT 
                warehouse_id,
                MAX(snapshot_date) AS max_date
            FROM supply_chain.inventory_snapshots
            GROUP BY warehouse_id
        ),
        warehouse_stock AS (
            SELECT 
                s.warehouse_id,
                SUM(s.quantity_on_hand) AS total_units_on_hand,
                COUNT(DISTINCT s.product_id) AS active_skus
            FROM supply_chain.inventory_snapshots s
            JOIN latest_snapshot ls ON s.warehouse_id = ls.warehouse_id AND s.snapshot_date = ls.max_date
            GROUP BY s.warehouse_id
        )
        SELECT 
            w.warehouse_id,
            w.name AS warehouse_name,
            w.location_city,
            w.region,
            w.capacity_sqft,
            COALESCE(ws.total_units_on_hand, 0) AS total_units_on_hand,
            COALESCE(ws.active_skus, 0) AS active_skus,
            ROUND((COALESCE(ws.total_units_on_hand, 0)::numeric / NULLIF(w.capacity_sqft, 0)), 2) AS stock_density_ratio
        FROM supply_chain.warehouses w
        LEFT JOIN warehouse_stock ws ON w.warehouse_id = ws.warehouse_id
        ORDER BY w.warehouse_id ASC;
    """
    return execute_query(sql)


def get_inbound_shipments_status(filters):
    """Inbound supplier shipment tracking by status and supplier volume."""
    where = ["1=1"]
    params = []
    if filters.get('start_date'):
        where.append("s.shipped_date >= %s")
        params.append(filters['start_date'])
    if filters.get('end_date'):
        where.append("s.shipped_date <= %s")
        params.append(filters['end_date'])

    sql = f"""
        SELECT 
            s.status,
            COUNT(*) AS shipment_lots,
            SUM(s.quantity) AS total_units,
            ROUND(AVG(COALESCE(s.arrival_date, CURRENT_DATE) - s.shipped_date)::numeric, 1) AS avg_transit_days
        FROM supply_chain.shipments s
        WHERE {' AND '.join(where)}
        GROUP BY s.status
        ORDER BY shipment_lots DESC;
    """
    return execute_query(sql, params)


def get_category_stockout_risks():
    """Identifies retail product categories with highest critical stockout risks."""
    sql = """
        SELECT 
            c.category_name,
            COUNT(i.product_id) AS total_store_skus,
            COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END) AS stockout_risk_count,
            ROUND((COUNT(CASE WHEN i.quantity_on_hand <= i.reorder_level THEN 1 END)::numeric / 
                   NULLIF(COUNT(i.product_id), 0) * 100), 2) AS stockout_risk_pct,
            SUM(i.quantity_on_hand) AS total_units_on_shelf
        FROM products.inventory i
        JOIN products.products p ON i.product_id = p.product_id
        JOIN core.dim_brand b ON p.brand_id = b.brand_id
        JOIN core.dim_category c ON b.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY stockout_risk_count DESC;
    """
    return execute_query(sql)
