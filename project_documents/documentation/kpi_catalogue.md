# RetailMart V3 - Authoritative KPI Catalogue (HR & Finance Dedicated)
## Enterprise Metric Specification Register

This catalogue defines all approved production KPIs across the **Executive Summary**, **HR Dashboard**, **Finance Dashboard**, and **Cross-Functional Analysis** domains in accordance with enterprise BI governance rules.

---

## 1. Executive Summary Dashboard KPIs

### KPI 1.1: Active Enterprise Workforce Headcount
- **KPI and Domain**: Active Enterprise Workforce Headcount (Executive Summary & HR)
- **Business Definition**: Total count of active staff employed across all retail stores and corporate departments.
- **Business Purpose**: Core enterprise workforce scale indicator supporting organizational planning.
- **Formula**: `Active Headcount = COUNT(employee_id)`
- **Grain**: Employee Master Grain
- **Tables and Columns**: `stores.employees.employee_id`, `stores.employees.salary`
- **Join Path**: N/A (Single Table)
- **Date Basis**: Snapshot as of current reporting date
- **Filters and Exclusions**: Valid non-null employee records
- **Feasibility**: Directly Available
- **Limitations**: No termination dates exist; all 3,000 employees are treated as active.
- **Visual and Drill-Down**: Headline KPI card with drill-through to `/business-dashboard/hr/`.
- **Validation Query**: `SELECT COUNT(*) FROM stores.employees;`
- **Management Action**: Maintain retail staffing targets and monitor headcount distribution.

### KPI 1.2: Delivered Commercial Net Revenue & Order Volume
- **KPI and Domain**: Delivered Commercial Net Revenue & Order Volume (Executive Summary & Finance)
- **Business Purpose**: Recognized commercial sales income from fulfilled customer purchase orders.
- **Formula**: `Delivered Net Revenue = SUM(net_total WHERE order_status = 'Delivered')`
- **Grain**: Customer Order Grain
- **Tables and Columns**: `sales.orders.net_total`, `sales.orders.order_status`, `sales.orders.order_date`
- **Join Path**: N/A
- **Date Basis**: `order_date`
- **Filters and Exclusions**: `order_status = 'Delivered'`
- **Feasibility**: Directly Available
- **Limitations**: Does not account for uncollected receivables.
- **Visual and Drill-Down**: Headline KPI card with monthly trend sparkline and drill-through to `/business-dashboard/finance/`.
- **Validation Query**: `SELECT COUNT(*), SUM(net_total) FROM sales.orders WHERE order_status = 'Delivered';`
- **Management Action**: Review commercial performance against targets if revenue trails prior period by >5%.

### KPI 1.3: Total Operating Expenditure (Corporate & Store)
- **KPI and Domain**: Total Operating Expenditure (Executive Summary & Finance)
- **Business Purpose**: Total recognized operational cash outflows across corporate overhead and branch costs.
- **Formula**: `Total OPEX = SUM(finance.expenses.amount) + SUM(stores.expenses.amount)`
- **Grain**: Macro Financial Grain
- **Tables and Columns**: `finance.expenses.amount`, `stores.expenses.amount`
- **Join Path**: Independent aggregation in CTEs before summation
- **Date Basis**: `expense_date`
- **Filters and Exclusions**: Excludes nulls and non-positive vouchers
- **Feasibility**: Directly Available
- **Limitations**: Excludes depreciation, amortization, and financing costs.
- **Visual and Drill-Down**: Headline KPI card with expense category donut chart.
- **Validation Query**: `SELECT (SELECT SUM(amount) FROM finance.expenses) + (SELECT SUM(amount) FROM stores.expenses);`
- **Management Action**: Institute spending controls when OPEX growth outpaces top-line revenue.

