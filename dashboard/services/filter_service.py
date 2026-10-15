from datetime import datetime, timedelta
from .db_service import execute_query, execute_one

DEFAULT_START_DATE = "2024-01-01"
DEFAULT_END_DATE = "2026-02-26"

def get_filter_options(selected_region=None):
    """Retrieve dynamic filter options from PostgreSQL for HR & Finance domains."""
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
    
    departments = execute_query("""
        SELECT dept_id, dept_name 
        FROM core.dim_department 
        ORDER BY dept_name;
    """)

    expense_categories = execute_query("""
        SELECT exp_cat_id, category_name 
        FROM core.dim_expense_category 
        ORDER BY category_name;
    """)
    
    return {
        'regions': regions,
        'stores': stores,
        'departments': departments,
        'expense_categories': expense_categories,
        'min_date': DEFAULT_START_DATE,
        'max_date': DEFAULT_END_DATE,
    }


def parse_filters(request):
    """Parse, sanitize, and validate HTTP GET filter query parameters."""
    start_date = request.GET.get('start_date', DEFAULT_START_DATE)
    end_date = request.GET.get('end_date', DEFAULT_END_DATE)
    region_id = request.GET.get('region_id')
    store_id = request.GET.get('store_id')
    dept_id = request.GET.get('dept_id')
    exp_cat_id = request.GET.get('exp_cat_id')
    
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
    cleaned_dept = int(dept_id) if dept_id and dept_id.isdigit() else None
    cleaned_exp_cat = int(exp_cat_id) if exp_cat_id and exp_cat_id.isdigit() else None
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'region_id': cleaned_region,
        'store_id': cleaned_store,
        'dept_id': cleaned_dept,
        'exp_cat_id': cleaned_exp_cat,
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
    where_sql = " AND ".join(conditions)
    return f"WHERE {where_sql}" if where_sql else "", params


def build_employee_where_clause(filters, alias="e"):
    """Build dynamic WHERE conditions for stores.employees queries."""
    conditions = []
    params = []

    if filters.get('dept_id'):
        conditions.append(f"{alias}.dept_id = %s")
        params.append(filters['dept_id'])

    if filters.get('store_id'):
        conditions.append(f"{alias}.store_id = %s")
        params.append(filters['store_id'])
    elif filters.get('region_id'):
        conditions.append(f"{alias}.store_id IN (SELECT store_id FROM stores.stores WHERE region_id = %s)")
        params.append(filters['region_id'])

    where_sql = " AND ".join(conditions)
    return f"WHERE {where_sql}" if where_sql else "", params


def build_expense_where_clause(filters, alias="e"):
    """Build dynamic WHERE conditions for finance.expenses queries."""
    conditions = []
    params = []

    if filters.get('start_date'):
        conditions.append(f"{alias}.expense_date >= %s")
        params.append(filters['start_date'])

    if filters.get('end_date'):
        conditions.append(f"{alias}.expense_date <= %s")
        params.append(filters['end_date'])

    if filters.get('exp_cat_id'):
        conditions.append(f"{alias}.exp_cat_id = %s")
        params.append(filters['exp_cat_id'])

    where_sql = " AND ".join(conditions)
    return f"WHERE {where_sql}" if where_sql else "", params

