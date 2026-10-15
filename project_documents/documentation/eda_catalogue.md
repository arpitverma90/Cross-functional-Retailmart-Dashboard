# RetailMart V3 - Comprehensive EDA Catalogue
## Management-Focused Exploratory Data Analysis Specifications

---

### EDA Item 1: Seasonality & Monthly Revenue Velocity
- **EDA Question**: How has monthly net sales revenue and order volume evolved across the 26-month operating history, and what seasonal inflection points exist?
- **Domain & Purpose**: Executive Summary & Sales — evaluates top-line commercial trajectory and identifies peak vs lean demand cycles.
- **Tables, Columns & Join**: `sales.orders` (`order_date`, `net_total`, `order_status`) joined with `core.dim_date` (`date_key`).
- **Method**: Time-series monthly aggregation with MoM and YoY percentage delta calculations using `LAG()` window functions.
- **Time Grain**: Monthly (2024-01 to 2026-02).
- **Suggested Visual**: Dual-axis line and bar chart (ApexCharts combo: bars for delivered order volume, purple line for net revenue).
- **Expected Insight**: Reveal holiday demand surges (e.g., Q4/festive quarters) and recent momentum heading into 2026.
- **Expected Decision**: Supply chain procurement and inventory buffer adjustments ahead of high-volume seasonal quarters.
- **Feasibility & Limitation**: **Directly Feasible**; requires standard `WHERE order_status = 'Delivered'` filter.

---

### EDA Item 2: Product Category Contribution & Pricing Power
- **EDA Question**: Which product categories generate the highest net revenue and gross margins, and how does average selling price correlate with sales volume?
- **Domain & Purpose**: Sales Dashboard — identifies high-yield merchandise lines versus commoditized low-margin categories.
- **Tables, Columns & Join**: `sales.order_items` (`quantity`, `net_amount`, `prod_id`) $\bowtie$ `products.products` (`price`, `cost_price`) $\bowtie$ `core.dim_brand` $\bowtie$ `core.dim_category` (`category_name`).
- **Method**: Cross-sectional category Pareto aggregation and margin percentage computation.
- **Time Grain**: Full historical dataset and trailing 12 months.
- **Suggested Visual**: Horizontal bar chart of Category Revenue sorted descending, paired with a margin percentage bubble overlay.
- **Expected Insight**: Highlights the top 3 categories that drive over 60% of total revenue.
- **Expected Decision**: Reallocate vendor merchandising budgets and shelf space toward categories with both high velocity and strong margin.
- **Feasibility & Limitation**: **Directly Feasible**; requires joins from `order_items` to `products` and `dim_brand` to `dim_category`.

---

### EDA Item 3: RFM Customer Deciles & Churn Probability
- **EDA Question**: What proportion of the customer base qualifies as high-value 'Champions' vs 'At-Risk' churn candidates, and what is their relative revenue impact?
- **Domain & Purpose**: Customer Dashboard — drives customer lifetime value optimization and prevents churn among top spenders.
- **Tables, Columns & Join**: `sales.orders` (`cust_id`, `order_date`, `net_total`) $\bowtie$ `customers.customers` (`tier`).
- **Method**: Recency, Frequency, Monetary quintile scoring (`NTILE(5)`) anchored to current operating date `2026-02-26`.
- **Time Grain**: Customer lifecycle view.
- **Suggested Visual**: Scatter/bubble matrix (X-axis: Recency days, Y-axis: Frequency, Bubble size: Total net spend, Color: RFM Segment).
- **Expected Insight**: Pinpoints high-spending VIP customers who have not placed an order in over 90 days.
- **Expected Decision**: Automated high-priority alerts to customer success and dedicated retention promotional campaigns.
- **Feasibility & Limitation**: **Derivable**; churn probability is a heuristic proxy based on recency inactivity.

---

### EDA Item 4: Courier SLA Lead Time & Delivery Reliability
- **EDA Question**: Which courier partners meet the $\le 5$-day transit SLA, and where are the primary parcel delivery bottlenecks geographically?
- **Domain & Purpose**: Operations Dashboard — evaluates logistics carrier contracts and regional delivery efficiency.
- **Tables, Columns & Join**: `sales.shipments` (`courier_name`, `shipped_date`, `delivered_date`, `status`) $\bowtie$ `sales.orders` $\bowtie$ `stores.stores` $\bowtie$ `core.dim_region` (`region_name`).
- **Method**: Transit duration distribution analysis, percentile lead times (P50, P90), and SLA breach percentages.
- **Time Grain**: Monthly and overall carrier performance.
- **Suggested Visual**: Multi-bar chart comparing SLA compliance % alongside average lead time in days by courier.
- **Expected Insight**: Reveals carriers with chronic delivery delays in specific geographical zones.
- **Expected Decision**: Enforce contractual SLA penalty clauses or adjust carrier allocation weighting.
- **Feasibility & Limitation**: **Directly Feasible**; calculated on delivered parcels where `delivered_date` is not null.

---

### EDA Item 5: Factory Quality Rejection vs Product Return Rates
- **EDA Question**: Is there a direct statistical correlation between manufacturing scrap/rejection rates on the shop floor and subsequent customer product return rates for defective merchandise?
- **Domain & Purpose**: Cross-Functional Dashboard — bridges factory production operations with downstream customer satisfaction.
- **Tables, Columns & Join**: `manufacture.work_orders` (`product_id`, `rejected_quantity`, `quantity_produced`) $\bowtie$ `products.products` $\bowtie$ `sales.returns` (`reason = 'Defective'`).
- **Method**: Bivariate correlation and category defect-rate alignment.
- **Time Grain**: Production batch and return quarterly cycles.
- **Suggested Visual**: Side-by-side comparative bar chart or dual scatter plot linking factory scrap rate to defect return rate.
- **Expected Insight**: Identifies whether customer return spikes are triggered by production assembly flaws or transit damage.
- **Expected Decision**: Root-cause preventive engineering on offending assembly lines and stricter pre-shipment QA checks.
- **Feasibility & Limitation**: **Derivable**; work orders track manufactured SKU runs while returns specify defective items.