### KPI 1.4: Net Operating Spread & Margin [PROXY]
- **KPI and Domain**: Net Operating Spread & Margin (Executive Summary & Finance)
- **Business Purpose**: Evaluates operating margin health as revenue minus total operating expenses.
- **Formula**: `Net Spread = Delivered Revenue - Total OPEX; Margin % = Net Spread / Revenue * 100`
- **Grain**: Macro Financial Grain
- **Tables and Columns**: `sales.orders`, `finance.expenses`, `stores.expenses`
- **Join Path**: Pre-aggregated CTEs joined on macro reporting period
- **Date Basis**: `order_date`, `expense_date`
- **Filters and Exclusions**: Delivered orders only
- **Feasibility**: Proxy Metric `[PROXY]`
- **Limitations**: Serves as an operational proxy for operating income; not audited EBITDA.
- **Visual and Drill-Down**: KPI card with margin gauge and MoM variance badge.
- **Validation Query**: CTE reconciling sales revenue against combined expense sums.
- **Management Action**: Trigger operational efficiency audits if operating margin turns negative.

### KPI 1.5: Monthly Processed Payroll Cash Outflow
- **KPI and Domain**: Monthly Processed Payroll Cash Outflow (Executive Summary & HR)
- **Business Purpose**: Monitors total bank disbursement volume for employee salaries.
- **Formula**: `Monthly Payroll = SUM(amount) WHERE status = 'Processed'`
- **Grain**: Salary Disbursement Grain
- **Tables and Columns**: `hr.salary_history.amount`, `hr.salary_history.status`, `hr.salary_history.payment_date`
- **Join Path**: N/A
- **Date Basis**: `payment_date`
- **Filters and Exclusions**: `status = 'Processed'`
- **Feasibility**: Directly Available
- **Limitations**: Covers historical processed disbursements from March 2025 to Feb 2026.
- **Visual and Drill-Down**: Monthly bar chart tracking monthly payroll expenditure.
- **Validation Query**: `SELECT SUM(amount) FROM hr.salary_history WHERE status = 'Processed';`
- **Management Action**: Validate salary disbursement approvals and cash balances prior to payout dates.

### KPI 1.6: Enterprise Labor Cost to Revenue Ratio [Cross-Functional]
- **KPI and Domain**: Enterprise Labor Cost to Revenue Ratio (Executive Summary & Cross-Functional)
- **Business Purpose**: Assesses human capital expenditure intensity relative to commercial income.
- **Formula**: `Labor Cost Ratio % = (Annualized Payroll / Delivered Revenue) * 100`
- **Grain**: Macro Ratio Grain
- **Tables and Columns**: `stores.employees.salary`, `sales.orders.net_total`
- **Join Path**: Pre-aggregated CTEs
- **Date Basis**: Reporting period date bounds
- **Filters and Exclusions**: Delivered orders only
- **Feasibility**: Derivable
- **Limitations**: Relies on annualized base salaries.
- **Visual and Drill-Down**: Ratio metric tile with regional comparison chart.
- **Validation Query**: Reconciles `SUM(salary)*12` against `SUM(net_total)`.
- **Management Action**: Adjust store staffing models where labor cost exceeds 25% of store sales.

### KPI 1.7: Revenue per Employee [Cross-Functional]
- **KPI and Domain**: Revenue per Employee (Executive Summary & Cross-Functional)
- **Business Purpose**: Core workforce productivity indicator measuring revenue generation per staff member.
- **Formula**: `Revenue per Employee = Total Delivered Revenue / Total Headcount`
- **Grain**: Enterprise Productivity Grain
- **Tables and Columns**: `sales.orders.net_total`, `stores.employees.employee_id`
- **Join Path**: Pre-aggregated CTEs
- **Date Basis**: Reporting period date bounds
- **Filters and Exclusions**: Delivered orders only
- **Feasibility**: Derivable
- **Limitations**: Reflects macro enterprise average.
- **Visual and Drill-Down**: Headline metric card with regional breakdown.
- **Validation Query**: Reconciles delivered net revenue divided by 3,000 headcount.
- **Management Action**: Investigate stores with below-average revenue per employee.

### KPI 1.8: Workforce Attendance Compliance Rate [PROXY]
- **KPI and Domain**: Workforce Attendance Compliance Rate (Executive Summary & HR)
- **Business Purpose**: Monitors regular attendance and presenteeism against scheduled workdays.
- **Formula**: `Compliance % = (Avg Days Present / 22.0) * 100`
- **Grain**: Employee-Month Grain
- **Tables and Columns**: `hr.attendance.attendance_id`, `hr.attendance.check_in`
- **Join Path**: `hr.attendance.employee_id` -> `stores.employees.employee_id`
- **Date Basis**: `attendance_date`
- **Filters and Exclusions**: Non-null check-in timestamps
- **Feasibility**: Proxy Metric `[PROXY]`
- **Limitations**: Standard 22-day working month is assumed as formal leave records are absent.
- **Visual and Drill-Down**: Department attendance bar chart.
- **Validation Query**: Aggregates distinct days present per employee per month.
- **Management Action**: Implement attendance remediation plans in branches falling below 85%.

