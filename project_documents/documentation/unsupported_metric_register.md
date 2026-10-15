# RetailMart V3 - Unsupported Metric Register
## Analytical Governance & Feasibility Boundaries

In compliance with the project's **Non-Negotiable Analytical Rules**, this register formally documents metrics that cannot be calculated reliably from the available 16-schema, 55-table database without making unverified assumptions.

---

| Metric Name | Requested / Candidate Domain | Why It Is Not Feasible | Missing Required Data / Relational Gap | Approved Proxy or Alternative Measure |
| :--- | :--- | :--- | :--- | :--- |
| **True Corporate EBITDA** | Finance / Executive | The database lacks comprehensive financial accounting statements (COGS schedules, enterprise depreciation & amortization, corporate interest expense, tax schedules). | `finance.expenses` records operational cash outflows but lacks full balance sheet & P&L accounting structures. | **Store Operating Margin**: `SUM(net_total) - SUM(unit cost) - SUM(store expenses)`. |
| **Customer Acquisition Cost (CAC)** | Marketing / Customer | Advertising expenditures in `marketing.ads_spend` are tracked at the campaign level by platform, but there is no clickstream attribution key connecting ad spend to individual customer registrations. | No customer tracking ID or UTM touchpoint key in `customers.customers` linking to `marketing.ads_spend`. | **Campaign Blended Cost per Click/Impression**: Analyzed strictly at campaign aggregate level in marketing context. |
| **Return on Ad Spend (ROAS) at SKU Level** | Marketing / Sales | Ad campaigns promote broad brand initiatives (`marketing.campaigns`), not individual product line items. | No SKU or `product_id` column in `marketing.campaigns` or `marketing.ads_spend`. | **Brand/Category Promo Lift**: Measuring incremental sales during active promo windows (`products.promotions`). |
| **Employee Attrition Rate** | HR / Operations | Employee records track hiring dates (`stores.employees.joining_date`) but have no exit, resignation, or termination date column. | Missing `termination_date` or `status` in `stores.employees`. | **Store Staffing Density & Labor Expense**: `COUNT(employee_id)` per store and average store salary expense. |
| **Warehouse Cubic Capacity Utilization** | Operations / Supply Chain | Warehouses record `capacity_sqft`, but inventory snapshots record discrete SKU unit counts without carton cubic dimensions or pallet storage factors. | No package volume ($L \times W \times H$) or pallet conversion factors in `products.products`. | **Warehouse SKU Count & Unit Density**: Tracking total units on hand over time across warehouse distribution centers. |
| **Predictive Churn Probability** | Customer | Machine learning survival models or probability scores are not pre-computed or stored in the database. | No churn label or machine learning inference outputs in customer schemas. | **Recency Inactivity Proxy**: Customers with zero orders in $>90$ days vs their historical purchase cadence. |

---

## Governance Rules
1. No unapproved metric from this register may be labeled as a verified financial or operational fact on any dashboard page.
2. If an alternative or proxy metric is presented, it must be explicitly marked with the `[PROXY]` badge and accompanied by documented calculation logic.
