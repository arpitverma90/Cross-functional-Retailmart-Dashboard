from datetime import datetime, timedelta
from .db_service import execute_query, execute_one

DEFAULT_START_DATE = "2024-01-01"
DEFAULT_END_DATE = "2026-02-26"

def get_filter_options(selected_region=None):
    """Retrieve dynamic filter options from PostgreSQL."""
    regions = execute_query("""
        SELECT region_id, region_name, state 
        FROM core.dim_region 
        ORDER BY region_name;
    """)
    
    store_sql = "SELECT store_id, store_name, region_id, city FROM stores.stores"
    store_params = []
    if selected_region:
        store_sql += " WHERE region_id = %s"
        store_params.append(selected_region)
    store_sql += " ORDER BY store_name;"
    stores = execute_query(store_sql, store_params)
    
    categories = execute_query("""
        SELECT category_id, category_name 
        FROM core.dim_category 
        ORDER BY category_name;
    """)
    
    tiers = execute_query("""
        SELECT DISTINCT tier AS tier_name 
        FROM customers.customers 
        WHERE tier IS NOT NULL 
        ORDER BY tier;
    """)
    
    return {
        'regions': regions,
        'stores': stores,
        'categories': categories,
        'tiers': tiers,
        'min_date': DEFAULT_START_DATE,
        'max_date': DEFAULT_END_DATE,
    }


def parse_filters(request):
    """Parse, sanitize, and validate HTTP GET filter query parameters."""
    start_date = request.GET.get('start_date', DEFAULT_START_DATE)
    end_date = request.GET.get('end_date', DEFAULT_END_DATE)
    region_id = request.GET.get('region_id')
    store_id = request.GET.get('store_id')
    category_id = request.GET.get('category_id')
    customer_tier = request.GET.get('customer_tier')
    
    # Validation
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except (ValueError, TypeError):
        start_date = DEFAULT_START_DATE
        
    try:
        datetime.strptime(end_date, '%Y-%m-%d')
    except (ValueError, TypeError):
        end_date = DEFAULT_END_DATE
        
    cleaned_region = int(region_id) if region_id and region_id.isdigit() else None
    cleaned_store = int(store_id) if store_id and store_id.isdigit() else None
    cleaned_category = int(category_id) if category_id and category_id.isdigit() else None
    cleaned_tier = customer_tier.strip() if customer_tier and customer_tier in ['Bronze', 'Silver', 'Gold', 'Platinum'] else None
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'region_id': cleaned_region,
        'store_id': cleaned_store,
        'category_id': cleaned_category,
        'customer_tier': cleaned_tier,
    }


def build_sales_where_clause(filters, alias="o"):
    """Build dynamic WHERE conditions for sales orders queries."""
    conditions = [f"{alias}.order_status = 'Delivered'"]
    params = []
    
    if filters.get('start_date'):
        conditions.append(f"{alias}.order_date >= %s")
        params.append(filters['start_date'])
        
    if filters.get('end_date'):
        conditions.append(f"{alias}.order_date <= %s")
        params.append(filters['end_date'])
        
    if filters.get('store_id'):
        conditions.append(f"{alias}.store_id = %s")
        params.append(filters['store_id'])
    elif filters.get('region_id'):
        conditions.append(f"{alias}.store_id IN (SELECT store_id FROM stores.stores WHERE region_id = %s)")
        params.append(filters['region_id'])
        
    if filters.get('customer_tier'):
        conditions.append(f"{alias}.cust_id IN (SELECT customer_id FROM customers.customers WHERE tier = %s)")
        params.append(filters['customer_tier'])
        
    if filters.get('category_id'):
        conditions.append(f"""EXISTS (
            SELECT 1 FROM sales.order_items oi_filter
            JOIN products.products p_filter ON oi_filter.prod_id = p_filter.product_id
            JOIN core.dim_brand b_filter ON p_filter.brand_id = b_filter.brand_id
            WHERE oi_filter.order_id = {alias}.order_id AND b_filter.category_id = %s
        )""")
        params.append(filters['category_id'])
        
    where_sql = " AND ".join(conditions)
    return f"WHERE {where_sql}" if where_sql else "", params
