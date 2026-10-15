"""
People & Financial Governance Analytics Service:
Powers HR Workforce and Financial Ledger Dashboards.
"""

from dashboard.services.db_service import execute_query


def get_hr_dashboard_data():
    """Aggregate HR workforce metrics, store staffing, role breakdown, and salary disbursements."""
    
    # 1. Headline KPIs
    kpi_query = """
        SELECT 
            COUNT(employee_id) AS total_employees,
            ROUND(AVG(salary), 2) AS avg_salary,
            SUM(salary) AS total_monthly_payroll,
            COUNT(DISTINCT store_id) AS active_stores_staffed,
            ROUND(COUNT(employee_id)::numeric / COUNT(DISTINCT store_id), 1) AS avg_staff_per_store
        FROM stores.employees;
    """
    kpis = execute_query(kpi_query)[0]
    
    # 2. Headcount & Average Salary by Department
    dept_query = """
        SELECT 
            d.dept_id,
            d.dept_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(COUNT(e.employee_id)::numeric / SUM(COUNT(e.employee_id)) OVER () * 100, 2) AS dept_share_pct,
            ROUND(AVG(e.salary), 2) AS avg_salary,
            SUM(e.salary) AS total_dept_payroll
        FROM core.dim_department d
        LEFT JOIN stores.employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_id, d.dept_name
        ORDER BY employee_count DESC;
    """
    dept_rows = execute_query(dept_query)
    
    # 3. Staffing & Roles Breakdown
    role_query = """
        SELECT 
            role,
            COUNT(employee_id) AS staff_count,
            ROUND(AVG(salary), 2) AS avg_salary,
            MIN(salary) AS min_salary,
            MAX(salary) AS max_salary
        FROM stores.employees
        GROUP BY role
        ORDER BY staff_count DESC;
    """
    role_rows = execute_query(role_query)
    
    # 4. Store Labor Productivity (Sales per Employee)
    productivity_query = """
        WITH store_sales AS (
            SELECT 
                store_id, 
                COUNT(order_id) AS delivered_orders,
                SUM(net_total) AS total_net_revenue
            FROM sales.orders
            WHERE order_status = 'Delivered'
            GROUP BY store_id
        ),
        store_staff AS (
            SELECT 
                store_id, 
                COUNT(employee_id) AS staff_count,
                SUM(salary) AS total_payroll
            FROM stores.employees
            GROUP BY store_id
        )
        SELECT 
            s.store_id,
            s.store_name,
            s.city,
            r.region_name,
            COALESCE(st.staff_count, 0) AS staff_count,
            ROUND(COALESCE(ss.total_net_revenue, 0), 2) AS store_revenue,
            ROUND(COALESCE(ss.total_net_revenue, 0) / NULLIF(st.staff_count, 0), 2) AS revenue_per_employee,
            ROUND(COALESCE(st.total_payroll, 0) * 12 / NULLIF(ss.total_net_revenue, 0) * 100, 2) AS labor_cost_pct
        FROM stores.stores s
        JOIN core.dim_region r ON s.region_id = r.region_id
        LEFT JOIN store_staff st ON s.store_id = st.store_id
        LEFT JOIN store_sales ss ON s.store_id = ss.store_id
        ORDER BY revenue_per_employee DESC NULLS LAST
        LIMIT 10;
    """
    productivity_rows = execute_query(productivity_query)
    
    # 5. Attendance Summary
    att_query = """
        SELECT 
            COUNT(attendance_id) AS total_attendance_logs,
            COUNT(DISTINCT employee_id) AS logged_employees,
            COUNT(DISTINCT attendance_date) AS operating_days_logged
        FROM hr.attendance;
    """
    attendance_stats = execute_query(att_query)[0]

    return {
        'kpis': {
            'total_employees': kpis['total_employees'],
            'avg_salary': float(kpis['avg_salary']),
            'total_monthly_payroll': float(kpis['total_monthly_payroll']),
            'active_stores_staffed': kpis['active_stores_staffed'],
            'avg_staff_per_store': float(kpis['avg_staff_per_store']),
            'total_attendance_logs': attendance_stats['total_attendance_logs']
        },
        'departments': dept_rows,
        'roles': role_rows,
        'productivity': productivity_rows
    }


def get_finance_dashboard_data():
    """Aggregate financial waterfall, store operating expenses, enterprise budget categories, and accounts."""
    
    # 1. Headline Profitability Waterfall
    waterfall_query = """
        SELECT 
            (SELECT SUM(net_total) FROM sales.orders WHERE order_status = 'Delivered') AS delivered_revenue,
            (SELECT SUM(oi.quantity * p.cost_price) 
             FROM sales.order_items oi 
             JOIN sales.orders o ON oi.order_id = o.order_id 
             JOIN products.products p ON oi.prod_id = p.product_id 
             WHERE o.order_status = 'Delivered') AS cogs,
            (SELECT SUM(refund_amount) FROM sales.returns) AS return_refunds,
            (SELECT SUM(amount) FROM stores.expenses) AS store_opex;
    """
    w = execute_query(waterfall_query)[0]
    
    rev = float(w['delivered_revenue'] or 0)
    cogs = float(w['cogs'] or 0)
    gross_profit = rev - cogs
    gross_margin_pct = round((gross_profit / rev) * 100, 2) if rev else 0
    returns = float(w['return_refunds'] or 0)
    opex = float(w['store_opex'] or 0)
    contrib_margin = rev - cogs - returns - opex
    contrib_margin_pct = round((contrib_margin / rev) * 100, 2) if rev else 0
    
    # 2. Store Operating Expense Breakdown (Rent, Utilities, Maintenance, etc.)
    store_exp_query = """
        SELECT 
            expense_type,
            COUNT(store_expense_id) AS expense_count,
            ROUND(SUM(amount), 2) AS total_expense,
            ROUND(AVG(amount), 2) AS avg_expense,
            ROUND(SUM(amount) / SUM(SUM(amount)) OVER () * 100, 2) AS share_pct
        FROM stores.expenses
        GROUP BY expense_type
        ORDER BY total_expense DESC;
    """
    store_expenses = execute_query(store_exp_query)
    
    # 3. Enterprise Expenses by Category (finance.expenses)
    enterprise_exp_query = """
        SELECT 
            ec.category_name,
            COUNT(fe.expense_id) AS transaction_count,
            ROUND(SUM(fe.amount), 2) AS total_amount,
            ROUND(SUM(fe.amount) / SUM(SUM(fe.amount)) OVER () * 100, 2) AS category_share_pct
        FROM core.dim_expense_category ec
        JOIN finance.expenses fe ON ec.exp_cat_id = fe.exp_cat_id
        GROUP BY ec.exp_cat_id, ec.category_name
        ORDER BY total_amount DESC;
    """
    enterprise_expenses = execute_query(enterprise_exp_query)
    
    # 4. Treasury & Bank Accounts
    accounts_query = """
        SELECT 
            account_id,
            account_holder,
            account_type,
            ROUND(balance, 2) AS balance,
            created_at::date AS opening_date
        FROM finance.accounts
        ORDER BY balance DESC
        LIMIT 10;
    """
    accounts_rows = execute_query(accounts_query)

    return {
        'waterfall': {
            'delivered_revenue': rev,
            'cogs': cogs,
            'gross_profit': gross_profit,
            'gross_margin_pct': gross_margin_pct,
            'return_refunds': returns,
            'store_opex': opex,
            'contribution_margin': contrib_margin,
            'contribution_margin_pct': contrib_margin_pct
        },
        'store_expenses': store_expenses,
        'enterprise_expenses': enterprise_expenses,
        'accounts': accounts_rows
    }