### KPI 1.9: Liquid Treasury Cash & Bank Account Reserves
- **KPI and Domain**: Liquid Treasury Cash & Bank Account Reserves (Executive Summary & Finance)
- **Business Purpose**: Tracks available cash reserves across corporate bank accounts.
- **Formula**: `Treasury Balance = SUM(balance) FROM finance.accounts`
- **Grain**: Account Ledger Grain
- **Tables and Columns**: `finance.accounts.balance`, `finance.accounts.account_type`
- **Join Path**: N/A
- **Date Basis**: Current snapshot
- **Filters and Exclusions**: Non-null balances
- **Feasibility**: Directly Available
- **Limitations**: Represents cash balances without reconciliation to external banking APIs.
- **Visual and Drill-Down**: Account balance breakdown card by account type.
- **Validation Query**: `SELECT SUM(balance) FROM finance.accounts;`
- **Management Action**: Ensure treasury reserves maintain minimum 90-day liquidity buffer.

### KPI 1.10: Gross Commercial Margin & Product Profitability
- **KPI and Domain**: Gross Commercial Margin & Product Profitability (Executive Summary & Finance)
- **Business Purpose**: Quantifies product gross margin after deducting Cost of Goods Sold.
- **Formula**: `Gross Margin % = (Net Revenue - COGS) / Net Revenue * 100`
- **Grain**: Order Item Grain
- **Tables and Columns**: `sales.order_items.net_amount`, `sales.order_items.quantity`, `products.products.cost_price`
- **Join Path**: `sales.order_items.prod_id = products.products.product_id`
- **Date Basis**: `sales.orders.order_date`
- **Filters and Exclusions**: Delivered orders only
- **Feasibility**: Derivable
- **Limitations**: Unit cost price is assumed static across inventory batches.
- **Visual and Drill-Down**: Margin trajectory line chart and category table.
- **Validation Query**: Reconciles net amount minus `quantity * cost_price`.
- **Management Action**: Discontinue or re-price SKU lines generating negative gross margins.

---

## 2. Detailed HR Domain KPIs

### KPI 2.1: Workforce Distribution by Department and Role
- **Domain**: HR Intelligence
- **Formula**: `COUNT(employee_id) GROUP BY dept_name, role`
- **Grain**: Department & Role Grain
- **Tables**: `stores.employees`, `core.dim_department`
- **Feasibility**: Directly Available
- **Management Action**: Align departmental headcounts with organizational workforce plans.

### KPI 2.2: Base Salary Structure by Department
- **Domain**: HR Intelligence
- **Formula**: `MIN, AVG, MEDIAN, MAX(salary) GROUP BY dept_name`
- **Grain**: Department Grain
- **Tables**: `stores.employees`, `core.dim_department`
- **Feasibility**: Directly Available
- **Management Action**: Benchmark departmental pay scales against market standards.

### KPI 2.3: Payroll Compensation Components (Basic, HRA, Allowances)
- **Domain**: HR Intelligence
- **Formula**: `SUM(basic_salary), SUM(hra), SUM(other_allowances), SUM(gross_salary)`
- **Grain**: Payroll Component Grain
- **Tables**: `payroll.pay_slips`
- **Feasibility**: Directly Available
- **Management Action**: Optimize allowance structuring to ensure compliance with labor codes.

### KPI 2.4: Statutory Payroll Deductions and Net Payout
- **Domain**: HR Intelligence
- **Formula**: `SUM(pf), SUM(professional_tax), SUM(income_tax), SUM(net_salary)`
- **Grain**: Payroll Deduction Grain
- **Tables**: `payroll.pay_slips`
- **Feasibility**: Directly Available
- **Management Action**: Guarantee timely statutory deposits of PF and withholding taxes.

