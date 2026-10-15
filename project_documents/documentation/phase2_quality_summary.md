# Phase 2: Data Quality & Wrangling Summary
## RetailMart V3 Analytical Database Layer (HR & Finance Focus)

- **Audit Standard**: 5 Pillars of Enterprise Data Quality (Completeness, Accuracy, Consistency, Timeliness, Uniqueness)
- **Database Tested**: `accio_retailmart_27` (PostgreSQL 18.4)
- **Audit Suite**: `scripts/verify_data_quality.py`
- **Result**: **68/68 Quality Checks Passed (100.0%)**

---

## 1. Pillar-by-Pillar Verification Matrix

### Pillar 1: Completeness (Null Rate Evaluation)
| Evaluation Check | Target Table & Column | Null Count | Null Rate | Status |
| :--- | :--- | :--- | :--- | :--- |
| Mandatory Customer in Order | `sales.orders.cust_id` | 0 | 0.00% | **PASSED** |
| Mandatory Order Date | `sales.orders.order_date` | 0 | 0.00% | **PASSED** |
| Mandatory Order Net Total | `sales.orders.net_total` | 0 | 0.00% | **PASSED** |
| Mandatory Product in Line Item | `sales.order_items.prod_id` | 0 | 0.00% | **PASSED** |
| Mandatory Customer Email | `customers.customers.email` | 0 | 0.00% | **PASSED** |
| Mandatory Product Price | `products.products.price` | 0 | 0.00% | **PASSED** |
| Mandatory Employee First Name | `stores.employees.first_name` | 0 | 0.00% | **PASSED** |
| Mandatory Employee Joining Date | `stores.employees.joining_date` | 0 | 0.00% | **PASSED** |
| Mandatory Employee Salary | `stores.employees.salary` | 0 | 0.00% | **PASSED** |
| Mandatory Employee Store ID | `stores.employees.store_id` | 0 | 0.00% | **PASSED** |
| Mandatory Employee Dept ID | `stores.employees.dept_id` | 0 | 0.00% | **PASSED** |
| Mandatory Attendance Employee ID | `hr.attendance.employee_id` | 0 | 0.00% | **PASSED** |
| Mandatory Attendance Date | `hr.attendance.attendance_date` | 0 | 0.00% | **PASSED** |
| Mandatory Payslip Employee ID | `payroll.pay_slips.employee_id` | 0 | 0.00% | **PASSED** |
| Mandatory Payslip Gross Salary | `payroll.pay_slips.gross_salary` | 0 | 0.00% | **PASSED** |
| Mandatory Payslip Net Salary | `payroll.pay_slips.net_salary` | 0 | 0.00% | **PASSED** |
| Mandatory Corporate Expense Category | `finance.expenses.exp_cat_id` | 0 | 0.00% | **PASSED** |
| Mandatory Corporate Expense Amount | `finance.expenses.amount` | 0 | 0.00% | **PASSED** |
| Mandatory Store Expense Store ID | `stores.expenses.store_id` | 0 | 0.00% | **PASSED** |
| Mandatory Store Expense Amount | `stores.expenses.amount` | 0 | 0.00% | **PASSED** |
| Mandatory Account Balance | `finance.accounts.balance` | 0 | 0.00% | **PASSED** |

### Pillar 2: Accuracy & Domain Boundaries
| Evaluation Check | Target Condition | Violations | Status | Mitigation / Finding |
| :--- | :--- | :--- | :--- | :--- |
| Non-Negative Net Revenue | `sales.orders.net_total < 0` | 0 | **PASSED** | All order financial totals are strictly $\ge 0$. |
| Reasonable Discounts | `discount_amount > gross_total` | 0 | **PASSED** | No discounts exceed gross totals. |
| Positive Item Quantities | `sales.order_items.quantity <= 0` | 0 | **PASSED** | All line items represent positive quantities. |
| Non-Negative Unit Prices | `sales.order_items.unit_price < 0`| 0 | **PASSED** | Unit selling prices are positive. |
| Non-Negative Cost Prices | `products.products.cost_price < 0`| 0 | **PASSED** | Base COGS is strictly non-negative. |
| Chronological Delivery Flow | `delivered_date < shipped_date` | 0 | **PASSED** | Zero chronological inversions in parcel delivery. |
| Positive Employee Salary | `stores.employees.salary <= 0` | 0 | **PASSED** | All 3,000 employees have positive salaries. |
| Attendance Chronology | `check_out < check_in` | 0 | **PASSED** | Clock-out strictly occurs after clock-in. |
| Attendance Duration Bounds | Shift duration > 24 hours | 0 | **PASSED** | Average shift is 9.0 hrs; none exceed 24 hrs. |
| Positive Gross Salary | `payroll.pay_slips.gross_salary < 0`| 0 | **PASSED** | Gross compensation is strictly non-negative. |
| Positive Net Salary | `payroll.pay_slips.net_salary < 0` | 0 | **PASSED** | Net payout is strictly non-negative. |
| Net Leq Gross Salary | `net_salary > gross_salary` | 0 | **PASSED** | Deductions ensure net never exceeds gross. |
| Payslip Gross Arithmetic | Gross = Basic + HRA + Allowances | 0 | **PASSED** | 100% arithmetic accuracy (within ₹0.05 rounding). |
| Payslip Net Arithmetic | Net = Gross - Deductions | 0 | **PASSED** | 100% deduction arithmetic accuracy. |
| Positive Corporate Expenses | `finance.expenses.amount <= 0` | 0 | **PASSED** | All 40,000 corporate expenses are positive. |
| Positive Store Expenses | `stores.expenses.amount <= 0` | 0 | **PASSED** | All 20,000 store expenses are positive. |
| Positive Bank Transfers | `finance.transfer_log.amount <= 0`| 0 | **PASSED** | Inter-account transfers are positive values. |
| Distinct Transfer Accounts | `from_account = to_account` | 0 | **PASSED** | No circular transfers to the same account. |

