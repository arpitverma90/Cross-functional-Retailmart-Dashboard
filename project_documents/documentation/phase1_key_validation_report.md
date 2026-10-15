# Phase 1: Key Validation & Referential Integrity Report
## RetailMart V3 Relational Database Layer

- **Target Database**: `accio_retailmart_27` (PostgreSQL 18.4)
- **Total Foreign Key & Cardinality Checks**: 43 Key Relationships Verified
- **Orphan Records Found**: **0 (Zero Orphan Records)**
- **Audit Date**: 2026-09-10

---

## 1. Referential Integrity Audit Results

All foreign key pairs were tested using left outer joins against non-null child columns:
`SELECT count(*) FROM child c LEFT JOIN parent p ON c.fk = p.pk WHERE c.fk IS NOT NULL AND p.pk IS NULL;`

| Child Table | Foreign Key Column | Parent Table | Referenced Column | Status | Orphan Count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sales.orders` | `cust_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `sales.orders` | `store_id` | `stores.stores` | `store_id` | **PASSED** | 0 |
| `sales.orders` | `payment_mode_id` | `finance.payment_modes` | `mode_id` | **PASSED** | 0 |
| `sales.order_items` | `order_id` | `sales.orders` | `order_id` | **PASSED** | 0 |
| `sales.order_items` | `prod_id` | `products.products` | `product_id` | **PASSED** | 0 |
| `sales.payments` | `order_id` | `sales.orders` | `order_id` | **PASSED** | 0 |
| `sales.shipments` | `order_id` | `sales.orders` | `order_id` | **PASSED** | 0 |
| `sales.returns` | `order_id` | `sales.orders` | `order_id` | **PASSED** | 0 |
| `sales.returns` | `prod_id` | `products.products` | `product_id` | **PASSED** | 0 |
| `customers.addresses` | `customer_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `customers.reviews` | `customer_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `customers.reviews` | `product_id` | `products.products` | `product_id` | **PASSED** | 0 |
| `customers.loyalty_points` | `customer_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `customers.wallets` | `cust_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `products.products` | `brand_id` | `core.dim_brand` | `brand_id` | **PASSED** | 0 |
| `products.products` | `supplier_id` | `products.suppliers` | `supplier_id` | **PASSED** | 0 |
| `products.inventory` | `store_id` | `stores.stores` | `store_id` | **PASSED** | 0 |
| `products.inventory` | `product_id` | `products.products` | `product_id` | **PASSED** | 0 |
| `stores.stores` | `region_id` | `core.dim_region` | `region_id` | **PASSED** | 0 |
| `stores.employees` | `store_id` | `stores.stores` | `store_id` | **PASSED** | 0 |
| `stores.employees` | `dept_id` | `core.dim_department` | `dept_id` | **PASSED** | 0 |
| `stores.expenses` | `store_id` | `stores.stores` | `store_id` | **PASSED** | 0 |
| `supply_chain.shipments` | `supplier_id` | `products.suppliers` | `supplier_id` | **PASSED** | 0 |
| `supply_chain.shipments` | `warehouse_id` | `supply_chain.warehouses` | `warehouse_id` | **PASSED** | 0 |
| `supply_chain.shipments` | `product_id` | `products.products` | `product_id` | **PASSED** | 0 |
| `supply_chain.inventory_snapshots` | `warehouse_id` | `supply_chain.warehouses` | `warehouse_id` | **PASSED** | 0 |
| `supply_chain.inventory_snapshots` | `product_id` | `products.products` | `product_id` | **PASSED** | 0 |
| `manufacture.work_orders` | `product_id` | `products.products` | `product_id` | **PASSED** | 0 |
| `manufacture.work_orders` | `line_id` | `manufacture.production_lines` | `line_id` | **PASSED** | 0 |
| `support.tickets` | `customer_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `support.tickets` | `agent_id` | `stores.employees` | `employee_id` | **PASSED** | 0 |
| `call_center.calls` | `customer_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `call_center.calls` | `agent_id` | `stores.employees` | `employee_id` | **PASSED** | 0 |
| `call_center.transcripts` | `call_id` | `call_center.calls` | `call_id` | **PASSED** | 0 |
| `loyalty.members` | `customer_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `loyalty.members` | `tier_id` | `loyalty.tiers` | `tier_id` | **PASSED** | 0 |
| `loyalty.redemptions` | `customer_id` | `customers.customers` | `customer_id` | **PASSED** | 0 |
| `finance.expenses` | `exp_cat_id` | `core.dim_expense_category` | `exp_cat_id` | **PASSED** | 0 |
| `hr.attendance` | `employee_id` | `stores.employees` | `employee_id` | **PASSED** | 0 |
| `hr.salary_history` | `employee_id` | `stores.employees` | `employee_id` | **PASSED** | 0 |
| `payroll.pay_slips` | `employee_id` | `stores.employees` | `employee_id` | **PASSED** | 0 |
| `audit.record_changes` | `changed_by` | `stores.employees` | `employee_id` | **PASSED** | 0 |
| `audit.refund_log` | `order_id` | `sales.orders` | `order_id` | **PASSED** | 0 |

---

## 2. Cardinality & Multiplicity Confirmation

1. **`sales.orders` to `sales.order_items`**: 1 to 1..4 (One-to-Many). 112,612 orders have more than 1 item. Direct joins without item aggregation multiply order rows.
2. **`sales.orders` to `sales.shipments`**: 1 to 0..1 (One-to-Zero-or-One). Out of 150,000 orders, 104,987 have shipped. Max shipments per order is strictly 1.
3. **`sales.orders` to `sales.returns`**: 1 to 0..1 (One-to-Zero-or-One). Out of 150,000 orders, 7,465 have returns. Max returns per order is strictly 1.
4. **`sales.orders` to `sales.payments`**: 1 to 0..1 (One-to-Zero-or-One). Out of 150,000 orders, 142,450 have payment records. Max payments per order is strictly 1.
5. **`customers.customers` to `customers.addresses`**: 1 to 1 (One-to-One in current database: 50,000 customers map to 50,000 address records).

---

## 3. Commercial Revenue Reconciliation Confirmation

- **Total Commercial Orders**: 150,000
- **Total Delivered Orders**: 82,540
- **Total Delivered Net Revenue (`sales.orders`)**: **₹6,769,536,004.48**
- **Total Delivered Net Amount (`sales.order_items`)**: **₹6,769,536,004.48**
- **Variance**: **₹0.00 (Exact 100.00% match)**
- **Authoritative Headline Revenue Metric**: **₹676.95 Cr**
