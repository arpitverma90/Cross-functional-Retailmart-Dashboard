# Phase 2: Data Quality & Wrangling Summary
## RetailMart V3 Analytical Database Layer

- **Audit Standard**: 5 Pillars of Enterprise Data Quality (Completeness, Accuracy, Consistency, Timeliness, Uniqueness)
- **Database Tested**: `accio_retailmart_27` (PostgreSQL 18.4)
- **Audit Suite**: `scripts/verify_data_quality.py`
- **Result**: **27/27 Quality Checks Passed (100.0%)**

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

### Pillar 2: Accuracy & Domain Boundaries
| Evaluation Check | Target Condition | Violations | Status | Mitigation / Finding |
| :--- | :--- | :--- | :--- | :--- |
| Non-Negative Net Revenue | `sales.orders.net_total < 0` | 0 | **PASSED** | All order financial totals are strictly $\ge 0$. |
| Reasonable Discounts | `discount_amount > gross_total` | 0 | **PASSED** | No discounts exceed gross totals. |
| Positive Item Quantities | `sales.order_items.quantity <= 0` | 0 | **PASSED** | All order line items represent positive purchase quantities. |
| Non-Negative Unit Prices | `sales.order_items.unit_price < 0`| 0 | **PASSED** | Unit selling prices are positive. |
| Non-Negative Cost Prices | `products.products.cost_price < 0`| 0 | **PASSED** | Base COGS is strictly non-negative. |
| Chronological Delivery Flow | `delivered_date < shipped_date` | 0 | **PASSED** | Zero chronological inversions in parcel logistics. |
| Work Order Scrap Boundary | `rejected_quantity > quantity_produced` | 0 | **PASSED** | Factory quality scrap is bounded by total run quantity. |
| Non-Negative Retail Stock | `products.inventory.quantity_on_hand < 0` | 0 | **PASSED** | Store physical inventory has zero negative stock. |

### Pillar 3: Consistency & Cross-Grain Reconciliation
| Evaluation Check | Reconciled Tables | Observed Metrics | Variance | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Delivered Revenue Alignment** | `sales.orders` vs `sales.order_items` | Orders: ₹6,769,536,004.48<br>Items: ₹6,769,536,004.48 | ₹0.00 | **PASSED (100.0%)** |
| Customer Foreign Keys | `sales.orders` $\to$ `customers` | 150,000 valid orders | 0 Orphans | **PASSED** |
| Order Line Items Foreign Keys | `sales.order_items` $\to$ `orders` | 375,202 valid items | 0 Orphans | **PASSED** |
| Logistics Parcel Foreign Keys | `sales.shipments` $\to$ `orders` | 104,987 valid parcels | 0 Orphans | **PASSED** |
| Customer Return Foreign Keys | `sales.returns` $\to$ `orders` | 7,465 valid returns | 0 Orphans | **PASSED** |

### Pillar 4: Timeliness & Temporal Horizon
- **Observed Date Span**: `2024-01-01` to `2026-02-26` (788 calendar days).
- **Calendar Alignment**: Strictly matches `core.dim_date` spanning identical 788 daily keys.
- **Status**: **PASSED**.

### Pillar 5: Uniqueness & Primary Key Integrity
- `sales.orders` (`order_id`): 150,000 distinct PKs, 0 duplicates.
- `sales.order_items` (`order_item_id`): 375,202 distinct PKs, 0 duplicates.
- `customers.customers` (`customer_id`): 50,000 distinct PKs, 0 duplicates.
- `products.products` (`product_id`): 6,036 distinct PKs, 0 duplicates.
- `stores.stores` (`store_id`): 200 distinct PKs, 0 duplicates.
- `sales.shipments` (`shipment_id`): 104,987 distinct PKs, 0 duplicates.
- `sales.returns` (`return_id`): 7,465 distinct PKs, 0 duplicates.
- **Status**: **PASSED**.
