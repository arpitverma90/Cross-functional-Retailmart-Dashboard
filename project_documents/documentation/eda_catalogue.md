# RetailMart V3 - Exploratory Data Analysis (EDA) Catalogue (HR & Finance Dedicated)
## In-Depth Management Investigation Queries

This catalogue defines exploratory data analysis queries and investigative deep-dives across Departmental salary compression, Attendance presenteeism patterns, Monthly operating jaws, Store efficiency quartiles, Cash transfer failures, and Statutory tax burdens.

---

### EDA 5.1: Departmental Salary Compression & Outlier Variance
- **EDA Question**: Does salary compression or extreme pay inequality exist within specific departments?
- **Domain and Purpose**: HR Analytics — audits pay equity, interquartile range (IQR), and salary dispersion across organizational divisions.
- **Tables, Columns and Join**: `stores.employees e JOIN core.dim_department d ON e.dept_id = d.dept_id`
- **Method**: Statistical dispersion analysis (Min, P25, Median, P75, Max, IQR spread).
- **Time Grain**: Cross-sectional snapshot
- **Suggested Visual**: Box-and-whisker plot or statistical summary table.
- **Expected Insight**: Identification of departments with high wage compression or wide outlier spreads.
- **Expected Decision**: Adjust compensation bands to maintain competitive and equitable pay structures.
- **Feasibility and Limitation**: Fully feasible on verified `stores.employees.salary` data.

### EDA 5.2: Attendance Presenteeism & Clock-In Dispersion Patterns
- **EDA Question**: At what hours do retail employees predominantly clock in, and how does shift length vary by arrival time?
- **Domain and Purpose**: HR Analytics — examines peak arrival times and punctuality distribution.
- **Tables, Columns and Join**: `hr.attendance` (check_in, check_out)
- **Method**: Hourly frequency segmentation and duration averaging.
- **Time Grain**: Hourly clock-in grain
- **Suggested Visual**: Hourly bar distribution chart.
- **Expected Insight**: Distribution of shifts across early morning, standard morning, and afternoon openings.
- **Expected Decision**: Align store opening rosters with observed employee clock-in patterns.
- **Feasibility and Limitation**: Fully feasible; records with null check-in/out excluded.

### EDA 5.3: Monthly Revenue vs. Operating Expenses Operating Jaw Analysis
- **EDA Question**: Are operating costs growing faster than commercial sales revenue over time?
- **Domain and Purpose**: Finance Analytics — evaluates operating leverage and jaw spread (Revenue Growth % - OPEX Growth %).
- **Tables, Columns and Join**: CTE combining `sales.orders`, `finance.expenses`, and `stores.expenses` by month.
- **Method**: Time-series cohort comparison and Month-over-Month (MoM) delta analysis.
- **Time Grain**: Monthly grain (2024 to 2026)
- **Suggested Visual**: Dual-axis line chart tracking Revenue vs. OPEX growth with jaw spread bars.
- **Expected Insight**: Pinpoints periods where expense inflation eroded operating margins.
- **Expected Decision**: Impose immediate discretionary spending freezes when operating jaws turn negative.
- **Feasibility and Limitation**: Derivable from validated orders and expense records.

### EDA 5.4: Store Efficiency Quartile Analysis: Staff vs. Sales Outliers
- **EDA Question**: Which retail stores deliver top-tier sales productivity per worker, and which lag in the bottom quartile?
- **Domain and Purpose**: Cross-Functional Analytics — classifies 200 retail stores into efficiency quartiles based on revenue per employee.
- **Tables, Columns and Join**: `stores.stores s LEFT JOIN stores.employees e ON s.store_id = e.store_id LEFT JOIN sales.orders o ON s.store_id = o.store_id`
- **Method**: NTILE(4) quartile segmentation based on revenue per head.
- **Time Grain**: Portfolio-level aggregate
- **Suggested Visual**: Quartile comparison cards and scatter plot (Staff vs. Sales).
- **Expected Insight**: Clear demarcation between high-efficiency flagship stores and low-productivity outliers.
- **Expected Decision**: Deploy store excellence teams to bottom-quartile branches to overhaul operations.
- **Feasibility and Limitation**: Fully supported by pre-aggregated store sales and employee counts.

### EDA 5.5: Cash Liquidity Risk & Inter-Account Failure Investigation
- **EDA Question**: What accounts are involved in failed inter-account transfers, and what is the monetary exposure?
- **Domain and Purpose**: Finance Analytics — investigates banking transfer rejections to safeguard corporate liquidity.
- **Tables, Columns and Join**: `finance.transfer_log t JOIN finance.accounts a1 ON t.from_account = a1.account_id JOIN finance.accounts a2 ON t.to_account = a2.account_id WHERE status = 'Failed'`
- **Method**: Exception filtering and transaction ranking.
- **Time Grain**: Transaction event grain
- **Suggested Visual**: Exception audit table with highlighted failure amounts.
- **Expected Insight**: Isolates high-value failed transfers and source/target account holders.
- **Expected Decision**: Instruct treasury desk to re-authenticate credentials or rectify routing details.
- **Feasibility and Limitation**: Directly available in `finance.transfer_log`.

### EDA 5.6: Effective Statutory Tax Burden across Salary Tranches
- **EDA Question**: Does the effective income tax deduction rate scale progressively across employee compensation tiers?
- **Domain and Purpose**: HR & Finance Analytics — audits tax withholding progressivity across entry, mid, senior, and executive pay bands.
- **Tables, Columns and Join**: `payroll.pay_slips` (gross_salary, income_tax)
- **Method**: Income tier segmentation and effective tax rate calculation (`Income Tax / Gross Salary * 100`).
- **Time Grain**: Annual/Monthly payslip grain
- **Suggested Visual**: Progressive bar chart showing effective tax rate by compensation bracket.
- **Expected Insight**: Verifies statutory tax progression across employee compensation bands.
- **Expected Decision**: Validate payroll withholding algorithms against statutory income tax slabs.
- **Feasibility and Limitation**: Directly calculated from itemized payslip records.\n