### Pillar 3: Consistency & Cross-Grain Reconciliation
| Evaluation Check | Reconciled Tables | Observed Metrics | Variance | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Delivered Revenue Alignment** | `sales.orders` vs `sales.order_items` | Orders: ₹6,769,536,004.48<br>Items: ₹6,769,536,004.48 | ₹0.00 | **PASSED (100.0%)** |
| Customer Foreign Keys | `sales.orders` $\to$ `customers` | 150,000 valid orders | 0 Orphans | **PASSED** |
| Order Line Items Foreign Keys | `sales.order_items` $\to$ `orders` | 375,202 valid items | 0 Orphans | **PASSED** |
| Employee Store Foreign Keys | `stores.employees` $\to$ `stores.stores` | 3,000 valid employees | 0 Orphans | **PASSED** |
| Employee Dept Foreign Keys | `stores.employees` $\to$ `core.dim_department` | 3,000 valid employees | 0 Orphans | **PASSED** |
| Attendance Employee Foreign Keys | `hr.attendance` $\to$ `stores.employees` | 88,310 valid events | 0 Orphans | **PASSED** |
| Salary History Employee Foreign Keys | `hr.salary_history` $\to$ `stores.employees` | 36,000 valid payouts | 0 Orphans | **PASSED** |
| Payslip Employee Foreign Keys | `payroll.pay_slips` $\to$ `stores.employees` | 12,000 valid slips | 0 Orphans | **PASSED** |
| Corporate Expense Category Keys | `finance.expenses` $\to$ `core.dim_expense_category` | 40,000 valid expenses | 0 Orphans | **PASSED** |
| Store Expense Store Keys | `stores.expenses` $\to$ `stores.stores` | 20,000 valid expenses | 0 Orphans | **PASSED** |
| Transfer Source Account Keys | `finance.transfer_log` $\to$ `finance.accounts` | 500 valid transfers | 0 Orphans | **PASSED** |
| Transfer Target Account Keys | `finance.transfer_log` $\to$ `finance.accounts` | 500 valid transfers | 0 Orphans | **PASSED** |

### Pillar 4: Timeliness & Temporal Horizon
- **Orders Date Span**: `2024-01-01` to `2026-02-26` (788 calendar days).
- **Attendance Date Span**: `2024-01-01` to `2026-02-26` (788 calendar days).
- **Employee Joining Date Span**: `2021-03-31` to `2026-01-31`.
- **Payroll Slips Date Span**: `2024-01-31` to `2025-12-31`.
- **Finance Expenses Date Span**: `2024-01-01` to `2026-02-26`.
- **Store Expenses Date Span**: `2025-02-25` to `2026-02-25`.
- **Status**: **PASSED**.

### Pillar 5: Uniqueness & Primary Key Integrity
- `stores.employees` (`employee_id`): 3,000 distinct PKs, 0 duplicates.
- `hr.attendance` (`attendance_id`): 88,310 distinct PKs, 0 duplicates.
- `payroll.pay_slips` (`pay_slip_id`): 12,000 distinct PKs, 0 duplicates.
- `hr.salary_history` (`payment_id`): 36,000 distinct PKs, 0 duplicates.
- `finance.expenses` (`expense_id`): 40,000 distinct PKs, 0 duplicates.
- `stores.expenses` (`store_expense_id`): 20,000 distinct PKs, 0 duplicates.
- `finance.accounts` (`account_id`): 200 distinct PKs, 0 duplicates.
- `finance.transfer_log` (`transfer_id`): 500 distinct PKs, 0 duplicates.
- `sales.orders` (`order_id`): 150,000 distinct PKs, 0 duplicates.
- `sales.order_items` (`order_item_id`): 375,202 distinct PKs, 0 duplicates.
- `stores.stores` (`store_id`): 200 distinct PKs, 0 duplicates.
- **Status**: **PASSED (100.0% Unique)**.