### KPI 2.5: Monthly Salary Disbursement History and Status
- **Domain**: HR Intelligence
- **Formula**: `COUNT(*), SUM(amount) GROUP BY Month, status`
- **Grain**: Payment Month Grain
- **Tables**: `hr.salary_history`
- **Feasibility**: Directly Available
- **Management Action**: Immediately investigate failed bank disbursement transactions.

### KPI 2.6: Employee Attendance Shift Duration Distribution
- **Domain**: HR Intelligence
- **Formula**: `EXTRACT(EPOCH FROM (check_out - check_in))/3600.0`
- **Grain**: Shift Tier Grain
- **Tables**: `hr.attendance`
- **Feasibility**: Derivable
- **Management Action**: Curb excessive overtime (>9.5 hours) to prevent staff burnout.

### KPI 2.7: Departmental Attendance Compliance Rates [PROXY]
- **Domain**: HR Intelligence
- **Formula**: `(AVG(days_present) / 22.0) * 100 GROUP BY dept_name`
- **Grain**: Department Grain
- **Tables**: `hr.attendance`, `stores.employees`, `core.dim_department`
- **Feasibility**: Proxy Metric `[PROXY]`
- **Management Action**: Implement attendance improvement plans in lagging departments.

### KPI 2.8: Retail Store Staffing Density and Payroll by Branch
- **Domain**: HR Intelligence
- **Formula**: `COUNT(employee_id), SUM(salary) GROUP BY store_id`
- **Grain**: Retail Store Grain
- **Tables**: `stores.stores`, `stores.employees`, `core.dim_region`
- **Feasibility**: Directly Available
- **Management Action**: Reallocate staffing from overstaffed branches to understaffed locations.

### KPI 2.9: Workforce Hiring Cadence and Joining Cohorts
- **Domain**: HR Intelligence
- **Formula**: `COUNT(employee_id) GROUP BY Year, Month of joining_date`
- **Grain**: Hiring Month Grain
- **Tables**: `stores.employees`
- **Feasibility**: Directly Available
- **Management Action**: Align HR recruitment pipeline with retail expansion plans.

---

## 3. Detailed Finance Domain KPIs

### KPI 3.1: Monthly Commercial Net Revenue Trajectory
- **Domain**: Finance Intelligence
- **Formula**: `SUM(net_total) GROUP BY Month WHERE status = 'Delivered'`
- **Grain**: Monthly Grain
- **Tables**: `sales.orders`
- **Feasibility**: Directly Available
- **Management Action**: Revise quarterly revenue forecasts based on sales trajectory.

### KPI 3.2: Corporate Operating Expenses by Expense Category
- **Domain**: Finance Intelligence
- **Formula**: `SUM(amount) GROUP BY exp_cat_id`
- **Grain**: Expense Category Grain
- **Tables**: `finance.expenses`, `core.dim_expense_category`
- **Feasibility**: Directly Available
- **Management Action**: Audit and control corporate overhead categories showing abnormal growth.

### KPI 3.3: Store Operating Expenses by Cost Type
- **Domain**: Finance Intelligence
- **Formula**: `SUM(amount) GROUP BY expense_type`
- **Grain**: Cost Type Grain
- **Tables**: `stores.expenses`
- **Feasibility**: Directly Available
- **Management Action**: Benchmark rent, electricity, and security costs across retail stores.

### KPI 3.4: Product Category Gross Margin and COGS Contribution
- **Domain**: Finance Intelligence
- **Formula**: `(Net Sales - COGS) / Net Sales * 100 GROUP BY category_name`
- **Grain**: Product Category Grain
- **Tables**: `sales.order_items`, `products.products`, `core.dim_category`, `sales.orders`
- **Feasibility**: Derivable
- **Management Action**: Re-negotiate supplier cost prices on low-margin merchandise lines.

### KPI 3.5: Treasury Liquidity and Bank Account Balance Distribution
- **Domain**: Finance Intelligence
- **Formula**: `SUM(balance) GROUP BY account_type`
- **Grain**: Account Type Grain
- **Tables**: `finance.accounts`
- **Feasibility**: Directly Available
- **Management Action**: Rebalance cash balances between operating accounts and interest-bearing deposits.

