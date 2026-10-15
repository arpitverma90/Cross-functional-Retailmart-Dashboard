"""
Builds the standalone, client-side interactive HTML dashboard for GitHub Pages (index.html).
Renders all 3 Domain Suites (Marketing, Digital, Logistics; Sales, Customer, Operations; HR, Finance)
along with Executive Summary, Scenario Simulator, ApexCharts visualizations, and direct deliverable download links.
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GITHUB_DIR = os.path.join(BASE_DIR, 'retailmart_bi_github')
INDEX_FILE = os.path.join(GITHUB_DIR, 'index.html')

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RetailMart V3 · Enterprise Analytics &amp; Domain Suites</title>
    
    <!-- Fonts: Outfit (Headings) & Inter (Data & Body) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Tabler Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.31.0/dist/tabler-icons.min.css">
    
    <!-- ApexCharts.js -->
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>

    <style>
        :root {
            --navy-dark: #0A1128;
            --navy-surface: #0F172A;
            --navy-card: #1E293B;
            --navy-card-hover: #24344D;
            --border-card: #2D3D5A;
            --blue-border: #1E3A5F;
            --text-white: #F8FAFC;
            --text-light: #CBD5E1;
            --text-muted: #94A3B8;
            --cyan: #2CD4E1;
            --purple: #8B5CF6;
            --pink: #EC4899;
            --orange: #F97316;
            --yellow: #FBBF24;
            --emerald: #10B981;
            --rose: #F43F5E;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--navy-dark);
            color: var(--text-light);
            line-height: 1.5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Top Navigation Header */
        .top-navbar {
            background-color: var(--navy-surface);
            border-bottom: 1px solid var(--border-card);
            padding: 0.75rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 1000;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .brand-wrapper {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 8px;
            background: linear-gradient(135deg, #1E3A8A 0%, var(--purple) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            color: #fff;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        }

        .brand-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-white);
            line-height: 1.2;
        }

        .brand-sub {
            font-size: 0.7rem;
            color: var(--cyan);
            font-weight: 500;
        }

        /* Nav Tabs & Suites */
        .nav-tabs {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background-color: rgba(15, 23, 42, 0.7);
            padding: 0.25rem 0.5rem;
            border-radius: 9999px;
            border: 1px solid var(--blue-border);
            overflow-x: auto;
        }

        .suite-pill {
            display: flex;
            align-items: center;
            border-radius: 9999px;
            padding: 2px 4px;
            gap: 2px;
        }
        .suite-1 { background: rgba(14, 165, 233, 0.12); border: 1px solid rgba(14, 165, 233, 0.35); }
        .suite-2 { background: rgba(168, 85, 247, 0.12); border: 1px solid rgba(168, 85, 247, 0.35); }
        .suite-3 { background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); }

        .suite-tag {
            font-size: 0.62rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 0 5px;
            letter-spacing: 0.5px;
        }
        .tag-1 { color: #38BDF8; }
        .tag-2 { color: #C084FC; }
        .tag-3 { color: #34D399; }

        .nav-tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 0.35rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 600;
            border-radius: 9999px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .nav-tab-btn:hover {
            color: var(--text-white);
            background: rgba(255, 255, 255, 0.08);
        }

        .nav-tab-btn.active {
            background: var(--purple);
            color: #fff;
            box-shadow: 0 2px 8px rgba(139, 92, 246, 0.5);
        }

        .nav-tab-btn.active-s1 {
            background: #0284C7;
            color: #fff;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.5);
        }

        .nav-tab-btn.active-s2 {
            background: #7C3AED;
            color: #fff;
            box-shadow: 0 2px 8px rgba(124, 58, 237, 0.5);
        }

        .nav-tab-btn.active-s3 {
            background: #059669;
            color: #fff;
            box-shadow: 0 2px 8px rgba(5, 150, 105, 0.5);
        }

        /* Top Action Buttons */
        .header-actions {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .btn-dropdown {
            background: rgba(37, 99, 235, 0.25);
            border: 1px solid rgba(37, 99, 235, 0.6);
            color: #93C5FD;
            padding: 0.4rem 0.85rem;
            font-size: 0.75rem;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            position: relative;
        }

        .dropdown-menu {
            display: none;
            position: absolute;
            right: 0;
            top: calc(100% + 6px);
            width: 320px;
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 8px;
            box-shadow: 0 16px 36px rgba(0,0,0,0.7);
            z-index: 2000;
            padding: 6px 0;
            text-align: left;
        }

        .dropdown-header {
            padding: 6px 12px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid #334155;
        }

        .dropdown-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            padding: 4px 8px;
            gap: 4px;
            border-bottom: 1px solid #334155;
        }

        .dropdown-btn-link {
            padding: 4px 6px;
            font-size: 0.68rem;
            text-decoration: none;
            text-align: center;
            border-radius: 4px;
            display: inline-block;
            font-weight: 600;
        }
        .link-pdf { background: rgba(244,63,94,0.15); color: #FDA4AF; border: 1px solid rgba(244,63,94,0.3); }
        .link-doc { background: rgba(59,130,246,0.15); color: #93C5FD; border: 1px solid rgba(59,130,246,0.3); }
        .link-html { background: rgba(13,148,136,0.15); color: #5EEAD4; border: 1px solid rgba(13,148,136,0.3); }

        /* Main Container */
        .main-container {
            max-width: 1440px;
            margin: 0 auto;
            padding: 1.5rem;
            flex: 1;
            width: 100%;
        }

        .dashboard-tab-content {
            display: none;
            animation: fadeIn 0.25s ease-in-out;
        }
        .dashboard-tab-content.active { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Page Header */
        .page-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-card);
            padding-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .page-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-white);
        }

        .page-desc {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }

        /* KPI Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .kpi-card {
            background-color: var(--navy-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            padding: 1.1rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
        }
        .border-cyan::before { background: var(--cyan); }
        .border-purple::before { background: var(--purple); }
        .border-orange::before { background: var(--orange); }
        .border-pink::before { background: var(--pink); }
        .border-yellow::before { background: var(--yellow); }
        .border-emerald::before { background: var(--emerald); }

        .kpi-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }

        .kpi-label {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
        }

        .kpi-value {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--text-white);
            margin-bottom: 0.25rem;
        }

        .kpi-sub {
            font-size: 0.72rem;
            color: var(--text-muted);
        }

        /* Charts Grid */
        .charts-grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.5rem;
        }

        .chart-card {
            background-color: var(--navy-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            padding: 1.25rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .chart-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .chart-title {
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-white);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Tables */
        .table-card {
            background-color: var(--navy-card);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            margin-bottom: 1.5rem;
        }

        .table-header {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border-card);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .table-title {
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-white);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .table-wrapper {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.78rem;
            text-align: left;
        }

        th {
            background-color: rgba(15, 23, 42, 0.6);
            color: var(--text-muted);
            padding: 0.75rem 1rem;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--border-card);
        }

        td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(45, 61, 90, 0.4);
            color: var(--text-light);
        }

        tr:hover td {
            background-color: rgba(255, 255, 255, 0.02);
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 600;
        }
        .badge-success { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-warning { background: rgba(245, 158, 11, 0.15); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-danger { background: rgba(244, 63, 94, 0.15); color: #FDA4AF; border: 1px solid rgba(244, 63, 94, 0.3); }
        .badge-neutral { background: rgba(148, 163, 184, 0.15); color: #CBD5E1; border: 1px solid rgba(148, 163, 184, 0.3); }

        /* Simulator Controls */
        .slider-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.5rem;
        }

        .slider-group {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--border-card);
            border-radius: 8px;
            padding: 1rem;
        }

        .slider-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-white);
            margin-bottom: 0.5rem;
        }

        input[type=range] {
            width: 100%;
            height: 6px;
            background: #2D3D5A;
            border-radius: 4px;
            outline: none;
            cursor: pointer;
        }

        /* Footer */
        footer {
            background-color: var(--navy-surface);
            border-top: 1px solid var(--border-card);
            padding: 1.5rem;
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: auto;
        }
    </style>
</head>
<body>

    <!-- Top Corporate Navigation -->
    <header class="top-navbar">
        <div class="brand-wrapper">
            <div class="brand-icon">
                <i class="ti ti-chart-dots"></i>
            </div>
            <div>
                <div class="brand-title">RetailMart <span style="color: var(--purple);">V3</span></div>
                <div class="brand-sub"><i class="ti ti-circle-filled" style="font-size: 0.5rem; color: #10B981;"></i> Live Online · GitHub Pages Deployment</div>
            </div>
        </div>

        <!-- Distinct Domain Suites Navigation -->
        <nav class="nav-tabs">
            <!-- Global Overview -->
            <button class="nav-tab-btn active" onclick="switchTab('executive')">
                <i class="ti ti-layout-dashboard"></i> Executive
            </button>

            <!-- Suite 1: Growth & Supply Chain -->
            <div class="suite-pill suite-1">
                <span class="suite-tag tag-1">Suite 1</span>
                <button class="nav-tab-btn" onclick="switchTab('marketing')"><i class="ti ti-target"></i> Marketing</button>
                <button class="nav-tab-btn" onclick="switchTab('digital')"><i class="ti ti-device-analytics"></i> Digital</button>
                <button class="nav-tab-btn" onclick="switchTab('logistics')"><i class="ti ti-truck-delivery"></i> Logistics</button>
            </div>

            <!-- Suite 2: Commercial & Customers -->
            <div class="suite-pill suite-2">
                <span class="suite-tag tag-2">Suite 2</span>
                <button class="nav-tab-btn" onclick="switchTab('sales')"><i class="ti ti-shopping-cart"></i> Sales</button>
                <button class="nav-tab-btn" onclick="switchTab('customers')"><i class="ti ti-user-check"></i> Customer</button>
                <button class="nav-tab-btn" onclick="switchTab('operations')"><i class="ti ti-boxes"></i> Operations</button>
            </div>

            <!-- Suite 3: People & Governance -->
            <div class="suite-pill suite-3">
                <span class="suite-tag tag-3">Suite 3</span>
                <button class="nav-tab-btn" onclick="switchTab('hr')"><i class="ti ti-users"></i> HR</button>
                <button class="nav-tab-btn" onclick="switchTab('finance')"><i class="ti ti-chart-line"></i> Finance</button>
            </div>

            <!-- Tools -->
            <button class="nav-tab-btn" onclick="switchTab('simulator')">
                <i class="ti ti-calculator"></i> Simulator
            </button>
        </nav>

        <!-- Domain Deliverables Dropdown -->
        <div class="header-actions">
            <div style="position: relative;">
                <button id="dropbtn" class="btn-dropdown" onclick="toggleDropdown()">
                    <i class="ti ti-download"></i> Domain Deliverables <i class="ti ti-chevron-down" style="font-size: 0.65rem;"></i>
                </button>
                
                <div id="dropmenu" class="dropdown-menu">
                    <!-- Suite 1 -->
                    <div class="dropdown-header" style="color: #38BDF8; background: rgba(56, 189, 248, 0.08);">
                        Suite 1: Marketing, Digital &amp; Logistics
                    </div>
                    <div class="dropdown-grid">
                        <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="dropdown-btn-link link-pdf"><i class="ti ti-file-type-pdf"></i> PDF</a>
                        <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.docx" download class="dropdown-btn-link link-doc"><i class="ti ti-file-type-docx"></i> Word</a>
                        <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.html" target="_blank" class="dropdown-btn-link link-html"><i class="ti ti-file-type-html"></i> HTML</a>
                    </div>

                    <!-- Suite 2 -->
                    <div class="dropdown-header" style="color: #C084FC; background: rgba(192, 132, 252, 0.08);">
                        Suite 2: Sales, Customer &amp; Operations
                    </div>
                    <div class="dropdown-grid">
                        <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="dropdown-btn-link link-pdf"><i class="ti ti-file-type-pdf"></i> PDF</a>
                        <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.docx" download class="dropdown-btn-link link-doc"><i class="ti ti-file-type-docx"></i> Word</a>
                        <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.html" target="_blank" class="dropdown-btn-link link-html"><i class="ti ti-file-type-html"></i> HTML</a>
                    </div>

                    <!-- Suite 3 -->
                    <div class="dropdown-header" style="color: #34D399; background: rgba(52, 211, 153, 0.08);">
                        Suite 3: HR &amp; Financial Governance
                    </div>
                    <div class="dropdown-grid">
                        <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.pdf" target="_blank" class="dropdown-btn-link link-pdf"><i class="ti ti-file-type-pdf"></i> PDF</a>
                        <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.docx" download class="dropdown-btn-link link-doc"><i class="ti ti-file-type-docx"></i> Word</a>
                        <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.html" target="_blank" class="dropdown-btn-link link-html"><i class="ti ti-file-type-html"></i> HTML</a>
                    </div>

                    <!-- Master Documents -->
                    <div class="dropdown-header" style="color: #94A3B8;">Master Governance &amp; Codebase</div>
                    <div style="padding: 6px 12px; display: flex; flex-direction: column; gap: 4px;">
                        <a href="./project_documents/documentation/RetailMart_V3_Master_KPI_and_EDA_SQL_Queries.docx" download style="color: #F8FAFC; text-decoration: none; font-size: 0.72rem; display: flex; align-items: center; gap: 6px; padding: 4px 0;">
                            <i class="ti ti-database" style="color: #A855F7;"></i> Master SQL Queries (.docx)
                        </a>
                        <a href="./project_documents/documentation/RetailMart_V3_Executive_Insights_Report.pdf" target="_blank" style="color: #F8FAFC; text-decoration: none; font-size: 0.72rem; display: flex; align-items: center; gap: 6px; padding: 4px 0;">
                            <i class="ti ti-file-type-pdf" style="color: #F43F5E;"></i> Executive Insights Report (PDF)
                        </a>
                    </div>
                </div>
            </div>

            <a href="https://github.com/Archanak2810/sales-customer-operations-analytics" target="_blank" style="color: var(--text-white); background: rgba(255,255,255,0.08); padding: 0.4rem 0.75rem; border-radius: 6px; font-size: 0.75rem; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.35rem;">
                <i class="ti ti-brand-github"></i> Repository
            </a>
        </div>
    </header>

    <!-- Main Dashboard Container -->
    <main class="main-container">

        <!-- ==================================================================== -->
        <!-- TAB 0: EXECUTIVE SUMMARY -->
        <!-- ==================================================================== -->
        <section id="tab-executive" class="dashboard-tab-content active">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Executive Performance &amp; Cross-Domain Synthesis</h2>
                    <div class="page-desc">High-level enterprise indicators across Revenue, Workforce, Operations, and Media Efficiency</div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <span class="status-badge badge-success"><i class="ti ti-check"></i> PostgreSQL 18 Pushdown Active</span>
                    <a href="./project_documents/documentation/RetailMart_V3_Executive_Insights_Report.pdf" target="_blank" class="status-badge badge-neutral" style="text-decoration: none;"><i class="ti ti-file-type-pdf"></i> Executive Dossier</a>
                </div>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-purple">
                    <div class="kpi-header"><span class="kpi-label">Delivered Net Revenue</span><i class="ti ti-currency-rupee" style="color: var(--purple);"></i></div>
                    <div class="kpi-value">₹676.95 Cr</div>
                    <div class="kpi-sub">82,540 Delivered Orders (₹82,015 AOV)</div>
                </div>
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Active Transacting Base</span><i class="ti ti-users" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">40,380</div>
                    <div class="kpi-sub">80.8% Penetration of 50,000 Master CRM</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Carrier On-Time SLA</span><i class="ti ti-clock-check" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">79.80%</div>
                    <div class="kpi-sub">&le; 5 Days Target (4.00d Avg Lead Time)</div>
                </div>
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Marketing Ad Spend</span><i class="ti ti-speakerphone" style="color: var(--orange);"></i></div>
                    <div class="kpi-value">₹1.03 Cr</div>
                    <div class="kpi-sub">7.86% Utilization of ₹13.11 Cr Budget</div>
                </div>
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Active Workforce</span><i class="ti ti-id-badge-2" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">3,000 Staff</div>
                    <div class="kpi-sub">Across 10 Departments (₹18.98 Cr Monthly Payroll)</div>
                </div>
                <div class="kpi-card border-yellow">
                    <div class="kpi-header"><span class="kpi-label">Quality Scrap Rate</span><i class="ti ti-tool" style="color: var(--yellow);"></i></div>
                    <div class="kpi-value">2.54%</div>
                    <div class="kpi-sub">15,000 Batches (640,075 Defect Units)</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-chart-line" style="color: var(--cyan);"></i> Enterprise Revenue Velocity vs. Operating Spend Trajectory</div></div>
                    <div id="chart-exec-rev"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-pie" style="color: var(--purple);"></i> Product Category Net Sales Mix &amp; Realized Gross Margins</div></div>
                    <div id="chart-exec-cat"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 1: MARKETING (SUITE 1) -->
        <!-- ==================================================================== -->
        <section id="tab-marketing" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Marketing Intelligence Dashboard (Suite 1)</h2>
                    <div class="page-desc">Paid Advertising Platforms, Campaign Pacing &amp; Customer Email CRM Engagement</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 1 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Total Realized Spend</span><i class="ti ti-currency-rupee" style="color: var(--orange);"></i></div>
                    <div class="kpi-value">₹1.03 Cr</div>
                    <div class="kpi-sub">₹10,302,874 across 5 paid networks</div>
                </div>
                <div class="kpi-card border-purple">
                    <div class="kpi-header"><span class="kpi-label">Authorized Budget</span><i class="ti ti-wallet" style="color: var(--purple);"></i></div>
                    <div class="kpi-value">₹13.11 Cr</div>
                    <div class="kpi-sub">250 Total Marketing Initiatives</div>
                </div>
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Budget Utilization</span><i class="ti ti-chart-pie" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">7.86%</div>
                    <div class="kpi-sub">Ad spend pacing vs budget cap</div>
                </div>
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Emails Dispatched</span><i class="ti ti-mail" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">12.95M</div>
                    <div class="kpi-sub">3,907,091 Opened (30.17% Open Rate)</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Click-Through Rate (CTR)</span><i class="ti ti-cursor-text" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">22.92%</div>
                    <div class="kpi-sub">895,617 Total Clicks on Opened Mail</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-brand-facebook" style="color: var(--pink);"></i> Ad Spend Allocation by Platform</div></div>
                    <div id="chart-mktg-platform"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-chart-bar" style="color: var(--cyan);"></i> Monthly Spend Velocity (₹ Lakhs)</div></div>
                    <div id="chart-mktg-monthly"></div>
                </div>
            </div>

            <div class="table-card">
                <div class="table-header"><div class="table-title"><i class="ti ti-list-details" style="color: var(--cyan);"></i> Top 5 Strategic Marketing Campaigns</div></div>
                <div class="table-wrapper">
                    <table>
                        <thead><tr><th>Campaign</th><th>Start Date</th><th>End Date</th><th>Budget (₹)</th><th>Realized Spend (₹)</th><th>Pacing</th><th>Status</th></tr></thead>
                        <tbody>
                            <tr><td><strong>Diwali Mega Sale Extravaganza</strong></td><td>2024-10-01</td><td>2024-11-15</td><td>₹1,500,000</td><td style="color: var(--orange); font-weight: 600;">₹1,420,500</td><td><span class="status-badge badge-success">94.7%</span></td><td><span class="status-badge badge-neutral">Completed</span></td></tr>
                            <tr><td><strong>New Year Fresh Start 2025</strong></td><td>2024-12-20</td><td>2025-01-10</td><td>₹1,200,000</td><td style="color: var(--orange); font-weight: 600;">₹1,180,000</td><td><span class="status-badge badge-success">98.3%</span></td><td><span class="status-badge badge-neutral">Completed</span></td></tr>
                            <tr><td><strong>Monsoon Clearance Blowout</strong></td><td>2025-07-01</td><td>2025-08-15</td><td>₹900,000</td><td style="color: var(--orange); font-weight: 600;">₹845,200</td><td><span class="status-badge badge-success">93.9%</span></td><td><span class="status-badge badge-neutral">Completed</span></td></tr>
                            <tr><td><strong>Back to School Tech Deals</strong></td><td>2025-05-15</td><td>2025-06-30</td><td>₹850,000</td><td style="color: var(--orange); font-weight: 600;">₹810,000</td><td><span class="status-badge badge-success">95.3%</span></td><td><span class="status-badge badge-neutral">Completed</span></td></tr>
                            <tr><td><strong>Independence Week Specials</strong></td><td>2025-08-08</td><td>2025-08-18</td><td>₹750,000</td><td style="color: var(--orange); font-weight: 600;">₹720,000</td><td><span class="status-badge badge-success">96.0%</span></td><td><span class="status-badge badge-neutral">Completed</span></td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 2: DIGITAL (SUITE 1) -->
        <!-- ==================================================================== -->
        <section id="tab-digital" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Digital Experience &amp; Journey Dashboard (Suite 1)</h2>
                    <div class="page-desc">Web Traffic Scale, Session Dynamics, Device Ecosystem &amp; Clickstream Interaction Funnels</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 1 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Total Web Sessions</span><i class="ti ti-device-analytics" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">99,320</div>
                    <div class="kpi-sub">Unique browsing visitor journeys</div>
                </div>
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Aggregated Page Views</span><i class="ti ti-browser" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">500,000</div>
                    <div class="kpi-sub">5.03 Pages per Browsing Session</div>
                </div>
                <div class="kpi-card border-purple">
                    <div class="kpi-header"><span class="kpi-label">Identified Customer Visitors</span><i class="ti ti-user-check" style="color: var(--purple);"></i></div>
                    <div class="kpi-value">49,949</div>
                    <div class="kpi-sub">Transacting &amp; authenticated users</div>
                </div>
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Mobile Traffic Share</span><i class="ti ti-device-mobile" style="color: var(--orange);"></i></div>
                    <div class="kpi-value">59.91%</div>
                    <div class="kpi-sub">Mobile web &amp; smartphone dominance</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Total Interaction Events</span><i class="ti ti-click" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">200,000</div>
                    <div class="kpi-sub">49,990 Clicks | 49,840 Form Submits</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-devices" style="color: var(--cyan);"></i> Device Ecosystem Share (%)</div></div>
                    <div id="chart-digital-devices"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-filter" style="color: var(--purple);"></i> E-Commerce Web Funnel Progression</div></div>
                    <div id="chart-digital-funnel"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 3: LOGISTICS (SUITE 1) -->
        <!-- ==================================================================== -->
        <section id="tab-logistics" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Logistics &amp; Supply Chain Dashboard (Suite 1)</h2>
                    <div class="page-desc">Order Fulfillment, Courier Partner On-Time SLA, Transit Lead Times &amp; Distribution Warehousing</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 1 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Total Outbound Shipments</span><i class="ti ti-package" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">104,987</div>
                    <div class="kpi-sub">82,540 Delivered (78.6%)</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Carrier On-Time SLA</span><i class="ti ti-clock-check" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">79.80%</div>
                    <div class="kpi-sub">&le; 5 Days Dispatch-to-Door Delivery Target</div>
                </div>
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Avg Delivery Lead Time</span><i class="ti ti-calendar-event" style="color: var(--orange);"></i></div>
                    <div class="kpi-value">4.00 Days</div>
                    <div class="kpi-sub">Courier fulfillment cycle speed</div>
                </div>
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Active In-Transit Pipeline</span><i class="ti ti-truck-delivery" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">14,982</div>
                    <div class="kpi-sub">Parcels currently in transport</div>
                </div>
                <div class="kpi-card border-yellow">
                    <div class="kpi-header"><span class="kpi-label">Central Warehouses Footprint</span><i class="ti ti-building-warehouse" style="color: var(--yellow);"></i></div>
                    <div class="kpi-value">830,000 Sq Ft</div>
                    <div class="kpi-sub">Across 5 Central Regional Distribution Centers</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-truck" style="color: var(--cyan);"></i> Courier Partner On-Time SLA Comparison (%)</div></div>
                    <div id="chart-logistics-courier"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-hourglass" style="color: var(--emerald);"></i> Delivery Lead Time Distribution (Days)</div></div>
                    <div id="chart-logistics-leadtime"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 4: SALES (SUITE 2) -->
        <!-- ==================================================================== -->
        <section id="tab-sales" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Commercial Sales &amp; Revenue Intelligence (Suite 2)</h2>
                    <div class="page-desc">Revenue Velocity, Gross Margins, Category Pareto Contribution &amp; Branch Store Outlets</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 2 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-purple">
                    <div class="kpi-header"><span class="kpi-label">Delivered Net Revenue</span><i class="ti ti-currency-rupee" style="color: var(--purple);"></i></div>
                    <div class="kpi-value">₹676.95 Cr</div>
                    <div class="kpi-sub">₹6,769,536,004.48 net sales</div>
                </div>
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Fulfilled Orders</span><i class="ti ti-shopping-bag" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">82,540</div>
                    <div class="kpi-sub">100% delivered customer orders</div>
                </div>
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Average Order Value (AOV)</span><i class="ti ti-basket" style="color: var(--orange);"></i></div>
                    <div class="kpi-value">₹82,015</div>
                    <div class="kpi-sub">Mean net basket realization</div>
                </div>
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Gross Catalog Value</span><i class="ti ti-receipt" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">₹701.23 Cr</div>
                    <div class="kpi-sub">₹24.27 Cr absorbed promotions (3.46%)</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-chart-line" style="color: var(--cyan);"></i> Monthly Net Sales Velocity (₹ Crores)</div></div>
                    <div id="chart-sales-trend"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-tags" style="color: var(--purple);"></i> Category Gross Margin Economics (%)</div></div>
                    <div id="chart-sales-margins"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 5: CUSTOMER (SUITE 2) -->
        <!-- ==================================================================== -->
        <section id="tab-customers" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Customer RFM Intelligence &amp; Retention (Suite 2)</h2>
                    <div class="page-desc">Behavioral Segmentation (Recency, Frequency, Monetary), Loyalty Tiers &amp; Repeat Purchase Cohorts</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 2 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Active Transacting Buyers</span><i class="ti ti-user-check" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">40,380</div>
                    <div class="kpi-sub">80.8% Penetration of 50,000 Accounts</div>
                </div>
                <div class="kpi-card border-purple">
                    <div class="kpi-header"><span class="kpi-label">Champions RFM Segment</span><i class="ti ti-crown" style="color: var(--purple);"></i></div>
                    <div class="kpi-value">8,885</div>
                    <div class="kpi-sub">₹234.80 Cr Total Spend (14d Recency)</div>
                </div>
                <div class="kpi-card border-yellow">
                    <div class="kpi-header"><span class="kpi-label">At-Risk Segment</span><i class="ti ti-alert-triangle" style="color: var(--yellow);"></i></div>
                    <div class="kpi-value">6,518</div>
                    <div class="kpi-sub">120+ Days Inactivity Churn Risk</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Repeat Buyer Rate</span><i class="ti ti-repeat" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">58.4%</div>
                    <div class="kpi-sub">Multiple completed purchase orders</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-chart-pie" style="color: var(--cyan);"></i> RFM Customer Segment Breakdown</div></div>
                    <div id="chart-cust-rfm"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-medal" style="color: var(--yellow);"></i> Loyalty Tier Spend Velocity (₹ Cr)</div></div>
                    <div id="chart-cust-tiers"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 6: OPERATIONS (SUITE 2) -->
        <!-- ==================================================================== -->
        <section id="tab-operations" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Operations, Inventory &amp; Factory Quality (Suite 2)</h2>
                    <div class="page-desc">Store Shelf Stock Health, Stockout Vulnerability, Manufacturing Work Orders &amp; Scrap Defect Rates</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 2 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Total Inventory Slots</span><i class="ti ti-boxes" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">114,153</div>
                    <div class="kpi-sub">Active SKU &times; store shelf allocations</div>
                </div>
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Out of Stock (OOS)</span><i class="ti ti-alert-circle" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">595 SKUs</div>
                    <div class="kpi-sub">0.52% zero-stock revenue loss exposure</div>
                </div>
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Low Stock (At Reorder)</span><i class="ti ti-clock-pause" style="color: var(--orange);"></i></div>
                    <div class="kpi-value">16,880 SKUs</div>
                    <div class="kpi-sub">Pending replenishment reorders</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Factory Scrap Rate</span><i class="ti ti-tool" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">2.54%</div>
                    <div class="kpi-sub">640,075 Defect Units of 25.19M Produced</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-shield-check" style="color: var(--cyan);"></i> Store Inventory Stock Health Distribution</div></div>
                    <div id="chart-ops-health"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-settings" style="color: var(--pink);"></i> Factory Scrap Rate % Across 10 Production Lines</div></div>
                    <div id="chart-ops-scrap"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 7: HR (SUITE 3) -->
        <!-- ==================================================================== -->
        <section id="tab-hr" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Human Resources &amp; Workforce Intelligence (Suite 3)</h2>
                    <div class="page-desc">Headcount Demographics, Compensation Structure, Attendance Compliance &amp; Store Staffing Ratios</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 3 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Active Headcount</span><i class="ti ti-users" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">3,000 Staff</div>
                    <div class="kpi-sub">100% Active across 10 functional depts</div>
                </div>
                <div class="kpi-card border-purple">
                    <div class="kpi-header"><span class="kpi-label">Monthly Base Payroll</span><i class="ti ti-wallet" style="color: var(--purple);"></i></div>
                    <div class="kpi-value">₹18.98 Cr</div>
                    <div class="kpi-sub">₹189,800,000 contractual payroll</div>
                </div>
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Average Base Salary</span><i class="ti ti-id" style="color: var(--cyan);"></i></div>
                    <div class="kpi-value">₹63,267</div>
                    <div class="kpi-sub">Median: ₹55,000 / month</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Attendance Proxy Compliance</span><i class="ti ti-clock" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">94.8%</div>
                    <div class="kpi-sub">88,310 check-in/check-out logs</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-building" style="color: var(--pink);"></i> Departmental Headcount Distribution</div></div>
                    <div id="chart-hr-dept"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-cash" style="color: var(--cyan);"></i> Average Monthly Compensation by Department (₹)</div></div>
                    <div id="chart-hr-comp"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 8: FINANCE (SUITE 3) -->
        <!-- ==================================================================== -->
        <section id="tab-finance" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Financial Performance &amp; Treasury Ledger (Suite 3)</h2>
                    <div class="page-desc">Operating Expenditure (Corporate &amp; Store OPEX), Treasury Liquidity &amp; Payment Tender Rails</div>
                </div>
                <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="text-decoration: none;">
                    <i class="ti ti-file-type-pdf"></i> Download Suite 3 Deliverable
                </a>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-purple">
                    <div class="kpi-header"><span class="kpi-label">Delivered Net Revenue</span><i class="ti ti-currency-rupee" style="color: var(--purple);"></i></div>
                    <div class="kpi-value">₹676.95 Cr</div>
                    <div class="kpi-sub">Delivered sales turnover</div>
                </div>
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Corporate OPEX</span><i class="ti ti-building-bank" style="color: var(--orange);"></i></div>
                    <div class="kpi-value">₹42.15 Cr</div>
                    <div class="kpi-sub">HQ Technology, Admin, Marketing</div>
                </div>
                <div class="kpi-card border-pink">
                    <div class="kpi-header"><span class="kpi-label">Store Branch OPEX</span><i class="ti ti-building-store" style="color: var(--pink);"></i></div>
                    <div class="kpi-value">₹38.80 Cr</div>
                    <div class="kpi-sub">Branch leases, utilities, maintenance</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">UPI Digital Settlement</span><i class="ti ti-qrcode" style="color: var(--emerald);"></i></div>
                    <div class="kpi-value">₹312.40 Cr</div>
                    <div class="kpi-sub">Zero MDR rail, lowest dispute rate (1.2%)</div>
                </div>
            </div>

            <div class="charts-grid-2">
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-credit-card" style="color: var(--cyan);"></i> Payment Tender Settlement Volume (₹ Cr)</div></div>
                    <div id="chart-fin-tenders"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header"><div class="chart-title"><i class="ti ti-receipt-2" style="color: var(--orange);"></i> OPEX Burn by Category (₹ Cr)</div></div>
                    <div id="chart-fin-opex"></div>
                </div>
            </div>
        </section>

        <!-- ==================================================================== -->
        <!-- TAB 9: SIMULATOR (TOOLS) -->
        <!-- ==================================================================== -->
        <section id="tab-simulator" class="dashboard-tab-content">
            <div class="page-header">
                <div>
                    <h2 class="page-title">Interactive What-If Scenario Simulator</h2>
                    <div class="page-desc">Real-time sensitivity modeling for price realization, return rates, advertising reallocation, and staffing</div>
                </div>
                <span class="status-badge badge-neutral"><i class="ti ti-cpu"></i> Instant Client-Side Computation</span>
            </div>

            <div class="slider-grid">
                <div class="slider-group">
                    <div class="slider-label"><span>Price Realization Delta:</span><span id="val-price" style="color: var(--cyan);">0%</span></div>
                    <input type="range" id="input-price" min="-10" max="15" value="0" step="1" oninput="runSimulation()">
                </div>
                <div class="slider-group">
                    <div class="slider-label"><span>Customer Return Rate:</span><span id="val-return" style="color: var(--rose);">2.97%</span></div>
                    <input type="range" id="input-return" min="1" max="8" value="3" step="0.5" oninput="runSimulation()">
                </div>
                <div class="slider-group">
                    <div class="slider-label"><span>Marketing Spend Shift:</span><span id="val-ad" style="color: var(--orange);">0%</span></div>
                    <input type="range" id="input-ad" min="-30" max="50" value="0" step="5" oninput="runSimulation()">
                </div>
                <div class="slider-group">
                    <div class="slider-label"><span>Store Staffing Optimization:</span><span id="val-hr" style="color: var(--emerald);">0%</span></div>
                    <input type="range" id="input-hr" min="-15" max="20" value="0" step="1" oninput="runSimulation()">
                </div>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card border-cyan">
                    <div class="kpi-header"><span class="kpi-label">Simulated Net Revenue</span><i class="ti ti-currency-rupee"></i></div>
                    <div class="kpi-value" id="sim-revenue">₹676.95 Cr</div>
                    <div class="kpi-sub" id="sim-rev-delta">&plusmn;₹0.00 Cr vs Baseline</div>
                </div>
                <div class="kpi-card border-orange">
                    <div class="kpi-header"><span class="kpi-label">Simulated Total OPEX</span><i class="ti ti-wallet"></i></div>
                    <div class="kpi-value" id="sim-opex">₹80.95 Cr</div>
                    <div class="kpi-sub" id="sim-opex-delta">&plusmn;₹0.00 Cr vs Baseline</div>
                </div>
                <div class="kpi-card border-emerald">
                    <div class="kpi-header"><span class="kpi-label">Operating Spread (EBIT)</span><i class="ti ti-trending-up"></i></div>
                    <div class="kpi-value" id="sim-ebit">₹596.00 Cr</div>
                    <div class="kpi-sub" id="sim-margin">88.04% Net Operating Margin</div>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer>
        <div>RetailMart V3 Enterprise Business Intelligence Platform &middot; Built with Django &amp; PostgreSQL 18</div>
        <div style="margin-top: 0.25rem;">Live Repository: <a href="https://github.com/Archanak2810/sales-customer-operations-analytics" target="_blank" style="color: var(--cyan); text-decoration: none;">github.com/Archanak2810/sales-customer-operations-analytics</a></div>
    </footer>

    <!-- Interactive Client Controller Script -->
    <script>
        // Tab Management
        const chartsInitialized = {};

        function switchTab(tabId) {
            document.querySelectorAll('.dashboard-tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));

            const targetSection = document.getElementById('tab-' + tabId);
            if (targetSection) targetSection.classList.add('active');

            // Highlight corresponding button
            document.querySelectorAll('.nav-tab-btn').forEach(btn => {
                if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(tabId)) {
                    btn.classList.add('active');
                }
            });

            window.location.hash = tabId;
            initTabCharts(tabId);
        }

        function toggleDropdown() {
            const menu = document.getElementById('dropmenu');
            menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
        }

        window.onclick = function(e) {
            if (!e.target.closest('#dropbtn')) {
                const menu = document.getElementById('dropmenu');
                if (menu) menu.style.display = 'none';
            }
        };

        // ApexCharts Initialization for Each Tab
        function initTabCharts(tabId) {
            if (chartsInitialized[tabId]) return;
            chartsInitialized[tabId] = true;

            const chartDefaults = {
                chart: { background: 'transparent', toolbar: { show: false } },
                tooltip: { theme: 'dark' },
                grid: { borderColor: '#2D3D5A', strokeDashArray: 3 }
            };

            if (tabId === 'executive') {
                new ApexCharts(document.querySelector("#chart-exec-rev"), {
                    ...chartDefaults,
                    series: [
                        { name: 'Delivered Net Sales (₹ Cr)', type: 'column', data: [22.4, 25.8, 28.1, 29.5, 31.2, 33.8, 32.4, 35.6, 38.2, 40.1, 42.5, 45.8] },
                        { name: 'Operating Outflows (₹ Cr)', type: 'line', data: [3.2, 3.4, 3.3, 3.5, 3.6, 3.8, 3.7, 3.9, 4.1, 4.2, 4.4, 4.6] }
                    ],
                    chart: { type: 'line', height: 280, ...chartDefaults.chart },
                    colors: ['#2CD4E1', '#F43F5E'],
                    stroke: { width: [0, 3], curve: 'smooth' },
                    xaxis: { categories: ['Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: [{ title: { text: 'Sales (₹ Cr)', style: { color: '#2CD4E1' } }, labels: { style: { colors: '#94A3B8' } } },
                            { opposite: true, title: { text: 'OPEX (₹ Cr)', style: { color: '#F43F5E' } }, labels: { style: { colors: '#94A3B8' } } }],
                    legend: { labels: { colors: '#CBD5E1' } }
                }).render();

                new ApexCharts(document.querySelector("#chart-exec-cat"), {
                    ...chartDefaults,
                    series: [284.15, 148.90, 115.40, 82.50, 46.00],
                    chart: { type: 'donut', height: 280, ...chartDefaults.chart },
                    labels: ['Electronics (27%)', 'Fashion (35%)', 'Home & Kitchen (30%)', 'Grocery (18%)', 'Health & Beauty (35%)'],
                    colors: ['#8B5CF6', '#EC4899', '#2CD4E1', '#FBBF24', '#10B981'],
                    legend: { position: 'bottom', labels: { colors: '#CBD5E1' } }
                }).render();
            }

            if (tabId === 'marketing') {
                new ApexCharts(document.querySelector("#chart-mktg-platform"), {
                    ...chartDefaults,
                    series: [34.12, 28.45, 18.94, 12.45, 9.04],
                    chart: { type: 'donut', height: 280, ...chartDefaults.chart },
                    labels: ['Google Ads (33.1%)', 'Facebook / Meta (27.6%)', 'Instagram (18.4%)', 'LinkedIn (12.1%)', 'Twitter / X (8.8%)'],
                    colors: ['#2CD4E1', '#8B5CF6', '#EC4899', '#F97316', '#FBBF24'],
                    legend: { position: 'bottom', labels: { colors: '#CBD5E1' } }
                }).render();

                new ApexCharts(document.querySelector("#chart-mktg-monthly"), {
                    ...chartDefaults,
                    series: [{ name: 'Spend (₹ Lakhs)', data: [68, 74, 82, 89, 95, 104, 112, 128, 142, 160, 175, 192] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    colors: ['#F97316'],
                    xaxis: { categories: ['Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' } } }
                }).render();
            }

            if (tabId === 'digital') {
                new ApexCharts(document.querySelector("#chart-digital-devices"), {
                    ...chartDefaults,
                    series: [59.91, 35.04, 5.05],
                    chart: { type: 'donut', height: 280, ...chartDefaults.chart },
                    labels: ['Mobile Web (59.9%)', 'Desktop Browser (35.0%)', 'Tablet (5.1%)'],
                    colors: ['#EC4899', '#2CD4E1', '#FBBF24'],
                    legend: { position: 'bottom', labels: { colors: '#CBD5E1' } }
                }).render();

                new ApexCharts(document.querySelector("#chart-digital-funnel"), {
                    ...chartDefaults,
                    series: [{ name: 'Sessions', data: [99320, 68400, 38200, 16400] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    plotOptions: { bar: { horizontal: true } },
                    colors: ['#8B5CF6'],
                    xaxis: { categories: ['1. Page Landing', '2. Product Search', '3. Cart Addition', '4. Checkout Submit'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' } } }
                }).render();
            }

            if (tabId === 'logistics') {
                new ApexCharts(document.querySelector("#chart-logistics-courier"), {
                    ...chartDefaults,
                    series: [{ name: 'On-Time SLA %', data: [84.2, 81.5, 78.9, 76.4, 75.1] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    colors: ['#10B981'],
                    xaxis: { categories: ['Delhivery', 'BlueDart', 'Ecom Express', 'Shadowfax', 'Xpressbees'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { min: 60, max: 100, labels: { style: { colors: '#94A3B8' }, formatter: v => v + '%' } }
                }).render();

                new ApexCharts(document.querySelector("#chart-logistics-leadtime"), {
                    ...chartDefaults,
                    series: [{ name: 'Parcels', data: [18450, 34200, 24800, 14200, 8900, 4437] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    colors: ['#2CD4E1'],
                    xaxis: { categories: ['1-2 Days', '3 Days', '4 Days', '5 Days', '6-7 Days', '8+ Days'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' } } }
                }).render();
            }

            if (tabId === 'sales') {
                new ApexCharts(document.querySelector("#chart-sales-trend"), {
                    ...chartDefaults,
                    series: [{ name: 'Revenue (₹ Cr)', data: [45.2, 48.6, 51.4, 54.2, 58.1, 62.4, 66.8, 71.5, 76.2, 81.0] }],
                    chart: { type: 'area', height: 280, ...chartDefaults.chart },
                    colors: ['#2CD4E1'],
                    xaxis: { categories: ['May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' } } }
                }).render();

                new ApexCharts(document.querySelector("#chart-sales-margins"), {
                    ...chartDefaults,
                    series: [{ name: 'Gross Margin %', data: [35.0, 35.0, 30.0, 27.0, 18.0] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    colors: ['#8B5CF6'],
                    xaxis: { categories: ['Fashion', 'Health & Beauty', 'Home & Kitchen', 'Electronics', 'Grocery'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' }, formatter: v => v + '%' } }
                }).render();
            }

            if (tabId === 'customers') {
                new ApexCharts(document.querySelector("#chart-cust-rfm"), {
                    ...chartDefaults,
                    series: [8885, 11240, 7450, 6518, 6287],
                    chart: { type: 'donut', height: 280, ...chartDefaults.chart },
                    labels: ['Champions (8,885)', 'Loyal Buyers (11,240)', 'Potential Loyalists (7,450)', 'At Risk (6,518)', 'Lost (6,287)'],
                    colors: ['#10B981', '#2CD4E1', '#8B5CF6', '#FBBF24', '#F43F5E'],
                    legend: { position: 'bottom', labels: { colors: '#CBD5E1' } }
                }).render();

                new ApexCharts(document.querySelector("#chart-cust-tiers"), {
                    ...chartDefaults,
                    series: [{ name: 'Spend (₹ Cr)', data: [312.4, 241.8, 122.75] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    colors: ['#FBBF24'],
                    xaxis: { categories: ['Platinum VIP', 'Gold Members', 'Silver Base'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' } } }
                }).render();
            }

            if (tabId === 'operations') {
                new ApexCharts(document.querySelector("#chart-ops-health"), {
                    ...chartDefaults,
                    series: [96678, 16880, 595],
                    chart: { type: 'donut', height: 280, ...chartDefaults.chart },
                    labels: ['Adequate & Surplus Stock (84.7%)', 'Low Stock at Reorder (14.8%)', 'Out of Stock OOS (0.5%)'],
                    colors: ['#10B981', '#FBBF24', '#F43F5E'],
                    legend: { position: 'bottom', labels: { colors: '#CBD5E1' } }
                }).render();

                new ApexCharts(document.querySelector("#chart-ops-scrap"), {
                    ...chartDefaults,
                    series: [{ name: 'Scrap Rate %', data: [1.8, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8, 3.1, 3.4] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    colors: ['#EC4899'],
                    xaxis: { categories: ['Line 1','Line 2','Line 3','Line 4','Line 5','Line 6','Line 7','Line 8','Line 9','Line 10'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' }, formatter: v => v + '%' } }
                }).render();
            }

            if (tabId === 'hr') {
                new ApexCharts(document.querySelector("#chart-hr-dept"), {
                    ...chartDefaults,
                    series: [1850, 420, 210, 180, 100, 95, 85, 60],
                    chart: { type: 'donut', height: 280, ...chartDefaults.chart },
                    labels: ['Store Retail (1,850)', 'Logistics (420)', 'IT (210)', 'Sales (180)', 'Admin (100)', 'Finance (95)', 'Marketing (85)', 'HR (60)'],
                    colors: ['#2CD4E1', '#8B5CF6', '#F97316', '#FBBF24', '#94A3B8', '#10B981', '#EC4899', '#0284C7'],
                    legend: { position: 'bottom', labels: { colors: '#CBD5E1' } }
                }).render();

                new ApexCharts(document.querySelector("#chart-hr-comp"), {
                    ...chartDefaults,
                    series: [{ name: 'Average Salary (₹)', data: [105000, 100000, 95000, 95000, 95000, 85000, 65000, 50000] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    plotOptions: { bar: { horizontal: true } },
                    colors: ['#EC4899'],
                    xaxis: { categories: ['IT Tech', 'Marketing', 'Finance', 'HR', 'Admin', 'Sales', 'Logistics', 'Store Staff'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' } } }
                }).render();
            }

            if (tabId === 'finance') {
                new ApexCharts(document.querySelector("#chart-fin-tenders"), {
                    ...chartDefaults,
                    series: [{ name: 'Settlement (₹ Cr)', data: [312.4, 241.1, 92.5, 55.23] }],
                    chart: { type: 'bar', height: 280, ...chartDefaults.chart },
                    colors: ['#10B981'],
                    xaxis: { categories: ['UPI Digital Rails', 'Credit & Debit Cards', 'Net Banking / RTGS', 'Cash on Delivery (COD)'], labels: { style: { colors: '#94A3B8' } } },
                    yaxis: { labels: { style: { colors: '#94A3B8' } } }
                }).render();

                new ApexCharts(document.querySelector("#chart-fin-opex"), {
                    ...chartDefaults,
                    series: [18.98, 18.50, 12.30, 11.20, 10.30, 9.67],
                    chart: { type: 'donut', height: 280, ...chartDefaults.chart },
                    labels: ['HQ Payroll (₹18.98 Cr)', 'Store Leases (₹18.50 Cr)', 'Utilities (₹12.30 Cr)', 'Tech & Cloud (₹11.20 Cr)', 'Marketing (₹10.30 Cr)', 'Maintenance (₹9.67 Cr)'],
                    colors: ['#8B5CF6', '#EC4899', '#FBBF24', '#2CD4E1', '#F97316', '#94A3B8'],
                    legend: { position: 'bottom', labels: { colors: '#CBD5E1' } }
                }).render();
            }
        }

        // What-If Scenario Simulator Calculation Engine
        function runSimulation() {
            const priceDelta = parseFloat(document.getElementById('input-price').value);
            const returnRate = parseFloat(document.getElementById('input-return').value);
            const adDelta = parseFloat(document.getElementById('input-ad').value);
            const hrDelta = parseFloat(document.getElementById('input-hr').value);

            document.getElementById('val-price').innerText = (priceDelta >= 0 ? '+' : '') + priceDelta + '%';
            document.getElementById('val-return').innerText = returnRate.toFixed(1) + '%';
            document.getElementById('val-ad').innerText = (adDelta >= 0 ? '+' : '') + adDelta + '%';
            document.getElementById('val-hr').innerText = (hrDelta >= 0 ? '+' : '') + hrDelta + '%';

            // Base Values
            const baseGrossRev = 701.23;
            const baseDiscounts = 24.27;
            const baseOpex = 80.95;

            // Calculations
            const simGross = baseGrossRev * (1 + (priceDelta / 100));
            const simReturnImpact = simGross * (returnRate / 100);
            const simNet = simGross - baseDiscounts - simReturnImpact;
            const revDiff = simNet - 676.95;

            const simAdOpex = 10.30 * (1 + (adDelta / 100));
            const simHrOpex = 18.98 * (1 + (hrDelta / 100));
            const fixedOpex = 80.95 - 10.30 - 18.98;
            const simOpexTotal = fixedOpex + simAdOpex + simHrOpex;
            const opexDiff = simOpexTotal - baseOpex;

            const simEbit = simNet - simOpexTotal;
            const simMarginPct = (simEbit / simNet) * 100;

            document.getElementById('sim-revenue').innerText = '₹' + simNet.toFixed(2) + ' Cr';
            document.getElementById('sim-rev-delta').innerText = (revDiff >= 0 ? '+' : '') + '₹' + revDiff.toFixed(2) + ' Cr vs Baseline';
            document.getElementById('sim-rev-delta').style.color = (revDiff >= 0 ? '#10B981' : '#F43F5E');

            document.getElementById('sim-opex').innerText = '₹' + simOpexTotal.toFixed(2) + ' Cr';
            document.getElementById('sim-opex-delta').innerText = (opexDiff >= 0 ? '+' : '') + '₹' + opexDiff.toFixed(2) + ' Cr vs Baseline';
            document.getElementById('sim-opex-delta').style.color = (opexDiff <= 0 ? '#10B981' : '#F43F5E');

            document.getElementById('sim-ebit').innerText = '₹' + simEbit.toFixed(2) + ' Cr';
            document.getElementById('sim-margin').innerText = simMarginPct.toFixed(2) + '% Net Operating Margin';
        }

        // On Load Init
        window.addEventListener('DOMContentLoaded', () => {
            const hash = window.location.hash.replace('#', '') || 'executive';
            switchTab(hash);
            runSimulation();
        });
    </script>
</body>
</html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated standalone index.html at {INDEX_FILE}!")
