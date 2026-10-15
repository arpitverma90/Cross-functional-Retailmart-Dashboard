# RetailMart V3 Enterprise Business Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.13.2-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.4-336791.svg)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/Tests-20%2F20%20Passing-brightgreen.svg)]()
[![Codebase Status](https://img.shields.io/badge/Architecture-Production--Ready-success.svg)]()

A high-performance, responsive, and secure Enterprise Business Intelligence application developed for **RetailMart V3**. Built with a strict **Django MTV (Model-Template-View)** architecture and backed by **PostgreSQL 18.4**, this platform ingests, reconciles, and visualizes **2,391,602 rows** across **55 relational tables** within **16 distinct schemas**.

---

## 🏛️ Executive Summary & Key Highlights

RetailMart V3 is a multi-channel retail powerhouse spanning 200 physical stores across 20 Indian regions, integrated e-commerce delivery networks, in-house manufacturing, and extensive customer touchpoints.

### Key Headline Metrics Reconciled (Horizon: 2024-01-01 to 2026-02-26)
* **Gross Invoiced Orders**: 150,000 orders (₹1,232.14 Cr gross)
* **Delivered Orders**: **82,540 orders**
* **Recognized Net Revenue**: **₹6,769,536,004.48** (**₹676.95 Cr**)
* **Delivered Item Reconciled Sum**: **₹6,769,536,004.48** (**100.00% exact parity**)
* **Product Cost of Goods Sold (COGS)**: ₹4,188,438,400.00 (₹418.84 Cr)
* **Product Gross Margin**: ₹2,581,097,604.48 (38.13%)
* **Customer Return Refunds**: ₹200,996,441.72 (₹20.10 Cr, 2.97% return rate)
* **Store Operating Expenses**: ₹317,665,070.00 (₹31.77 Cr)
* **Net Contribution Margin**: **₹2,062,436,092.76** (**₹206.24 Cr / 30.47%**)
* **On-Time Delivery SLA**: **89.5%**
* **Perfect Order Rate**: **79.8%**

> **Analytical Guardrail Notice**: Financial governance strictly identifies Contribution Margin as Net Revenue less COGS, Return Refunds, and Direct Store Operating Expenses. In the absence of audited corporate tax, debt interest, and capital depreciation schedules, EBITDA/Operating Profit is governed as an uncertified proxy.

---

## 🧭 Dashboard Architecture & Routes

The application features two clearly demarcated areas served under unified session authentication, shared PostgreSQL pushdown querying, cascading filters, and a cohesive corporate dark design system:

```
                          ┌────────────────────────────────────────────────────────┐
                          │         RetailMart V3 Enterprise BI Platform           │
                          └──────────────────────────┬─────────────────────────────┘
                                                     │
                     ┌───────────────────────────────┴───────────────────────────────┐
                     ▼                                                               ▼
        ┌─────────────────────────┐                                    ┌──────────────────────────┐
        │ Area 1: Executive Suite │                                    │ Area 2: Domain Deep-Dive │
        └────────────┬────────────┘                                    └────────────┬─────────────┘
                     │                                                              │
         /executive-summary/                           ┌────────────────────────────┼────────────────────────────┐
       - 10 Headline Enterprise KPIs                   │                            │                            │
       - Multi-period comparison               /business-dashboard/sales/   /business-dashboard/customers/  /business-dashboard/operations/
       - Management Exception Flags            - Invoiced vs Net Sales      - RFM Segmentation (5 Cohorts)  - Dispatched Parcels & SLA
       - Drill-down routing                    - Top 10 SKUs & Categories   - High CLV Leaderboard          - Store & DC Inventory
                                               - Regional Store Leaderboard - Repeat Buyer Retention        - Factory Output & Defect Rates
                                                                                                                         │
                                                               ┌─────────────────────────────────────────────────────────┴──────────┐
                                                               │                                                                    │
                                                 /business-dashboard/cross-functional/                             /business-dashboard/simulator/
                                                 - Delivery SLA vs Review Rating                                   - Interactive Contribution Margin
                                                 - Return Cost Impact by Reason                                    - Sliders: Volume, Price, Returns, Costs
                                                 - Factory Output vs Real Demand                                   - Instant What-If Impact & Chart Delta
                                                 - Perfect Order Rate & Revenue at Risk
```

| Route | Dashboard Area | Target Audience | Primary Analytical Value |
|---|---|---|---|
| `/executive-summary/` | Area 1: Executive Summary | C-Suite, Board, VPs | Headline KPIs, period trends, exception monitoring, immediate drill-downs |
| `/business-dashboard/sales/` | Area 2: Sales Domain | CRO, Commercial Directors | Channel performance, SKU velocity, category revenue, store rankings |
| `/business-dashboard/customers/` | Area 2: Customer Domain | CMO, Retention Leads | RFM cohorts, customer lifetime value (CLV), churn risk, ratings |
| `/business-dashboard/operations/` | Area 2: Operations Domain | COO, Supply Chain Heads | Carrier delivery SLA, warehouse inventory, factory quality, store productivity |
| `/business-dashboard/cross-functional/` | Area 2: Cross-Functional | Enterprise Strategy | Carrier transit time vs reviews, returns root cause, production-sales gap |
| `/business-dashboard/simulator/` | Area 2: Scenario Tool | Finance & Strategy | Interactive what-if simulation on contribution margin and sensitivity |
| `/health/` | System Monitoring | DevOps, SRE | Database connectivity and response health probe |

---

## 🎨 Corporate Design System

The application adheres strictly to dark corporate tokens crafted for analytical clarity and reduced visual fatigue:

* **Navy Dark (Surface/Body)**: `#0F1F33`
* **Navy Card (Container Background)**: `#183A5F`
* **Blue Border (Card Dividers & Outlines)**: `#24598A`
* **Pure White (Headings & Values)**: `#FFFFFF`
* **Light Text (Labels & Tables)**: `#D5DCE5`
* **Muted Text (Subtitles & Secondary Stats)**: `#94A3B8`
* **Accent Purple (Financial & Primary)**: `#A459D0`
* **Accent Pink (Growth & Highlights)**: `#E95B9F`
* **Accent Cyan (Operations & Metrics)**: `#2CD4E1`
* **Accent Orange (Alerts & Caution)**: `#E88E3E`
* **Accent Yellow (Ratings & Margins)**: `#FFBD4A`
* **Accent Green (Positive Variance)**: `#10B981`
* **Grid & Subtle Lines**: `#6F8298` (30% opacity)

### Typography & Visualization
* **Headings**: `Outfit` (sans-serif, weights 600, 700, 800)
* **Body & Numerical Data**: `Inter` (sans-serif, tabular figures, weights 400, 500, 600)
* **Visualizations**: **ApexCharts.js** rendered with custom dark palettes, tooltips, responsive grid alignments, and zero-iframe architecture.
* **Currency Formatting**: Standard Indian numbering system (`₹ Cr` for Crores, `₹ L` for Lakhs, `₹` with thousand separators).

---

## ⚡ Technical Architecture & Query Optimization

1. **Pure Django MTV**: No heavy single-page app frameworks, no iframes, no Plotly Dash overhead. Standard Django request-response with clean asynchronous REST APIs for cascading UI controls.
2. **Server-Side Pushdown Computation**: 100% of analytical transformations, rollups, and aggregations are pushed down to PostgreSQL 18. Django executes parameterized raw queries returning structured dictionary results.
3. **Cartesian Product Elimination**: Multi-way table joins are strictly governed. Detail tables (`customers.reviews`, `sales.returns`, `sales.shipments`, `employees.attendance`) are pre-aggregated within isolated Common Table Expressions (CTEs) before joining parent entities, completely eliminating row duplication.
4. **Targeted Covering Indexes**:
   - `idx_orders_delivered_cov` on `sales.orders (order_status, order_date DESC) INCLUDE (net_total, cust_id, store_id)`: Reduces headline sales aggregation from **350ms to 38ms**.
   - `idx_order_items_order_cov` on `sales.order_items (order_id) INCLUDE (prod_id, quantity, net_amount, unit_price)`.
   - Foreign key and date indexes across all 16 schemas.
5. **Slow Query Auditing**: Built-in query logger in `db_service.py` timing every database transaction, logging queries exceeding 250ms for ongoing continuous optimization.

---

## 🗄️ Database Schemas & Data Modeling

The database `accio_retailmart_27` contains 16 schemas, 55 tables, and 2,391,602 records:

```
                               ┌───────────────────────────┐
                               │   CORE DIMENSION SCHEMA   │
                               │  dim_region, dim_category │
                               │  dim_brand, dim_channel   │
                               └─────────────┬─────────────┘
                                             │
      ┌────────────────────┬─────────────────┼─────────────────┬────────────────────┐
      ▼                    ▼                 ▼                 ▼                    ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│    SALES     │   │  CUSTOMERS   │   │  INVENTORY   │   │ MANUFACTURE  │   │   CARRIERS   │
│ orders       │   │ customers    │   │ stock_levels │   │ work_orders  │   │ carriers     │
│ order_items  │   │ reviews      │   │ transactions │   │ bills_of_mat │   │ tracking     │
│ payments     │   │ loyalty      │   │ reorders     │   │ qa_logs      │   │ rate_cards   │
│ shipments    │   │ segments     │   │ warehouses   │   │ factories    │   │ service_sla  │
│ returns      │   │ addresses    │   │ bins         │   │ machines     │   │ vehicles     │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
      │
      └──────► Supporting Context Schemas: finance, hr, payroll, marketing, web_events, audit
```

* **Relational Verification**: 43 foreign key relationship checks executed with **0 orphan rows** detected.
* **Data Quality Verification**: 27/27 automated quality checks passed (100.0% score) across completeness, uniqueness, timeliness, accuracy, and format validity.

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
* **Python**: `3.13.x` (or `>= 3.11`)
* **PostgreSQL**: `18.x` (or `>= 15`) running locally on port 5432
* **Git**

### 2. Clone the Repository
```bash
git clone <repository_url>
cd v3
```

### 3. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate environment (macOS / Linux)
source .venv/bin/activate

# Install required production dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and configure your credentials:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
DEBUG=True
SECRET_KEY=your-secure-django-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
DB_NAME=accio_retailmart_27
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 5. Ingest Database & Apply Analytical Views
If running on a fresh PostgreSQL instance:
```bash
# 1. Setup schema DDL
psql -U postgres -d accio_retailmart_27 -f project_documents/sql/01_setup_schema.sql

# 2. Ingest RetailMart V3 CSV dataset (16 schemas, 55 tables)
python scripts/load_data.py

# 3. Create high-performance analytical indexes
psql -U postgres -d accio_retailmart_27 -f project_documents/sql/02_create_indexes.sql

# 4. Create analytical views and materialized views
psql -U postgres -d accio_retailmart_27 -f project_documents/sql/03_analytical_views.sql
```

### 6. Run Migrations & Create Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
# Or use pre-configured executive user:
# Username: executive
# Password: RetailMart2026!
```

### 7. Collect Static Files & Start Development Server
```bash
python manage.py collectstatic --noinput
python manage.py runserver 8000
```
Open your browser at `http://127.0.0.1:8000/`.

---

## 🧪 Automated Testing & Verification

The application includes an automated test suite verifying database services, query correctness, authentication gates, cascading filter state, and template rendering:

```bash
# Run full automated test suite across all services and views
python -m unittest discover -s dashboard/tests
```

### Test Suite Coverage:
* `test_services.py` (8 Tests):
  * Database query runner & timing harness
  * Filter where-clause builders (dates, regions, stores, categories, tiers)
  * Executive Summary metrics reconciliation
  * Sales Intelligence metrics & category distribution
  * Customer Intelligence & RFM segmentation calculations
  * Operations & Carrier SLA computations
  * Cross-functional transit speed and return reasons
  * Contribution Margin baseline reconciliation
* `test_views.py` (12 Tests):
  * `/health/` health check endpoint
  * `/login/` authentication interface
  * Unauthenticated access redirect protection
  * Authenticated `/executive-summary/` rendering
  * Authenticated `/business-dashboard/sales/` rendering
  * Authenticated `/business-dashboard/customers/` rendering
  * Authenticated `/business-dashboard/operations/` rendering
  * Authenticated `/business-dashboard/cross-functional/` rendering
  * Authenticated `/business-dashboard/simulator/` rendering
  * `/api/stores/` cascading REST endpoint
  * `/api/simulator-baseline/` scenario baseline REST endpoint
  * Filter parameter integration across all 5 dashboard views

---

## 📦 Production Deployment Guide (Render / Cloud PaaS)

1. **Procfile**: Already configured for Gunicorn:
   ```
   web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
   ```
2. **Runtime**: Specified in `runtime.txt` (`python-3.13.2`).
3. **Static Assets**: Handled natively by **WhiteNoise** with gzip/brotli compression (`CompressedManifestStaticFilesStorage`).
4. **Production Security Check**:
   ```bash
   python manage.py check --deploy
   ```
5. **Environment Configuration**: Set `DEBUG=False`, `ALLOWED_HOSTS=<your-app>.onrender.com`, `SECURE_SSL_REDIRECT=True`, and provide production PostgreSQL credentials.

---

## 📚 Complete Project Documentation Index

All phase artifacts, audits, and architectural designs are available in `project_documents/`:

| Document | Path | Description |
|---|---|---|
| **Phase 1 Ingestion Report** | `project_documents/documentation/phase1_reconciliation_report.md` | 55-table exact row count reconciliation (2,391,602 rows) |
| **Phase 1 Key Validation** | `project_documents/documentation/phase1_key_validation_report.md` | 43 foreign key relationship checks (0 orphans) |
| **Data Dictionary** | `project_documents/documentation/data_dictionary.md` | Complete documentation of all 314 columns across 16 schemas |
| **Phase 2 Quality Summary** | `project_documents/documentation/phase2_quality_summary.md` | 5-pillar DQ audit results (27/27 checks passed) |
| **Phase 2 Reconciliation** | `project_documents/documentation/phase2_before_after_reconciliation.md` | Before-and-after cleaning reconciliation audit |
| **KPI Catalogue** | `project_documents/documentation/kpi_catalogue.md` | Formal mathematical definitions and SQL for all 25+ KPIs |
| **EDA Catalogue** | `project_documents/documentation/eda_catalogue.md` | 15 exploratory data analysis query patterns and findings |
| **Unsupported Metric Register** | `project_documents/documentation/unsupported_metric_register.md` | Register of unfeasible metrics (CAC, LTV/CAC, EBITDA) |
| **Data Model Diagram** | `project_documents/documentation/data_model_diagram.md` | Entity-Relationship diagrams and join topology |
| **Approved Queries Word Doc** | `project_documents/documentation/approved_kpi_and_eda_queries.docx` | Compiled MS Word deliverable with SQL queries & business rationale |
| **Jupyter Notebooks** | `project_documents/notebooks/` | 4 analytical notebooks (`01_profiling`, `02_cleaning`, `03_data_quality`, `04_eda_catalogue`) |

---

## 👥 Authors & Governance

* **Platform Solution Architecture**: Senior Business Intelligence Analyst & Django Solution Architect
* **Target Enterprise**: RetailMart V3 Enterprise
* **Horizon Analyzed**: January 1, 2024 to February 26, 2026
* **Database Engine**: PostgreSQL 18.4
* **Web Framework**: Django 6.1 (MTV)