### KPI 3.6: Inter-Account Fund Transfer Velocity and Status
- **Domain**: Finance Intelligence
- **Formula**: `COUNT(*), SUM(amount) GROUP BY status`
- **Grain**: Transfer Status Grain
- **Tables**: `finance.transfer_log`
- **Feasibility**: Directly Available
- **Management Action**: Investigate failed banking transfer events with financial partners.

### KPI 3.7: Customer Payment Settlement Success Rate by Tender Mode
- **Domain**: Finance Intelligence
- **Formula**: `(COUNT(Completed) / COUNT(*)) * 100 GROUP BY payment_mode`
- **Grain**: Payment Mode Grain
- **Tables**: `finance.payments`, `sales.orders`, `finance.payment_modes`
- **Feasibility**: Derivable
- **Management Action**: Route customer transactions through higher-reliability payment gateways.

### KPI 3.8: Customer Refund Volume and Financial Leakage Impact
- **Domain**: Finance Intelligence
- **Formula**: `SUM(refund_amount) GROUP BY reason`
- **Grain**: Return Reason Grain
- **Tables**: `sales.returns`
- **Feasibility**: Directly Available
- **Management Action**: Penalize suppliers supplying merchandise with high defect return rates.

### KPI 3.9: Regional Sales Revenue and Operating Profitability
- **Domain**: Finance Intelligence
- **Formula**: `(Regional Sales - Regional Store OPEX) GROUP BY region_name`
- **Grain**: Geographic Region Grain
- **Tables**: `sales.orders`, `stores.stores`, `core.dim_region`, `stores.expenses`
- **Feasibility**: Derivable
- **Management Action**: Prioritize marketing investment in top-margin sales regions.

---

## 4. Cross-Functional Integration KPIs

### KPI 4.1: Revenue per Employee by Sales Region
- **Domain**: Cross-Functional
- **Formula**: `Regional Delivered Revenue / Regional Staff Headcount`
- **Grain**: Regional Productivity Grain
- **Tables**: `sales.orders`, `stores.stores`, `core.dim_region`, `stores.employees`
- **Feasibility**: Derivable
- **Management Action**: Implement regional sales training where revenue per employee lags benchmark.

### KPI 4.2: Store Staffing Density vs. Store Sales Throughput
- **Domain**: Cross-Functional
- **Formula**: `Store Delivered Sales vs Store Staff Headcount`
- **Grain**: Retail Store Grain
- **Tables**: `sales.orders`, `stores.stores`, `stores.employees`
- **Feasibility**: Derivable
- **Management Action**: Reallocate personnel from low-volume to high-volume branches.

### KPI 4.3: Department Payroll vs. Operational Expenses
- **Domain**: Cross-Functional
- **Formula**: `Annualized Base Payroll vs Operational Overhead by Department`
- **Grain**: Department Grain
- **Tables**: `stores.employees`, `core.dim_department`
- **Feasibility**: Derivable
- **Management Action**: Review organizational department budgets where personnel costs outpace output.

### KPI 4.4: Shift Length Overtime Prevalence vs. Attendance Regularity
- **Domain**: Cross-Functional
- **Formula**: `(Overtime Shifts >9.5h / Total Shifts) * 100`
- **Grain**: Store Grain
- **Tables**: `hr.attendance`, `stores.employees`, `stores.stores`
- **Feasibility**: Derivable
- **Management Action**: Curb overtime hours by ensuring baseline staffing levels are met.

### KPI 4.5: Store Operational Contribution Profit [PROXY]
- **Domain**: Cross-Functional
- **Formula**: `Store Sales - Store COGS - Store Expenses - Store Payroll`
- **Grain**: Retail Store Grain
- **Tables**: `sales.orders`, `sales.order_items`, `products.products`, `stores.expenses`, `stores.employees`, `stores.stores`
- **Feasibility**: Proxy Metric `[PROXY]`
- **Management Action**: Create operational improvement plans for retail stores operating at a loss.

### KPI 4.6: Labor Cost Intensity Benchmark across Store Size Tiers
- **Domain**: Cross-Functional
- **Formula**: `(Total Store Payroll / Total Store Sales) * 100 GROUP BY Size Tier`
- **Grain**: Store Format Tier Grain
- **Tables**: `stores.stores`, `stores.employees`, `sales.orders`
- **Feasibility**: Derivable
- **Management Action**: Standardize staffing rosters based on retail square footage tiers.\n