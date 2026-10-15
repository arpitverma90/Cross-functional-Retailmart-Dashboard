# Phase 1: Row-Count Reconciliation Report
## RetailMart V3 Database Layer (PostgreSQL 18.4)

- **Target Database**: `accio_retailmart_27` on `localhost:5432`
- **Total Tables**: 55 across 16 Schemas
- **Total Ingested Rows**: **2,391,602**
- **Reconciliation Status**: **100.00% MATCH (0 Mismatches)**
- **Audit Timestamp**: 2026-09-10

---

## Detailed Table-by-Table Reconciliation

| Schema | Table Name | Source CSV Rows | PostgreSQL DB Rows | Variance | Status | Table Grain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `core` | `dim_date` | 788 | 788 | 0 | **MATCH** | 1 row per calendar day (2024-01-01 to 2026-02-26) |
| `core` | `dim_region` | 20 | 20 | 0 | **MATCH** | 1 row per geographic sales region |
| `core` | `dim_category` | 10 | 10 | 0 | **MATCH** | 1 row per top product category |
| `core` | `dim_brand` | 117 | 117 | 0 | **MATCH** | 1 row per product brand |
| `core` | `dim_department` | 10 | 10 | 0 | **MATCH** | 1 row per organizational department |
| `core` | `dim_expense_category` | 15 | 15 | 0 | **MATCH** | 1 row per operational expense category |
| `stores` | `stores` | 200 | 200 | 0 | **MATCH** | 1 row per physical retail store |
| `stores` | `employees` | 3,000 | 3,000 | 0 | **MATCH** | 1 row per store staff/management employee |
| `stores` | `expenses` | 20,000 | 20,000 | 0 | **MATCH** | 1 row per retail store operating expense item |
| `products` | `suppliers` | 117 | 117 | 0 | **MATCH** | 1 row per merchandise supplier |
| `products` | `products` | 6,036 | 6,036 | 0 | **MATCH** | 1 row per SKU / product catalog entry |
| `products` | `inventory` | 114,153 | 114,153 | 0 | **MATCH** | Store-level SKU inventory (`store_id` × `product_id`) |
| `products` | `promotions` | 800 | 800 | 0 | **MATCH** | 1 row per marketing promotional discount |
| `customers` | `customers` | 50,000 | 50,000 | 0 | **MATCH** | 1 row per registered customer account |
| `customers` | `addresses` | 50,000 | 50,000 | 0 | **MATCH** | 1 row per customer delivery address |
| `customers` | `reviews` | 30,000 | 30,000 | 0 | **MATCH** | 1 row per customer product rating & review |
| `customers` | `loyalty_points` | 25,000 | 25,000 | 0 | **MATCH** | 1 row per loyalty point issuance event |
| `customers` | `wallets` | 50,000 | 50,000 | 0 | **MATCH** | 1 row per customer digital wallet balance |
| `sales` | `orders` | 150,000 | 150,000 | 0 | **MATCH** | 1 row per customer commercial purchase order |
| `sales` | `order_items` | 375,202 | 375,202 | 0 | **MATCH** | 1 row per ordered SKU item (1–4 items/order) |
| `sales` | `payments` | 142,450 | 142,450 | 0 | **MATCH** | 1 row per payment transaction attempt |
| `sales` | `shipments` | 104,987 | 104,987 | 0 | **MATCH** | 1 row per customer outbound parcel shipment |
| `sales` | `returns` | 7,465 | 7,465 | 0 | **MATCH** | 1 row per item refund & return request |
| `finance` | `payment_modes` | 9 | 9 | 0 | **MATCH** | 1 row per recognized payment tender type |
| `finance` | `accounts` | 200 | 200 | 0 | **MATCH** | 1 row per internal corporate ledger account |
| `finance` | `transfer_log` | 500 | 500 | 0 | **MATCH** | 1 row per fund transfer between accounts |
| `finance` | `payments` | 142,450 | 142,450 | 0 | **MATCH** | 1 row per financial settlement & refund log |
| `finance` | `expenses` | 40,000 | 40,000 | 0 | **MATCH** | 1 row per corporate non-store expense |
| `finance` | `revenue_summary` | 788 | 788 | 0 | **MATCH** | 1 row per historical daily revenue summary |
| `hr` | `attendance` | 88,310 | 88,310 | 0 | **MATCH** | 1 row per daily employee clock-in record |
| `hr` | `salary_history` | 36,000 | 36,000 | 0 | **MATCH** | 1 row per monthly employee salary payment |
| `payroll` | `tax_brackets` | 6 | 6 | 0 | **MATCH** | 1 row per statutory income tax bracket |
| `payroll` | `pay_slips` | 12,000 | 12,000 | 0 | **MATCH** | 1 row per detailed employee salary pay slip |
| `marketing` | `campaigns` | 250 | 250 | 0 | **MATCH** | 1 row per multi-channel marketing campaign |
| `marketing` | `ads_spend` | 4,000 | 4,000 | 0 | **MATCH** | 1 row per daily platform advertising spend |
| `marketing` | `email_clicks` | 500 | 500 | 0 | **MATCH** | 1 row per email campaign performance blast |
| `support` | `tickets` | 10,000 | 10,000 | 0 | **MATCH** | 1 row per customer support case ticket |
| `call_center` | `calls` | 25,000 | 25,000 | 0 | **MATCH** | 1 row per inbound customer service phone call |
| `call_center` | `transcripts` | 25,000 | 25,000 | 0 | **MATCH** | 1 row per speech-to-text transcript & NLP score |
| `supply_chain` | `warehouses` | 5 | 5 | 0 | **MATCH** | 1 row per central regional distribution warehouse |
| `supply_chain` | `shipments` | 2,000 | 2,000 | 0 | **MATCH** | 1 row per supplier inbound bulk inventory freight |
| `supply_chain` | `inventory_snapshots` | 36,500 | 36,500 | 0 | **MATCH** | Warehouse SKU daily stock snapshot (365 days) |
| `manufacture` | `production_lines` | 10 | 10 | 0 | **MATCH** | 1 row per manufacturing assembly line |
| `manufacture` | `work_orders` | 15,000 | 15,000 | 0 | **MATCH** | 1 row per factory production batch run |
| `loyalty` | `tiers` | 4 | 4 | 0 | **MATCH** | 1 row per loyalty club tier (Bronze, Silver, Gold, Platinum) |
| `loyalty` | `members` | 30,000 | 30,000 | 0 | **MATCH** | 1 row per customer loyalty club member profile |
| `loyalty` | `redemptions` | 10,000 | 10,000 | 0 | **MATCH** | 1 row per loyalty reward points redemption |
| `web_events` | `page_views` | 500,000 | 500,000 | 0 | **MATCH** | 1 row per ecommerce storefront page view |
| `web_events` | `events` | 200,000 | 200,000 | 0 | **MATCH** | 1 row per user interaction click / cart event |
| `audit` | `application_logs` | 20,000 | 20,000 | 0 | **MATCH** | 1 row per application diagnostic log event |
| `audit` | `api_requests` | 50,000 | 50,000 | 0 | **MATCH** | 1 row per HTTP REST API request trace |
| `audit` | `record_changes` | 10,000 | 10,000 | 0 | **MATCH** | 1 row per database row modification audit trace |
| `audit` | `refund_log` | 2,000 | 2,000 | 0 | **MATCH** | 1 row per financial refund transaction trace |
| `audit` | `refund_failures` | 200 | 200 | 0 | **MATCH** | 1 row per failed customer refund event |
| `audit` | `procedure_calls` | 500 | 500 | 0 | **MATCH** | 1 row per database stored procedure audit |
| **TOTAL** | **55 TABLES** | **2,391,602** | **2,391,602** | **0** | **PASSED** | **100% Reconciled Across All 16 Schemas** |

---

## Technical Notes & Findings
- `customers.addresses`: When counting raw physical text lines via `wc -l`, an apparent discrepancy of 24,946 lines appeared due to multi-line street address strings with embedded newlines enclosed in RFC-4180 double quotes. Correct logical CSV parsing yields exactly 50,000 records, matching PostgreSQL table row count 1-to-1.
- No duplicate records or primary key collisions exist in any of the 55 tables.
