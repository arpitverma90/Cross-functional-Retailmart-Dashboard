# Sales, Customer & Operations Analytics Platform (RetailMart V3)
## Enterprise BI Engine for Commercial, Customer RFM, Operations, Growth & Governance

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg?logo=github)](https://archanak2810.github.io/sales-customer-operations-analytics/)
[![Python](https://img.shields.io/badge/Python-3.13.2-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.4-336791.svg)](https://www.postgresql.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success.svg)]()

> **🚀 Live Interactive Dashboard**: [https://archanak2810.github.io/sales-customer-operations-analytics/](https://archanak2810.github.io/sales-customer-operations-analytics/)  
> **💻 Local Full-Stack Server**: `http://127.0.0.1:8000/` (Django 5.1 + PostgreSQL 18 with 2.4M rows)

A high-performance, modular, and secure Enterprise Business Intelligence application built with **Django 5.1** and powered by **PostgreSQL 18** (`accio_retailmart_27`). This platform visualizes and analyzes over **2.4 million rows** across **55 relational tables** within **16 distinct database schemas**, structured into 3 distinct operational domain suites.

---

## 🌐 Deployment Links & Architecture Appropriateness

| Environment | URL / Endpoint | Target Engine | Purpose & Capabilities |
| :--- | :--- | :--- | :--- |
| **Live Interactive Web App (Production)** | [Launch Live Dashboard](https://archanak2810.github.io/sales-customer-operations-analytics/) | **GitHub Pages** (HTML5 + ApexCharts.js + Pre-computed PostgreSQL Data) | **Zero-setup client-side BI suite** featuring the full dark corporate navy theme (`#0F1F33` / `#183A5F`), left-hand **Global Filter tabs** (Quick Presets, Date Horizons, Geographic Scope, Cost Center), all 3 Domain Suites, interactive ApexCharts, scenario simulator, and one-click downloads of all PDF/Word/HTML domain deliverables. |
| **Local Full-Stack Enterprise Server** | `http://127.0.0.1:8000/` | **Django 5.1 MTV + PostgreSQL 18** (`accio_retailmart_27`) | **Full relational dynamic query engine**. Executes pushdown SQL aggregation queries, window functions, and live schema inspections directly against the 2.4 million row database across 16 schemas. |

### Why This Deployment Link Is Appropriate
1. **Instant Accessibility**: GitHub Pages provides 99.99% uptime, zero cold starts, and immediate public access for stakeholders, executives, and evaluators to interact with the full analytics dashboard without installing local database dependencies.
2. **True Interactive Experience**: The live deployment is not a static screenshot; it is a fully functional web application with interactive tab routing across all 3 domain suites, responsive ApexCharts data tooltips, and a dynamic sensitivity scenario calculator.
3. **Integrated Deliverable Distribution**: All 9 enterprise deliverables (.pdf, .docx, .html) and master SQL catalogs are directly downloadable from the live navigation bar.
4. **Complementary Local Full-Stack**: For data engineers and backend developers, the complete Django 5.1 codebase is included in this repository to run the dynamic server locally against live PostgreSQL.

---

## 🏛️ Enterprise Domain Suites & Architecture

RetailMart V3 organizes enterprise intelligence into three distinct, dedicated domain suites:

```text
                           ┌────────────────────────────────────────────────────────┐
                           │   Sales, Customer & Operations Analytics (RetailMart)   │
                           └──────────────────────────┬─────────────────────────────┘
                                                      │
         ┌────────────────────────────────────────────┼────────────────────────────────────────────┐
         ▼                                            ▼                                            ▼
┌─────────────────────────────────┐        ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│ Suite 1: Growth & Supply Chain  │        │ Suite 2: Commercial & Customers  │        │ Suite 3: People & Governance     │
├─────────────────────────────────┤        ├──────────────────────────────────┤        ├──────────────────────────────────┤
│ • Marketing Intelligence        │        │ • Commercial Sales Performance   │        │ • Human Resources Workforce      │
│   (/marketing/)                 │        │   (/sales/)                      │        │   (/hr/)                         │
│ • Digital Journey & Clickstream │        │ • Customer RFM & Retention       │        │ • Financial Ledger & Treasury    │
│   (/digital/)                   │        │   (/customers/)                  │        │   (/finance/)                    │
│ • Logistics & Carrier SLAs      │        │ • Store Inventory & Factory QA   │        │                                  │
│   (/logistics/)                 │        │   (/operations/)                 │        │                                  │
└─────────────────────────────────┘        └──────────────────────────────────┘        └──────────────────────────────────┘
```

---

## 📊 Core Performance Metrics by Domain

### Suite 1: Growth & Supply Chain
* **Marketing Campaigns**: 250 initiatives, ₹13.11 Cr authorized budget, ₹1.03 Cr realized spend (7.86% budget pacing).
* **Multi-Platform Ad Allocation**: Google Ads (33.1%), Facebook / Meta (27.6%), Instagram (18.4%), LinkedIn (12.1%), Twitter (8.8%).
* **Email CRM Engagement**: 12.95M outbound emails, 3.91M opened (30.17% open rate), 895K clicked (22.92% CTR).
* **Digital Traffic Scale**: 500,000 page views across 99,320 sessions (5.03 pages/session) with 59.91% mobile device share.
* **Outbound Logistics & Carrier SLAs**: 104,987 outbound parcels, 82,540 successfully delivered, 79.80% on-time delivery (OTD) against &le;5-day SLA, 4.00 days mean transit lead time.
* **Regional Warehousing**: 5 Central Distribution Centers comprising 830,000 sq ft capacity.

### Suite 2: Commercial & Customer Operations
* **Delivered Commercial Sales**: **₹676.95 Cr** net revenue across **82,540 fulfilled orders** with **₹82,015.22 Average Order Value (AOV)**.
* **Gross Revenue & Markdowns**: ₹701.23 Cr gross catalog value with ₹24.27 Cr absorbed promotional discounts (3.46% markdown rate).
* **Category Economics**: Electronics (₹284.15 Cr, 27% margin), Fashion & Apparel (₹148.90 Cr, 35% margin), Home & Kitchen (₹115.40 Cr, 30% margin), Grocery & Staples (₹82.50 Cr, 18% margin).
* **Customer Base Penetration**: 50,000 registered master accounts, 40,380 transacting buyers (80.8% buyer penetration).
* **Behavioral RFM Segmentation**: 8,885 Champions (₹234.80 Cr spend), 11,240 Loyal Customers, 6,518 At-Risk accounts.
* **Store Inventory Health**: 114,153 active store shelf slots, 595 zero-stock stockouts (0.52% OOS rate), 16,880 low-stock reorder triggers.
* **Manufacturing Plant Quality**: 15,000 completed work orders, 25.19M units produced, 640,075 rejected defect units (2.54% factory scrap rate across 10 production lines).

### Suite 3: People & Financial Governance
* **Active Workforce Headcount**: 3,000 employees across 10 functional departments.
* **Compensation & Payroll**: ₹18.98 Cr monthly contractual base payroll, ₹63,267 average salary (median: ₹55,000).
* **Store Operating Expenditure**: ₹38.80 Cr store OPEX (branch leases, utilities, staffing).
* **Corporate Operating Expenditure**: ₹42.15 Cr corporate OPEX (HQ technology, administrative, marketing).
* **Treasury Settlement Rails**: UPI (₹312.40 Cr, zero MDR, 1.2% dispute rate), Credit/Debit Cards (₹241.10 Cr), Net Banking (₹92.50 Cr), COD (₹55.23 Cr).

---

## 🧭 Application Route Register

| Route | Domain Suite | Primary Analytical Function |
| :--- | :--- | :--- |
| `/marketing/` | Suite 1: Growth & Supply Chain | Paid platform ad spend, campaign budget pacing, email engagement |
| `/digital/` | Suite 1: Growth & Supply Chain | Clickstream sessions, device/OS distribution, conversion funnel |
| `/logistics/` | Suite 1: Growth & Supply Chain | Courier on-time SLA benchmarking, transit lead times, warehouse footprint |
| `/sales/` | Suite 2: Commercial & Customer | Net revenue velocity, category margins, brand & store league tables |
| `/customers/` | Suite 2: Commercial & Customer | RFM segmentation, loyalty tier spending, repeat purchase cohorts |
| `/operations/` | Suite 2: Commercial & Customer | Store stock health matrix, regional stockout vulnerability, scrap rates |
| `/hr/` | Suite 3: People & Governance | Departmental headcount, payroll distribution, shift compliance |
| `/finance/` | Suite 3: People & Governance | Revenue vs OPEX waterfall, corporate/store expense ledgers, treasury |
| `/executive-summary/` | Executive Synthesis | Cross-domain KPI scorecard and high-level enterprise summary |
| `/simulator/` | Strategic Planning | Real-time sensitivity simulation (pricing, returns, OPEX, headcount) |

---

## 📦 Dedicated Domain Deliverables

Comprehensive deliverables in **PDF, Word (.docx), and HTML** are generated directly from verified PostgreSQL data:

1. **Domain Suite 1 Deliverables (Marketing, Digital & Logistics)**:
   - PDF: `project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf`
   - Word: `project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.docx`
   - HTML: `project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.html`
2. **Domain Suite 2 Deliverables (Sales, Customer & Operations)**:
   - PDF: `project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf`
   - Word: `project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.docx`
   - HTML: `project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.html`
3. **Domain Suite 3 Deliverables (HR & Finance)**:
   - PDF: `project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.pdf`
   - Word: `project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.docx`
   - HTML: `project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.html`
4. **Master Technical Documents**:
   - Master SQL Catalogue (.docx): `project_documents/documentation/RetailMart_V3_Master_KPI_and_EDA_SQL_Queries.docx`
   - Executive Insights Report (.pdf, .docx, .html): `project_documents/documentation/RetailMart_V3_Executive_Insights_Report.*`

---

## ⚡ Technical Architecture & Engineering Standards

1. **Django MTV Framework**: Clean modular separation of concerns with views, services, and templates.
2. **PostgreSQL Server-Side Pushdown Computation**: 100% of analytical transformations, window functions, and aggregations run inside PostgreSQL.
3. **Targeted Database Indexes**: Covering indexes on `sales.orders`, `sales.order_items`, `sales.shipments`, `web_events.page_views`, and `products.inventory`.
4. **Interactive Visualization**: ApexCharts-powered responsive charts with dynamic theme switching and dark mode contrast standards.

---

## 🚀 Quickstart & Local Installation

### 1. Prerequisites
* Python 3.11+ or 3.13+
* PostgreSQL 15+ or 18+ running on port 5432 with `accio_retailmart_27`

### 2. Environment Setup
```bash
cp .env.example .env
# Update .env with your PostgreSQL credentials
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Navigate to `http://127.0.0.1:8000/` and sign in with `admin` / `admin123`.
