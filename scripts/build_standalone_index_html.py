"""
Builds the standalone, client-side interactive HTML dashboard for GitHub Pages (index.html).
Maintains the exact dark corporate navy theme from the Django application and user screenshot:
- Navy Dark: #0F1F33, Navy Card: #183A5F, Purple Accent: #A459D0, Blue Border: #24598A
- Left-hand Global Filters Sidebar with Presets, Date Pickers, Geography, and Cost Center
- Top Navigation Bar with 3 Distinct Domain Suites (Suite 1, Suite 2, Suite 3), Cross, and Simulator
- Dedicated Marketing, Digital, Logistics, Sales, Customer, Operations, HR, Finance, Executive, and Simulator tabs
- Interactive ApexCharts, Simulator Levers, and Domain Deliverables Dropdown
"""

import os

BASE_DIR = r"g:\Data Analytics\SQL\12 SQL Batch June 2026\datasets\v3"
GITHUB_DIR = os.path.join(BASE_DIR, 'retailmart_bi_github')
INDEX_FILE = os.path.join(GITHUB_DIR, 'index.html')
SCRIPTS_FILE = os.path.join(BASE_DIR, 'scripts', 'build_standalone_index_html.py')
GITHUB_SCRIPTS_FILE = os.path.join(GITHUB_DIR, 'scripts', 'build_standalone_index_html.py')

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RetailMart V3 · Enterprise Analytics &amp; Domain Suites</title>
    
    <!-- Fonts: Outfit (Headings) & Inter (Body & Data) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Tabler Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.31.0/dist/tabler-icons.min.css">
    
    <!-- ApexCharts.js -->
    <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
    <script>
        // Disable dataLabels globally across all non-pie charts
        window.Apex = {
            dataLabels: { enabled: false }
        };
    </script>

    <style>
        /* Exact RetailMart V3 - Dark Corporate Design System */
        :root {
            --navy-dark: #0F1F33;
            --navy-card: #183A5F;
            --navy-hover: #1f4a7a;
            --blue-border: #24598A;
            --text-white: #FFFFFF;
            --text-light: #D5DCE5;
            --text-muted: #8E9BAE;
            
            --purple: #A459D0;      /* Revenue & positive performance */
            --purple-glow: rgba(164, 89, 208, 0.25);
            --pink: #E95B9F;        /* Customer metrics */
            --pink-glow: rgba(233, 91, 159, 0.2);
            --cyan: #2CD4E1;        /* Operations & quantities */
            --cyan-glow: rgba(44, 212, 225, 0.2);
            --orange: #E88E3E;      /* Costs & spend */
            --yellow: #FFBD4A;      /* Warnings & exceptions */
            --grid-color: #6F8298;  /* Axes & chart grid */
            --emerald: #10B981;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--navy-dark);
            color: var(--text-light);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.5;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
        }

        h1, h2, h3, h4, h5, h6, .font-heading {
            font-family: 'Outfit', sans-serif;
            color: var(--text-white);
            letter-spacing: -0.01em;
        }

        /* Layout */
        .app-container {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        .app-body {
            display: flex;
            flex-direction: row;
            flex: 1;
            min-height: calc(100vh - 65px);
            width: 100%;
        }

        /* Top Corporate Navigation */
        .top-navbar {
            background-color: rgba(15, 31, 51, 0.98);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--blue-border);
            position: sticky;
            top: 0;
            z-index: 1000;
            padding: 0.65rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }

        .brand-wrapper {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 9px;
            background: linear-gradient(135deg, var(--navy-card) 0%, var(--purple) 100%);
            border: 1px solid var(--blue-border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            color: #fff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .brand-title {
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.2;
            color: var(--text-white);
        }

        .brand-sub {
            font-size: 0.7rem;
            color: var(--text-muted);
            white-space: nowrap;
        }

        /* Nav Tabs & Suites */
        .nav-tabs {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background-color: rgba(24, 58, 95, 0.45);
            padding: 0.25rem 0.5rem;
            border-radius: 9999px;
            border: 1px solid var(--blue-border);
            overflow-x: auto;
            max-width: calc(100vw - 620px);
        }

        .suite-pill {
            display: flex;
            align-items: center;
            border-radius: 9999px;
            padding: 2px 4px;
            gap: 2px;
        }
        .suite-1 { background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.35); }
        .suite-2 { background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.35); }
        .suite-3 { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.35); }

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

        .nav-tab-link {
            padding: 0.32rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-light);
            text-decoration: none;
            background: transparent;
            border: none;
            border-radius: 9999px;
            transition: all 0.18s ease;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            cursor: pointer;
            font-family: inherit;
        }

        .nav-tab-link:hover {
            color: var(--text-white);
            background-color: rgba(36, 89, 138, 0.5);
        }

        .nav-tab-link.active {
            background-color: var(--purple);
            color: var(--text-white);
            box-shadow: 0 2px 8px var(--purple-glow);
        }

        /* Top Action Buttons */
        .header-actions {
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }

        .btn-dropdown {
            background: rgba(37, 99, 235, 0.25);
            border: 1px solid rgba(37, 99, 235, 0.6);
            color: #93C5FD;
            padding: 0.38rem 0.75rem;
            font-size: 0.75rem;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }
        .btn-dropdown:hover {
            background: rgba(37, 99, 235, 0.4);
            border-color: #60A5FA;
            color: #FFFFFF;
        }

        .dropdown-menu {
            display: none;
            position: absolute;
            right: 0;
            top: calc(100% + 6px);
            width: 330px;
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 8px;
            box-shadow: 0 16px 36px rgba(0,0,0,0.7);
            z-index: 1050;
            padding: 6px 0;
            text-align: left;
            max-height: 85vh;
            overflow-y: auto;
        }

        .dropdown-header {
            padding: 6px 14px;
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid #334155;
        }

        .dropdown-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            padding: 4px 10px;
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
            transition: opacity 0.15s;
        }
        .dropdown-btn-link:hover { opacity: 0.85; }
        .link-pdf { background: rgba(244,63,94,0.15); color: #FDA4AF; border: 1px solid rgba(244,63,94,0.3); }
        .link-doc { background: rgba(59,130,246,0.15); color: #93C5FD; border: 1px solid rgba(59,130,246,0.3); }
        .link-html { background: rgba(13,148,136,0.15); color: #5EEAD4; border: 1px solid rgba(13,148,136,0.3); }

        /* Left-Hand Sidebar Filters ("Keep the filter tabs") */
        .sidebar-filters {
            width: 290px;
            min-width: 290px;
            max-width: 290px;
            background-color: var(--navy-card);
            border-right: 1px solid var(--blue-border);
            height: calc(100vh - 65px);
            position: sticky;
            top: 65px;
            overflow-y: auto;
            overflow-x: hidden;
            z-index: 90;
            box-shadow: 2px 0 16px rgba(0, 0, 0, 0.3);
            scrollbar-width: thin;
            scrollbar-color: var(--blue-border) var(--navy-dark);
        }

        .sidebar-filters::-webkit-scrollbar { width: 6px; }
        .sidebar-filters::-webkit-scrollbar-track { background: var(--navy-dark); }
        .sidebar-filters::-webkit-scrollbar-thumb { background-color: var(--blue-border); border-radius: 3px; }

        .sidebar-filter-wrapper {
            padding: 1.25rem 1.15rem;
        }

        .sidebar-filter-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 0.85rem;
            border-bottom: 1px solid rgba(36, 89, 138, 0.4);
            margin-bottom: 1rem;
        }

        .sidebar-filter-form {
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
        }

        .filter-actions-top {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.35rem;
        }

        .filter-section-title {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--cyan);
            display: flex;
            align-items: center;
            gap: 0.35rem;
            margin-top: 0.4rem;
            margin-bottom: 0.2rem;
        }

        .filter-divider {
            height: 1px;
            background: rgba(36, 89, 138, 0.3);
            margin: 0.4rem 0;
        }

        .filter-presets-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.4rem;
            margin-bottom: 0.25rem;
        }

        .preset-btn {
            background-color: rgba(15, 31, 51, 0.7);
            border: 1px solid var(--blue-border);
            color: var(--text-light);
            border-radius: 6px;
            padding: 0.4rem 0.45rem;
            font-size: 0.72rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            font-family: inherit;
        }

        .preset-btn:hover, .preset-btn.active {
            background-color: var(--navy-hover);
            color: var(--text-white);
            border-color: var(--cyan);
        }

        .filter-field {
            display: flex;
            flex-direction: column;
        }

        .filter-field label {
            display: block;
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 0.3rem;
        }

        .filter-input, .filter-select {
            width: 100%;
            background-color: var(--navy-dark);
            border: 1px solid var(--blue-border);
            color: var(--text-white);
            padding: 0.5rem 0.75rem;
            border-radius: 8px;
            font-size: 0.82rem;
            font-family: inherit;
            transition: border-color 0.2s;
        }

        .filter-input:focus, .filter-select:focus {
            outline: none;
            border-color: var(--cyan);
        }

        .sidebar-freshness {
            margin-top: 1.25rem;
            padding-top: 0.85rem;
            border-top: 1px solid rgba(36, 89, 138, 0.4);
            font-size: 0.68rem;
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            padding: 0.5rem 1rem;
            font-size: 0.82rem;
            font-weight: 600;
            border-radius: 8px;
            border: 1px solid transparent;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.18s ease;
            font-family: inherit;
        }

        .btn-primary {
            background-color: var(--purple);
            color: var(--text-white);
        }
        .btn-primary:hover {
            background-color: #9247be;
            box-shadow: 0 2px 10px var(--purple-glow);
        }

        .btn-secondary {
            background-color: rgba(36, 89, 138, 0.4);
            border-color: var(--blue-border);
            color: var(--text-white);
        }
        .btn-secondary:hover {
            background-color: var(--blue-border);
        }

        .btn-reset {
            background-color: transparent;
            color: var(--text-muted);
            border: 1px solid rgba(111, 130, 152, 0.4);
        }
        .btn-reset:hover {
            color: var(--text-white);
            border-color: var(--text-muted);
        }

        /* Main Content Container */
        .main-content {
            flex: 1;
            min-width: 0;
            padding: 1.5rem 2rem 3rem 2rem;
            width: 100%;
            max-width: 100%;
        }

        .tab-pane {
            display: none;
            animation: fadeIn 0.2s ease-in-out;
        }
        .tab-pane.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Page Header */
        .page-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid rgba(36, 89, 138, 0.4);
            padding-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .page-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-white);
        }

        /* KPI Cards & Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.75rem;
        }

        .kpi-card {
            background: linear-gradient(180deg, var(--navy-card) 0%, rgba(24, 58, 95, 0.75) 100%);
            border: 1px solid var(--blue-border);
            border-radius: 14px;
            padding: 1.25rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, border-color 0.2s;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: var(--cyan);
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
        }
        .accent-purple::before { background: var(--purple); }
        .accent-pink::before { background: var(--pink); }
        .accent-cyan::before { background: var(--cyan); }
        .accent-orange::before { background: var(--orange); }
        .accent-yellow::before { background: var(--yellow); }

        .kpi-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }

        .kpi-title {
            font-size: 0.76rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--text-muted);
        }

        .kpi-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-white);
            font-family: 'Outfit', sans-serif;
            margin-bottom: 0.35rem;
        }

        .kpi-subtext {
            font-size: 0.75rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .kpi-badge {
            font-size: 0.68rem;
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            font-weight: 700;
        }
        .badge-neutral {
            color: var(--text-muted);
            background-color: rgba(142, 155, 174, 0.15);
        }
        .badge-positive {
            color: #34D399;
            background-color: rgba(52, 211, 153, 0.15);
        }
        .badge-success {
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        /* Charts */
        .charts-grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.75rem;
        }

        .chart-card {
            background-color: var(--navy-card);
            border: 1px solid var(--blue-border);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }

        .chart-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(36, 89, 138, 0.4);
            padding-bottom: 0.75rem;
        }

        .chart-title {
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-white);
        }

        /* Tables & Action Cards */
        .action-card, .table-card {
            background-color: var(--navy-card);
            border: 1px solid var(--blue-border);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            overflow-x: auto;
        }

        .action-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid rgba(36, 89, 138, 0.4);
        }

        .action-table, .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            text-align: left;
        }

        .action-table th, .data-table th {
            background-color: rgba(15, 31, 51, 0.7);
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.05em;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--blue-border);
        }

        .action-table td, .data-table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(36, 89, 138, 0.3);
            color: var(--text-light);
        }

        .action-table tr:hover td, .data-table tr:hover td {
            background-color: rgba(36, 89, 138, 0.25);
            color: var(--text-white);
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
        }

        .toast-notify {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #1E293B;
            border: 1px solid var(--cyan);
            color: #FFFFFF;
            padding: 0.75rem 1.25rem;
            border-radius: 8px;
            font-size: 0.85rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            display: none;
            align-items: center;
            gap: 0.6rem;
            z-index: 9999;
            animation: slideUp 0.3s ease;
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        /* Simulator Controls */
        .slider-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.5rem;
        }
        .slider-group {
            background: rgba(15, 31, 51, 0.7);
            border: 1px solid var(--blue-border);
            border-radius: 8px;
            padding: 1.1rem;
        }
        .slider-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-white);
            margin-bottom: 0.6rem;
        }
        input[type=range] {
            width: 100%;
            height: 6px;
            background: #24598A;
            border-radius: 3px;
            outline: none;
            -webkit-appearance: none;
        }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--purple);
            cursor: pointer;
            box-shadow: 0 0 6px var(--purple-glow);
        }

        @media (max-width: 1024px) {
            .app-body { flex-direction: column; }
            .sidebar-filters {
                width: 100%;
                min-width: 100%;
                max-width: 100%;
                height: auto;
                position: static;
                border-right: none;
                border-bottom: 1px solid var(--blue-border);
            }
            .charts-grid-2 { grid-template-columns: 1fr; }
            .nav-tabs { max-width: 100%; }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Top Corporate Navigation -->
        <header class="top-navbar">
            <div class="brand-wrapper">
                <div class="brand-icon">
                    <i class="ti ti-building-store"></i>
                </div>
                <div>
                    <h1 class="brand-title">
                        RetailMart <span style="color: var(--purple);">V3</span>
                    </h1>
                    <div class="brand-sub">
                        Enterprise Business Intelligence
                    </div>
                </div>
            </div>

            <!-- Unified Domain Suites Navigation -->
            <nav class="nav-tabs">
                <!-- Area 1: Executive Summary -->
                <button class="nav-tab-link" id="nav-executive" onclick="switchTab('executive')">
                    <i class="ti ti-layout-dashboard"></i> Executive
                </button>

                <!-- Domain Suite 1: Growth & Supply Chain -->
                <div class="suite-pill suite-1">
                    <span class="suite-tag tag-1">Suite 1</span>
                    <button class="nav-tab-link active" id="nav-marketing" onclick="switchTab('marketing')">
                        <i class="ti ti-target"></i> Marketing
                    </button>
                    <button class="nav-tab-link" id="nav-digital" onclick="switchTab('digital')">
                        <i class="ti ti-device-analytics"></i> Digital
                    </button>
                    <button class="nav-tab-link" id="nav-logistics" onclick="switchTab('logistics')">
                        <i class="ti ti-truck-delivery"></i> Logistics
                    </button>
                </div>

                <!-- Domain Suite 2: Commercial & Customer Operations -->
                <div class="suite-pill suite-2">
                    <span class="suite-tag tag-2">Suite 2</span>
                    <button class="nav-tab-link" id="nav-sales" onclick="switchTab('sales')">
                        <i class="ti ti-shopping-cart"></i> Sales
                    </button>
                    <button class="nav-tab-link" id="nav-customers" onclick="switchTab('customers')">
                        <i class="ti ti-user-check"></i> Customer
                    </button>
                    <button class="nav-tab-link" id="nav-operations" onclick="switchTab('operations')">
                        <i class="ti ti-boxes"></i> Operations
                    </button>
                </div>

                <!-- Domain Suite 3: People & Financial Governance -->
                <div class="suite-pill suite-3">
                    <span class="suite-tag tag-3">Suite 3</span>
                    <button class="nav-tab-link" id="nav-hr" onclick="switchTab('hr')">
                        <i class="ti ti-users"></i> HR
                    </button>
                    <button class="nav-tab-link" id="nav-finance" onclick="switchTab('finance')">
                        <i class="ti ti-chart-line"></i> Finance
                    </button>
                </div>

                <!-- Cross-Functional & Simulator -->
                <button class="nav-tab-link" id="nav-cross" onclick="switchTab('cross')">
                    <i class="ti ti-arrows-cross"></i> Cross
                </button>
                <button class="nav-tab-link" id="nav-simulator" onclick="switchTab('simulator')">
                    <i class="ti ti-calculator"></i> Simulator
                </button>
            </nav>

            <!-- User Status & Quick Actions -->
            <div class="header-actions">
                <!-- Comprehensive Deliverables Dropdown -->
                <div style="position: relative; display: inline-block;">
                    <button id="reports-dropdown-btn" type="button" class="btn-dropdown" onclick="toggleDeliverablesDropdown()">
                        <i class="ti ti-download"></i> Domain Deliverables <i class="ti ti-chevron-down" style="font-size: 0.7rem;"></i>
                    </button>
                    
                    <div id="reports-dropdown-menu" class="dropdown-menu">
                        <!-- Suite 1 Deliverables -->
                        <div class="dropdown-header" style="color: #38BDF8; background: rgba(56, 189, 248, 0.08);">
                            Suite 1: Marketing, Digital &amp; Logistics
                        </div>
                        <div class="dropdown-grid">
                            <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="dropdown-btn-link link-pdf">
                                <i class="ti ti-file-type-pdf"></i> PDF
                            </a>
                            <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.docx" download class="dropdown-btn-link link-doc">
                                <i class="ti ti-file-type-docx"></i> Word
                            </a>
                            <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.html" target="_blank" class="dropdown-btn-link link-html">
                                <i class="ti ti-file-type-html"></i> HTML
                            </a>
                        </div>

                        <!-- Suite 2 Deliverables -->
                        <div class="dropdown-header" style="color: #C084FC; background: rgba(192, 132, 252, 0.08);">
                            Suite 2: Sales, Customer &amp; Operations
                        </div>
                        <div class="dropdown-grid">
                            <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="dropdown-btn-link link-pdf">
                                <i class="ti ti-file-type-pdf"></i> PDF
                            </a>
                            <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.docx" download class="dropdown-btn-link link-doc">
                                <i class="ti ti-file-type-docx"></i> Word
                            </a>
                            <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.html" target="_blank" class="dropdown-btn-link link-html">
                                <i class="ti ti-file-type-html"></i> HTML
                            </a>
                        </div>

                        <!-- Suite 3 Deliverables -->
                        <div class="dropdown-header" style="color: #34D399; background: rgba(52, 211, 153, 0.08);">
                            Suite 3: HR &amp; Financial Governance
                        </div>
                        <div class="dropdown-grid">
                            <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.pdf" target="_blank" class="dropdown-btn-link link-pdf">
                                <i class="ti ti-file-type-pdf"></i> PDF
                            </a>
                            <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.docx" download class="dropdown-btn-link link-doc">
                                <i class="ti ti-file-type-docx"></i> Word
                            </a>
                            <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.html" target="_blank" class="dropdown-btn-link link-html">
                                <i class="ti ti-file-type-html"></i> HTML
                            </a>
                        </div>

                        <!-- Master SQL & Repository -->
                        <div class="dropdown-header" style="color: #94A3B8;">Master Technical Assets</div>
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

                <button class="btn btn-secondary" onclick="simulateLogout()" title="Logout" style="padding: 0.38rem 0.7rem; font-size: 0.75rem;">
                    <i class="ti ti-logout"></i> Logout
                </button>
            </div>
        </header>

        <!-- Main Application Body: Left Hand Sidebar + Content Area -->
        <div class="app-body">
            <!-- Left Hand Corner Filter Sidebar ("Keep the filter tabs") -->
            <aside class="sidebar-filters" id="sidebar-filters">
                <div class="sidebar-filter-wrapper">
                    <div class="sidebar-filter-header">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <i class="ti ti-adjustments-horizontal" style="color: var(--cyan); font-size: 1.15rem;"></i>
                            <span style="font-weight: 700; font-size: 0.95rem; color: var(--text-white);">Global Filters</span>
                        </div>
                        <span class="kpi-badge badge-neutral" style="font-size: 0.65rem; padding: 0.15rem 0.45rem;">PostgreSQL Live</span>
                    </div>

                    <form id="global-filter-form" onsubmit="handleApplyFilters(event)" class="sidebar-filter-form">
                        <!-- Top Action Buttons -->
                        <div class="filter-actions-top">
                            <button type="submit" class="btn btn-primary" style="flex: 1; padding: 0.5rem 0.6rem; font-size: 0.8rem;">
                                <i class="ti ti-filter"></i> Apply
                            </button>
                            <button type="button" id="btn-reset-filters" onclick="handleResetFilters()" class="btn btn-reset" title="Reset to defaults" style="padding: 0.5rem 0.65rem; font-size: 0.8rem;">
                                <i class="ti ti-rotate-clockwise"></i> Reset
                            </button>
                        </div>

                        <!-- Quick Presets -->
                        <div class="filter-section-title">
                            <i class="ti ti-history"></i> Quick Presets
                        </div>
                        <div class="filter-presets-grid">
                            <button type="button" onclick="applyDatePreset('all')" class="preset-btn active" id="preset-all">Full Horizon</button>
                            <button type="button" onclick="applyDatePreset('2025')" class="preset-btn" id="preset-2025">CY 2025</button>
                            <button type="button" onclick="applyDatePreset('90d')" class="preset-btn" id="preset-90d">90 Days</button>
                            <button type="button" onclick="applyDatePreset('30d')" class="preset-btn" id="preset-30d">30 Days</button>
                        </div>

                        <div class="filter-divider"></div>

                        <!-- Date Horizon -->
                        <div class="filter-section-title">
                            <i class="ti ti-calendar"></i> Date Horizon
                        </div>
                        <div class="filter-field">
                            <label for="filter-start-date">Start Date</label>
                            <input type="date" id="filter-start-date" name="start_date" class="filter-input" value="2024-01-01" min="2024-01-01" max="2026-02-26">
                        </div>

                        <div class="filter-field">
                            <label for="filter-end-date">End Date</label>
                            <input type="date" id="filter-end-date" name="end_date" class="filter-input" value="2026-02-26" min="2024-01-01" max="2026-02-26">
                        </div>

                        <div class="filter-divider"></div>

                        <!-- Geographic Scope -->
                        <div class="filter-section-title">
                            <i class="ti ti-map-pin"></i> Geographic Scope
                        </div>
                        <div class="filter-field">
                            <label for="filter-region">Region</label>
                            <select id="filter-region" name="region_id" class="filter-select" onchange="handleRegionChange()">
                                <option value="">All Regions (20)</option>
                                <option value="15">Central (Mizoram)</option>
                                <option value="13">Central (Arunachal Pradesh)</option>
                                <option value="5">East (Himachal Pradesh)</option>
                                <option value="18">North (Manipur)</option>
                                <option value="17">North (Tamil Nadu)</option>
                                <option value="3">North (Andhra Pradesh)</option>
                                <option value="2">North (Bihar)</option>
                                <option value="10">North (Assam)</option>
                                <option value="14">North (Gujarat)</option>
                                <option value="19">North (Uttar Pradesh)</option>
                                <option value="1">North East (Rajasthan)</option>
                                <option value="4">North East (Telangana)</option>
                                <option value="9">North East (Nagaland)</option>
                                <option value="11">North East (Odisha)</option>
                                <option value="12">North East (Maharashtra)</option>
                                <option value="8">South (Sikkim)</option>
                                <option value="7">South (Chhattisgarh)</option>
                                <option value="6">South (Haryana)</option>
                                <option value="20">South (West Bengal)</option>
                                <option value="16">West (Punjab)</option>
                            </select>
                        </div>

                        <div class="filter-field">
                            <label for="filter-store">Store (Cascading)</label>
                            <select id="filter-store" name="store_id" class="filter-select">
                                <option value="">All Stores (200)</option>
                                <option value="146">RetailMart Agartala Flagship (Agartala)</option>
                                <option value="193">RetailMart Agra Superstore (Agra)</option>
                                <option value="12">RetailMart Ahmedabad West (Ahmedabad)</option>
                                <option value="45">RetailMart Bangalore Indiranagar (Bangalore)</option>
                                <option value="67">RetailMart Bhopal Central (Bhopal)</option>
                                <option value="89">RetailMart Chennai OMR (Chennai)</option>
                                <option value="102">RetailMart Delhi CP Flagship (Delhi)</option>
                                <option value="115">RetailMart Hyderabad Hitec City (Hyderabad)</option>
                                <option value="128">RetailMart Kolkata Park Street (Kolkata)</option>
                                <option value="140">RetailMart Mumbai Bandra Megastore (Mumbai)</option>
                                <option value="177">RetailMart Pune Viman Nagar (Pune)</option>
                            </select>
                        </div>

                        <div class="filter-divider"></div>

                        <!-- HR & Finance Segmentation -->
                        <div class="filter-section-title">
                            <i class="ti ti-building"></i> Organization &amp; Cost Center
                        </div>
                        <div class="filter-field">
                            <label for="filter-department">HR Department</label>
                            <select id="filter-department" name="dept_id" class="filter-select">
                                <option value="">All Departments (10)</option>
                                <option value="8">Customer Support</option>
                                <option value="4">Finance</option>
                                <option value="5">HR</option>
                                <option value="6">IT</option>
                                <option value="9">Legal</option>
                                <option value="7">Logistics</option>
                                <option value="3">Marketing</option>
                                <option value="2">Operations</option>
                                <option value="10">Procurement</option>
                                <option value="1">Sales</option>
                            </select>
                        </div>

                        <div class="filter-field">
                            <label for="filter-expense-cat">Expense Category</label>
                            <select id="filter-expense-cat" name="exp_cat_id" class="filter-select">
                                <option value="">All Expense Types (15)</option>
                                <option value="14">Events</option>
                                <option value="9">Insurance</option>
                                <option value="11">Logistics</option>
                                <option value="3">Maintenance</option>
                                <option value="4">Marketing</option>
                                <option value="15">Miscellaneous</option>
                                <option value="7">Office Supplies</option>
                                <option value="8">Payroll</option>
                                <option value="12">R&amp;D</option>
                                <option value="1">Rent</option>
                                <option value="5">Software</option>
                                <option value="10">Taxes</option>
                                <option value="13">Training</option>
                                <option value="6">Travel</option>
                                <option value="2">Utilities</option>
                            </select>
                        </div>

                        <!-- Bottom Apply Button -->
                        <div style="margin-top: 0.85rem;">
                            <button type="submit" class="btn btn-primary" style="width: 100%; padding: 0.6rem; font-size: 0.85rem; font-weight: 600;">
                                <i class="ti ti-filter"></i> Apply Filters
                            </button>
                        </div>

                        <!-- Data Freshness -->
                        <div class="sidebar-freshness">
                            <div style="display: flex; align-items: center; gap: 0.35rem;">
                                <i class="ti ti-database" style="color: var(--cyan);"></i>
                                <span>Database: <strong>PostgreSQL 18.4</strong></span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.35rem;">
                                <i class="ti ti-clock" style="color: var(--text-muted);"></i>
                                <span>Freshness: <strong>2026-02-26 23:59</strong></span>
                            </div>
                        </div>
                    </form>
                </div>
            </aside>

            <!-- Main Dashboard Surface -->
            <main class="main-content">

                <!-- ========================================================= -->
                <!-- 1. MARKETING INTELLIGENCE DASHBOARD (Default Active View) -->
                <!-- ========================================================= -->
                <div id="tab-marketing" class="tab-pane active">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Marketing Intelligence Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Paid &amp; Owned Media Acquisition, Multi-Platform Ad Spend, Campaign Pacing &amp; Email Engagement
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div class="filter-window-badge" style="font-size: 0.75rem; color: var(--cyan); background: rgba(44, 212, 225, 0.1); padding: 0.35rem 0.75rem; border-radius: 6px; border: 1px solid rgba(44, 212, 225, 0.3);">
                                <i class="ti ti-calendar-time"></i> Active Window: <span id="mkt-window-tag">2024-01-01 to 2026-02-26</span>
                            </div>
                            <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <!-- Marketing Headline KPI Cards -->
                    <div class="kpi-grid">
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header">
                                <span class="kpi-title">Total Campaign Ad Spend</span>
                                <i class="ti ti-currency-rupee" style="color: var(--orange);"></i>
                            </div>
                            <div class="kpi-value" id="kpi-mkt-spend">₹10302874.41</div>
                            <div class="kpi-subtext">Across 5 paid platforms</div>
                        </div>

                        <div class="kpi-card accent-purple">
                            <div class="kpi-header">
                                <span class="kpi-title">Authorized Budget</span>
                                <i class="ti ti-wallet" style="color: var(--purple);"></i>
                            </div>
                            <div class="kpi-value" id="kpi-mkt-budget">₹126286595.49</div>
                            <div class="kpi-subtext">244 active initiatives</div>
                        </div>

                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header">
                                <span class="kpi-title">Budget Utilization</span>
                                <i class="ti ti-chart-pie" style="color: var(--cyan);"></i>
                            </div>
                            <div class="kpi-value" id="kpi-mkt-util">8.2%</div>
                            <div class="kpi-subtext">Pacing vs budget cap</div>
                        </div>

                        <div class="kpi-card accent-pink">
                            <div class="kpi-header">
                                <span class="kpi-title">Emails Delivered</span>
                                <i class="ti ti-mail" style="color: var(--pink);"></i>
                            </div>
                            <div class="kpi-value" id="kpi-mkt-emails">12952186</div>
                            <div class="kpi-subtext">Outbound customer comms</div>
                        </div>

                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header">
                                <span class="kpi-title">Email Open Rate</span>
                                <i class="ti ti-mail-opened" style="color: var(--cyan);"></i>
                            </div>
                            <div class="kpi-value" id="kpi-mkt-open">30.2%</div>
                            <div class="kpi-subtext">3907091 opened emails</div>
                        </div>

                        <div class="kpi-card accent-purple">
                            <div class="kpi-header">
                                <span class="kpi-title">Email Click-Through Rate</span>
                                <i class="ti ti-cursor-text" style="color: var(--purple);"></i>
                            </div>
                            <div class="kpi-value" id="kpi-mkt-ctr">22.9%</div>
                            <div class="kpi-subtext">CTR on opened volume</div>
                        </div>
                    </div>

                    <!-- Charts Row 1: Platform Spend Mix & Monthly Spend Trajectory -->
                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-brand-facebook" style="color: var(--pink);"></i>
                                    Ad Spend Allocation by Platform (₹)
                                </span>
                            </div>
                            <div id="chart-platform-spend"></div>
                        </div>

                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-chart-line" style="color: var(--orange);"></i>
                                    Monthly Ad Spend Trajectory by Platform
                                </span>
                            </div>
                            <div id="chart-spend-trend"></div>
                        </div>
                    </div>

                    <!-- Charts Row 2: Email Engagement Pacing & Top Campaigns Pacing -->
                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-mail-fast" style="color: var(--cyan);"></i>
                                    Email Marketing Performance: Open &amp; Click Rates (%)
                                </span>
                            </div>
                            <div id="chart-email-trend"></div>
                        </div>

                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-target-arrow" style="color: var(--purple);"></i>
                                    Top 10 Campaigns by Spend &amp; Budget Pacing
                                </span>
                            </div>
                            <div id="chart-campaign-pacing"></div>
                        </div>
                    </div>

                    <!-- Action Table: Top Campaigns Detailed Drilldown -->
                    <div class="action-card">
                        <div class="action-header">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <i class="ti ti-list-details" style="color: var(--cyan);"></i>
                                <h3 style="font-size: 1rem; font-weight: 600; color: var(--text-white);">
                                    Marketing Campaign Portfolio Performance &amp; Utilization
                                </h3>
                            </div>
                            <span style="font-size: 0.72rem; color: var(--text-muted);">
                                Ranked by total historical spend
                            </span>
                        </div>
                        <div style="overflow-x: auto;">
                            <table class="action-table">
                                <thead>
                                    <tr>
                                        <th>Campaign ID</th>
                                        <th>Campaign Initiative Name</th>
                                        <th>Date Window</th>
                                        <th>Authorized Budget</th>
                                        <th>Realized Spend</th>
                                        <th>Pacing (%)</th>
                                        <th>Platform Reach</th>
                                        <th>Status Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td style="font-weight: 600; color: var(--cyan);">#142</td>
                                        <td style="color: var(--text-white); font-weight: 500;">Diwali Mega Sale 2025</td>
                                        <td style="color: var(--text-muted); font-size: 0.75rem;">2025-10-01 to 2025-11-15</td>
                                        <td>₹1,850,000.00</td>
                                        <td style="color: var(--orange); font-weight: 600;">₹425,890.00</td>
                                        <td><span class="status-badge badge-success">23.0%</span></td>
                                        <td>5 Platforms</td>
                                        <td><span class="status-badge badge-neutral">Optimal Yield</span></td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: 600; color: var(--cyan);">#89</td>
                                        <td style="color: var(--text-white); font-weight: 500;">Independence Tech Fest 2024</td>
                                        <td style="color: var(--text-muted); font-size: 0.75rem;">2024-08-01 to 2024-08-20</td>
                                        <td>₹1,500,000.00</td>
                                        <td style="color: var(--orange); font-weight: 600;">₹382,150.00</td>
                                        <td><span class="status-badge badge-success">25.5%</span></td>
                                        <td>4 Platforms</td>
                                        <td><span class="status-badge badge-neutral">Completed</span></td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: 600; color: var(--cyan);">#211</td>
                                        <td style="color: var(--text-white); font-weight: 500;">Republic Day Wardrobe Refresh</td>
                                        <td style="color: var(--text-muted); font-size: 0.75rem;">2026-01-15 to 2026-01-31</td>
                                        <td>₹1,200,000.00</td>
                                        <td style="color: var(--orange); font-weight: 600;">₹294,600.00</td>
                                        <td><span class="status-badge badge-success">24.6%</span></td>
                                        <td>4 Platforms</td>
                                        <td><span class="status-badge badge-neutral">Active</span></td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: 600; color: var(--cyan);">#56</td>
                                        <td style="color: var(--text-white); font-weight: 500;">Summer Home &amp; Kitchen Clearance</td>
                                        <td style="color: var(--text-muted); font-size: 0.75rem;">2024-04-10 to 2024-05-15</td>
                                        <td>₹950,000.00</td>
                                        <td style="color: var(--orange); font-weight: 600;">₹248,320.00</td>
                                        <td><span class="status-badge badge-success">26.1%</span></td>
                                        <td>3 Platforms</td>
                                        <td><span class="status-badge badge-neutral">Completed</span></td>
                                    </tr>
                                    <tr>
                                        <td style="font-weight: 600; color: var(--cyan);">#178</td>
                                        <td style="color: var(--text-white); font-weight: 500;">Monsoon Footwear Blitz</td>
                                        <td style="color: var(--text-muted); font-size: 0.75rem;">2025-07-01 to 2025-08-10</td>
                                        <td>₹800,000.00</td>
                                        <td style="color: var(--orange); font-weight: 600;">₹198,740.00</td>
                                        <td><span class="status-badge badge-success">24.8%</span></td>
                                        <td>3 Platforms</td>
                                        <td><span class="status-badge badge-neutral">Completed</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 2. DIGITAL EXPERIENCE & JOURNEY DASHBOARD                 -->
                <!-- ========================================================= -->
                <div id="tab-digital" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Digital Experience &amp; Journey Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Web Traffic, Session Dynamics, Device Ecosystem, User Behavioral Funnels &amp; Landing Page Velocity
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div style="font-size: 0.75rem; color: var(--pink); background: rgba(233, 91, 159, 0.1); padding: 0.35rem 0.75rem; border-radius: 6px; border: 1px solid rgba(233, 91, 159, 0.3);">
                                <i class="ti ti-activity"></i> Live Clickstream Analytics
                            </div>
                            <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header"><span class="kpi-title">Total Web Sessions</span><i class="ti ti-device-analytics" style="color: var(--pink);"></i></div>
                            <div class="kpi-value">99,320</div>
                            <div class="kpi-subtext">Unique browsing sessions</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Total Page Views</span><i class="ti ti-browser" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">500,000</div>
                            <div class="kpi-subtext">Aggregated screen impressions</div>
                        </div>
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Identified Customers</span><i class="ti ti-user-check" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">40,380</div>
                            <div class="kpi-subtext">Logged-in customer accounts</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Pages per Session</span><i class="ti ti-arrows-shuffle" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">5.03</div>
                            <div class="kpi-subtext">Browsing depth intensity</div>
                        </div>
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header"><span class="kpi-title">Mobile Traffic Share</span><i class="ti ti-device-mobile" style="color: var(--orange);"></i></div>
                            <div class="kpi-value">59.9%</div>
                            <div class="kpi-subtext">Mobile web penetration</div>
                        </div>
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Total User Interactions</span><i class="ti ti-hand-click" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">500,000</div>
                            <div class="kpi-subtext">142,500 form submits</div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-devices" style="color: var(--pink);"></i> Device &amp; Operating System Matrix</span>
                            </div>
                            <div id="chart-device-os"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-chart-line" style="color: var(--cyan);"></i> Monthly Web Traffic Velocity (Views vs Sessions)</span>
                            </div>
                            <div id="chart-traffic-trend"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 3. LOGISTICS & SUPPLY CHAIN DASHBOARD                     -->
                <!-- ========================================================= -->
                <div id="tab-logistics" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Logistics &amp; Supply Chain Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Order Fulfillment, Courier SLA Benchmarks, Delivery Lead Times, Warehouse Capacity &amp; Store Stockout Risk
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div style="font-size: 0.75rem; color: var(--cyan); background: rgba(44, 212, 225, 0.1); padding: 0.35rem 0.75rem; border-radius: 6px; border: 1px solid rgba(44, 212, 225, 0.3);">
                                <i class="ti ti-truck-loading"></i> Enterprise Fulfillment Network
                            </div>
                            <a href="./project_documents/documentation/RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Delivered Shipments</span><i class="ti ti-package" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">82,540</div>
                            <div class="kpi-subtext">Completed parcels</div>
                        </div>
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Carrier On-Time SLA</span><i class="ti ti-clock-check" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">79.8%</div>
                            <div class="kpi-subtext">&le; 5 days transit target</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Avg Delivery Lead Time</span><i class="ti ti-calendar-event" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">4.00d</div>
                            <div class="kpi-subtext">Dispatch to delivery</div>
                        </div>
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header"><span class="kpi-title">In-Transit Parcels</span><i class="ti ti-truck-delivery" style="color: var(--orange);"></i></div>
                            <div class="kpi-value">14,210</div>
                            <div class="kpi-subtext">Active carrier pipeline</div>
                        </div>
                        <div class="kpi-card accent-yellow">
                            <div class="kpi-header"><span class="kpi-title">Awaiting Fulfillment</span><i class="ti ti-progress" style="color: var(--yellow);"></i></div>
                            <div class="kpi-value">4,832</div>
                            <div class="kpi-subtext">Orders in Processing state</div>
                        </div>
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header"><span class="kpi-title">Store Stockout Risk SKUs</span><i class="ti ti-alert-triangle" style="color: var(--pink);"></i></div>
                            <div class="kpi-value">595</div>
                            <div class="kpi-subtext">&le; reorder threshold</div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-truck" style="color: var(--cyan);"></i> Courier Volume &amp; SLA On-Time Rate (%)</span>
                            </div>
                            <div id="chart-courier-sla"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-map" style="color: var(--purple);"></i> Delivery SLA % by Geographic Region</span>
                            </div>
                            <div id="chart-region-sla"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 4. COMMERCIAL SALES PERFORMANCE DASHBOARD                 -->
                <!-- ========================================================= -->
                <div id="tab-sales" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Commercial Sales Performance Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Net Delivered Revenue, Category Margins, Discount Absorption &amp; Brand League Tables
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Delivered Commercial Sales</span><i class="ti ti-cash" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">₹676.95 Cr</div>
                            <div class="kpi-subtext">82,540 fulfilled orders</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Gross Catalog Value</span><i class="ti ti-tags" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">₹701.23 Cr</div>
                            <div class="kpi-subtext">Pre-discount order book</div>
                        </div>
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header"><span class="kpi-title">Absorbed Discounts</span><i class="ti ti-discount-2" style="color: var(--orange);"></i></div>
                            <div class="kpi-value">₹24.27 Cr</div>
                            <div class="kpi-subtext">3.46% markdown rate</div>
                        </div>
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header"><span class="kpi-title">Average Order Value (AOV)</span><i class="ti ti-receipt" style="color: var(--pink);"></i></div>
                            <div class="kpi-value">₹82,015.22</div>
                            <div class="kpi-subtext">Per delivered invoice</div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-category" style="color: var(--purple);"></i> Category Net Sales &amp; Margin (%)</span>
                            </div>
                            <div id="chart-sales-category"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-trending-up" style="color: var(--cyan);"></i> Monthly Net Sales Velocity (₹ Cr)</span>
                            </div>
                            <div id="chart-sales-trend"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 5. CUSTOMER RFM & RETENTION DASHBOARD                     -->
                <!-- ========================================================= -->
                <div id="tab-customers" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Customer RFM &amp; Retention Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Behavioral RFM Segmentation, Cohort Retention Curves, Loyalty Spending &amp; Churn Risk
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header"><span class="kpi-title">Registered Master Accounts</span><i class="ti ti-users" style="color: var(--pink);"></i></div>
                            <div class="kpi-value">50,000</div>
                            <div class="kpi-subtext">Total database master records</div>
                        </div>
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Transacting Buyers</span><i class="ti ti-shopping-bag" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">40,380</div>
                            <div class="kpi-subtext">80.8% buyer penetration</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Repeat Buyer Rate</span><i class="ti ti-repeat" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">64.2%</div>
                            <div class="kpi-subtext">&gt; 1 completed order</div>
                        </div>
                        <div class="kpi-card accent-yellow">
                            <div class="kpi-header"><span class="kpi-title">At-Risk VIP Accounts</span><i class="ti ti-user-x" style="color: var(--yellow);"></i></div>
                            <div class="kpi-value">6,518</div>
                            <div class="kpi-subtext">₹128.2 Cr revenue exposure</div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-pie-chart" style="color: var(--pink);"></i> Behavioral RFM Customer Distribution</span>
                            </div>
                            <div id="chart-rfm-distribution"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-chart-line" style="color: var(--cyan);"></i> Monthly Cohort Retention Rates (%)</span>
                            </div>
                            <div id="chart-customer-retention"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 6. STORE INVENTORY & OPERATIONS DASHBOARD                 -->
                <!-- ========================================================= -->
                <div id="tab-operations" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Store Inventory &amp; Operations Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Shelf Stock Health, Stockout Vulnerability, Manufacturing Quality &amp; Factory Scrap Rates
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <a href="./project_documents/documentation/RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Active Shelf Slots</span><i class="ti ti-building-store" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">114,153</div>
                            <div class="kpi-subtext">Store-SKU tracking positions</div>
                        </div>
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header"><span class="kpi-title">Zero-Stock Stockouts</span><i class="ti ti-alert-octagon" style="color: var(--orange);"></i></div>
                            <div class="kpi-value">595</div>
                            <div class="kpi-subtext">0.52% out-of-stock rate</div>
                        </div>
                        <div class="kpi-card accent-yellow">
                            <div class="kpi-header"><span class="kpi-title">Low-Stock Triggers</span><i class="ti ti-bell-ringing" style="color: var(--yellow);"></i></div>
                            <div class="kpi-value">16,880</div>
                            <div class="kpi-subtext">Inventory &le; reorder point</div>
                        </div>
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header"><span class="kpi-title">Factory Scrap Rate</span><i class="ti ti-tool" style="color: var(--pink);"></i></div>
                            <div class="kpi-value">2.54%</div>
                            <div class="kpi-subtext">640,075 scrap units produced</div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-chart-bar" style="color: var(--cyan);"></i> Store Inventory Health Distribution</span>
                            </div>
                            <div id="chart-ops-health"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-activity-heartbeat" style="color: var(--orange);"></i> Manufacturing Floor Scrap Rate by Line (%)</span>
                            </div>
                            <div id="chart-ops-scrap"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 7. HUMAN RESOURCES WORKFORCE DASHBOARD                    -->
                <!-- ========================================================= -->
                <div id="tab-hr" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Human Resources Workforce Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Departmental Headcount, Compensation Structures, Shift Compliance &amp; Talent Attrition
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Active Headcount</span><i class="ti ti-users-group" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">3,000</div>
                            <div class="kpi-subtext">Across 10 corporate departments</div>
                        </div>
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Monthly Base Payroll</span><i class="ti ti-credit-card" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">₹18.98 Cr</div>
                            <div class="kpi-subtext">Contractual fixed compensation</div>
                        </div>
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header"><span class="kpi-title">Average Monthly Salary</span><i class="ti ti-currency-rupee" style="color: var(--pink);"></i></div>
                            <div class="kpi-value">₹63,267</div>
                            <div class="kpi-subtext">Median salary: ₹55,000</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Shift Compliance</span><i class="ti ti-checks" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">94.6%</div>
                            <div class="kpi-subtext">Store floor staffing adherence</div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-chart-pie" style="color: var(--cyan);"></i> Headcount by Corporate Department</span>
                            </div>
                            <div id="chart-hr-headcount"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-chart-bar" style="color: var(--purple);"></i> Monthly Payroll Expenditure by Department (₹ Lakhs)</span>
                            </div>
                            <div id="chart-hr-payroll"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 8. FINANCIAL LEDGER & TREASURY DASHBOARD                  -->
                <!-- ========================================================= -->
                <div id="tab-finance" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Financial Ledger &amp; Treasury Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Revenue Waterfall, Store vs Corporate Operating Expenses, Contribution Margin &amp; Payment Settlement Rails
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <a href="./project_documents/documentation/RetailMart_V3_HR_Finance_Deliverable.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Domain Deliverable (PDF)
                            </a>
                        </div>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Delivered Net Revenue</span><i class="ti ti-chart-arrows" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">₹676.95 Cr</div>
                            <div class="kpi-subtext">82,540 fulfilled invoices</div>
                        </div>
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header"><span class="kpi-title">Store OPEX</span><i class="ti ti-building-store" style="color: var(--orange);"></i></div>
                            <div class="kpi-value">₹38.80 Cr</div>
                            <div class="kpi-subtext">200 retail branch leases &amp; utilities</div>
                        </div>
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header"><span class="kpi-title">Corporate OPEX</span><i class="ti ti-briefcase" style="color: var(--orange);"></i></div>
                            <div class="kpi-value">₹42.15 Cr</div>
                            <div class="kpi-subtext">Technology, HR &amp; administrative</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Contribution Margin</span><i class="ti ti-percentage" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">30.47%</div>
                            <div class="kpi-subtext">₹206.24 Cr delivered margin</div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-stairs-up" style="color: var(--purple);"></i> Financial Revenue &amp; OPEX Waterfall (₹ Cr)</span>
                            </div>
                            <div id="chart-fin-waterfall"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-credit-card" style="color: var(--cyan);"></i> Payment Rail Volume Distribution (₹ Cr)</span>
                            </div>
                            <div id="chart-fin-rails"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 9. CROSS-FUNCTIONAL HEALTH SCORECARD                      -->
                <!-- ========================================================= -->
                <div id="tab-cross" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Cross-Functional Health Scorecard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Cross-Domain Efficiency Ratios, Marketing-Sales Velocity &amp; Fulfillment Equilibrium
                            </div>
                        </div>
                    </div>

                    <div class="charts-grid-2">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-radar" style="color: var(--purple);"></i> Cross-Domain Performance Index (100 Base)</span>
                            </div>
                            <div id="chart-cross-radar"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title"><i class="ti ti-arrows-exchange" style="color: var(--cyan);"></i> Domain Spending vs Net Value Generated</span>
                            </div>
                            <div id="chart-cross-scatter"></div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 10. EXECUTIVE SYNTHESIS & SCORECARD                       -->
                <!-- ========================================================= -->
                <div id="tab-executive" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Executive Summary &amp; Enterprise Governance</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Cross-Domain KPI Scorecard, Strategic Synthesis &amp; 90-Day Action Directives
                            </div>
                        </div>
                        <a href="./project_documents/documentation/RetailMart_V3_Executive_Insights_Report.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                            <i class="ti ti-file-type-pdf"></i> Executive Insights Report (PDF)
                        </a>
                    </div>

                    <div class="kpi-grid">
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header"><span class="kpi-title">Total Enterprise Sales</span><i class="ti ti-cash" style="color: var(--purple);"></i></div>
                            <div class="kpi-value">₹676.95 Cr</div>
                            <div class="kpi-subtext">82,540 fulfilled invoices</div>
                        </div>
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header"><span class="kpi-title">Active Transacting Buyers</span><i class="ti ti-user-check" style="color: var(--cyan);"></i></div>
                            <div class="kpi-value">40,380</div>
                            <div class="kpi-subtext">80.8% buyer penetration</div>
                        </div>
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header"><span class="kpi-title">Carrier On-Time SLA</span><i class="ti ti-truck" style="color: var(--pink);"></i></div>
                            <div class="kpi-value">79.8%</div>
                            <div class="kpi-subtext">4.00 days mean transit</div>
                        </div>
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header"><span class="kpi-title">Total Operating OPEX</span><i class="ti ti-building" style="color: var(--orange);"></i></div>
                            <div class="kpi-value">₹80.95 Cr</div>
                            <div class="kpi-subtext">Store leases, corporate &amp; payroll</div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 11. SCENARIO SIMULATOR (WHAT-IF LEVERS)                   -->
                <!-- ========================================================= -->
                <div id="tab-simulator" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Enterprise Scenario Simulator (What-If Levers)</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Real-Time Financial Sensitivity Analysis, Price Realization, Returns Reduction &amp; Working Capital Modeling
                            </div>
                        </div>
                    </div>

                    <!-- Simulator Levers -->
                    <div class="slider-grid">
                        <div class="slider-group">
                            <div class="slider-label">
                                <span>Price Realization Rate</span>
                                <span id="label-price" style="color: var(--purple);">+0.0%</span>
                            </div>
                            <input type="range" id="sim-price" min="-5" max="10" step="0.5" value="0" oninput="runSimulation()">
                            <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.3rem;">
                                <span>-5%</span><span>Baseline (0%)</span><span>+10%</span>
                            </div>
                        </div>

                        <div class="slider-group">
                            <div class="slider-label">
                                <span>Return Rate Reduction</span>
                                <span id="label-returns" style="color: var(--cyan);">0%</span>
                            </div>
                            <input type="range" id="sim-returns" min="-50" max="0" step="5" value="0" oninput="runSimulation()">
                            <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.3rem;">
                                <span>-50% (Max Quality)</span><span>Baseline</span><span>0%</span>
                            </div>
                        </div>

                        <div class="slider-group">
                            <div class="slider-label">
                                <span>Volume Expansion</span>
                                <span id="label-volume" style="color: var(--pink);">+0.0%</span>
                            </div>
                            <input type="range" id="sim-volume" min="-20" max="25" step="1" value="0" oninput="runSimulation()">
                            <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.3rem;">
                                <span>-20%</span><span>Baseline</span><span>+25%</span>
                            </div>
                        </div>

                        <div class="slider-group">
                            <div class="slider-label">
                                <span>Store OpEx Rationalization</span>
                                <span id="label-opex" style="color: var(--orange);">0%</span>
                            </div>
                            <input type="range" id="sim-opex" min="-15" max="15" step="1" value="0" oninput="runSimulation()">
                            <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.3rem;">
                                <span>-15% (Lean)</span><span>Baseline</span><span>+15%</span>
                            </div>
                        </div>
                    </div>

                    <!-- Simulation Result Table -->
                    <div class="action-card">
                        <div class="action-header">
                            <h3 style="font-size: 1rem; font-weight: 600; color: var(--text-white);">
                                <i class="ti ti-calculator" style="color: var(--purple);"></i> Simulated Enterprise Financial Impact
                            </h3>
                        </div>
                        <table class="action-table">
                            <thead>
                                <tr>
                                    <th>Financial Metric</th>
                                    <th>Baseline Actuals</th>
                                    <th>Simulated Forecast</th>
                                    <th>Variance (₹ Shift)</th>
                                    <th>Strategic Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Delivered Commercial Revenue</strong></td>
                                    <td>₹676.95 Cr</td>
                                    <td id="res-rev" style="color: var(--cyan); font-weight: 700;">₹676.95 Cr</td>
                                    <td id="res-rev-var" style="color: var(--text-muted);">₹0.00 Cr</td>
                                    <td><span class="status-badge badge-neutral">Parity</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Delivered Contribution Margin</strong></td>
                                    <td>₹206.24 Cr (30.47%)</td>
                                    <td id="res-margin" style="color: #34D399; font-weight: 700;">₹206.24 Cr (30.47%)</td>
                                    <td id="res-margin-var" style="color: #34D399; font-weight: 600;">+₹0.00 Cr</td>
                                    <td><span class="status-badge badge-success">Optimized</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

            </main>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="toast-notify">
        <i class="ti ti-circle-check" style="color: var(--cyan); font-size: 1.25rem;"></i>
        <span id="toast-text">Filters Applied: Synchronized live view</span>
    </div>

    <!-- Interactive Scripts & ApexCharts Initializers -->
    <script>
        // Tab switching logic
        function switchTab(tabId) {
            // Update tabs
            document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
            const targetPane = document.getElementById('tab-' + tabId);
            if (targetPane) targetPane.classList.add('active');

            // Update nav active classes
            document.querySelectorAll('.nav-tab-link').forEach(el => el.classList.remove('active'));
            const targetBtn = document.getElementById('nav-' + tabId);
            if (targetBtn) targetBtn.classList.add('active');

            // Trigger window resize so ApexCharts correctly size
            window.dispatchEvent(new Event('resize'));
        }

        // Deliverables Dropdown toggle
        function toggleDeliverablesDropdown() {
            const menu = document.getElementById('reports-dropdown-menu');
            if (menu) {
                menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
            }
        }
        document.addEventListener('click', function(e) {
            const btn = document.getElementById('reports-dropdown-btn');
            const menu = document.getElementById('reports-dropdown-menu');
            if (btn && menu && !btn.contains(e.target) && !menu.contains(e.target)) {
                menu.style.display = 'none';
            }
        });

        // Quick Presets
        function applyDatePreset(preset) {
            document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
            const startInput = document.getElementById('filter-start-date');
            const endInput = document.getElementById('filter-end-date');

            if (preset === 'all') {
                document.getElementById('preset-all').classList.add('active');
                startInput.value = '2024-01-01';
                endInput.value = '2026-02-26';
            } else if (preset === '2025') {
                document.getElementById('preset-2025').classList.add('active');
                startInput.value = '2025-01-01';
                endInput.value = '2025-12-31';
            } else if (preset === '90d') {
                document.getElementById('preset-90d').classList.add('active');
                startInput.value = '2025-11-28';
                endInput.value = '2026-02-26';
            } else if (preset === '30d') {
                document.getElementById('preset-30d').classList.add('active');
                startInput.value = '2026-01-27';
                endInput.value = '2026-02-26';
            }
            showToast('Date preset activated: ' + startInput.value + ' to ' + endInput.value);
        }

        // Handle Apply Filters
        function handleApplyFilters(e) {
            e.preventDefault();
            const start = document.getElementById('filter-start-date').value;
            const end = document.getElementById('filter-end-date').value;
            const region = document.getElementById('filter-region');
            const regionText = region.options[region.selectedIndex].text;

            const windowTag = document.getElementById('mkt-window-tag');
            if (windowTag) windowTag.innerText = start + ' to ' + end;

            showToast('Filters Applied: Scope ' + regionText + ' · Window ' + start + ' to ' + end);
        }

        // Handle Reset Filters
        function handleResetFilters() {
            document.getElementById('filter-start-date').value = '2024-01-01';
            document.getElementById('filter-end-date').value = '2026-02-26';
            document.getElementById('filter-region').selectedIndex = 0;
            document.getElementById('filter-store').selectedIndex = 0;
            document.getElementById('filter-department').selectedIndex = 0;
            document.getElementById('filter-expense-cat').selectedIndex = 0;

            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('preset-all').classList.add('active');

            const windowTag = document.getElementById('mkt-window-tag');
            if (windowTag) windowTag.innerText = '2024-01-01 to 2026-02-26';

            showToast('Filters reset to default 2024-2026 enterprise baseline');
        }

        function handleRegionChange() {
            // Cascading store update feedback
            const regionSelect = document.getElementById('filter-region');
            const storeSelect = document.getElementById('filter-store');
            if (regionSelect.value !== "") {
                storeSelect.options[0].text = "Filtered Stores in Selected Region";
            } else {
                storeSelect.options[0].text = "All Stores (200)";
            }
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            const text = document.getElementById('toast-text');
            text.innerText = msg;
            toast.style.display = 'flex';
            setTimeout(() => { toast.style.display = 'none'; }, 3500);
        }

        function simulateLogout() {
            showToast('Session preserved · Standing in Demo Mode');
        }

        // What-if scenario calculator
        function runSimulation() {
            const price = parseFloat(document.getElementById('sim-price').value);
            const returns = parseFloat(document.getElementById('sim-returns').value);
            const volume = parseFloat(document.getElementById('sim-volume').value);
            const opex = parseFloat(document.getElementById('sim-opex').value);

            document.getElementById('label-price').innerText = (price >= 0 ? '+' : '') + price.toFixed(1) + '%';
            document.getElementById('label-returns').innerText = returns.toFixed(0) + '%';
            document.getElementById('label-volume').innerText = (volume >= 0 ? '+' : '') + volume.toFixed(1) + '%';
            document.getElementById('label-opex').innerText = (opex >= 0 ? '+' : '') + opex.toFixed(1) + '%';

            const baseRev = 676.95;
            const baseMargin = 206.24;

            const simRev = baseRev * (1 + volume/100) * (1 + price/100);
            const incrementalMargin = (simRev - baseRev) * 0.40 - (returns * 0.4) - (opex * 0.3);
            const simMargin = baseMargin + incrementalMargin;
            const marginPct = (simMargin / simRev) * 100;

            document.getElementById('res-rev').innerText = '₹' + simRev.toFixed(2) + ' Cr';
            const revVar = simRev - baseRev;
            document.getElementById('res-rev-var').innerText = (revVar >= 0 ? '+' : '') + '₹' + revVar.toFixed(2) + ' Cr';

            document.getElementById('res-margin').innerText = '₹' + simMargin.toFixed(2) + ' Cr (' + marginPct.toFixed(2) + '%)';
            const marginVar = simMargin - baseMargin;
            document.getElementById('res-margin-var').innerText = (marginVar >= 0 ? '+' : '') + '₹' + marginVar.toFixed(2) + ' Cr';
        }

        // Initialize ApexCharts on DOM load
        document.addEventListener('DOMContentLoaded', function() {
            // 1. Marketing Platform Spend Donut
            new ApexCharts(document.querySelector("#chart-platform-spend"), {
                series: [2194510.82, 2070878.68, 2019363.38, 1957549.14, 2060572.39],
                chart: { type: 'donut', height: 280, background: 'transparent' },
                labels: ['Facebook', 'Google', 'Twitter', 'LinkedIn', 'Instagram'],
                colors: ['#A459D0', '#2CD4E1', '#E88E3E', '#FFBD4A', '#E95B9F'],
                stroke: { colors: ['#183A5F'], width: 2 },
                dataLabels: {
                    enabled: true,
                    formatter: function(val) { return val.toFixed(1) + '%'; },
                    style: { fontFamily: 'Inter', fontSize: '11px', fontWeight: 600 }
                },
                legend: { position: 'bottom', labels: { colors: '#D5DCE5' }, fontFamily: 'Inter' },
                tooltip: { theme: 'dark', y: { formatter: function(v) { return '₹' + Number(v).toLocaleString(); } } }
            }).render();

            // 2. Marketing Monthly Spend Trajectory
            new ApexCharts(document.querySelector("#chart-spend-trend"), {
                series: [
                    { name: 'Facebook', data: [79541, 88430, 93615, 80795, 101854, 98450, 71596, 82180, 87859, 99515, 68352, 92514, 82965, 78231] },
                    { name: 'Google', data: [82100, 75400, 89200, 91500, 85600, 94200, 68500, 79200, 84300, 91200, 74500, 88900, 79400, 81500] },
                    { name: 'Twitter', data: [68900, 71200, 84500, 78900, 76500, 81200, 74500, 71800, 79500, 84200, 69800, 78400, 76200, 79400] },
                    { name: 'LinkedIn', data: [74500, 78900, 81200, 76500, 89400, 82100, 69800, 74500, 78200, 81500, 71200, 76500, 81200, 74500] },
                    { name: 'Instagram', data: [76500, 81200, 79500, 84200, 78900, 89400, 71200, 76500, 81200, 88900, 74500, 82100, 78900, 84200] }
                ],
                chart: { type: 'bar', stacked: true, height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#A459D0', '#2CD4E1', '#E88E3E', '#FFBD4A', '#E95B9F'],
                xaxis: {
                    categories: ['Jan 24', 'Mar 24', 'May 24', 'Jul 24', 'Sep 24', 'Nov 24', 'Jan 25', 'Mar 25', 'May 25', 'Jul 25', 'Sep 25', 'Nov 25', 'Jan 26', 'Feb 26'],
                    labels: { style: { colors: '#6F8298', fontFamily: 'Inter', fontSize: '10px' }, rotate: -45 }
                },
                yaxis: {
                    labels: { style: { colors: '#6F8298', fontFamily: 'Inter' }, formatter: function(v) { return '₹' + (v/1000).toFixed(0) + 'k'; } }
                },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                legend: { position: 'top', labels: { colors: '#D5DCE5' }, fontFamily: 'Inter' },
                tooltip: { theme: 'dark', y: { formatter: function(v) { return '₹' + Number(v).toLocaleString(); } } }
            }).render();

            // 3. Email Engagement
            new ApexCharts(document.querySelector("#chart-email-trend"), {
                series: [
                    { name: 'Open Rate (%)', data: [31.2, 29.8, 30.5, 32.1, 28.9, 30.4, 31.8, 30.2, 29.5, 30.9, 31.5, 29.8, 30.1, 30.2] },
                    { name: 'Click Rate (%)', data: [23.5, 22.1, 22.8, 24.2, 21.9, 23.1, 23.8, 22.9, 21.8, 23.4, 23.9, 22.4, 22.7, 22.9] }
                ],
                chart: { type: 'line', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                stroke: { width: [3, 3], curve: 'smooth' },
                colors: ['#2CD4E1', '#A459D0'],
                xaxis: {
                    categories: ['Jan 24', 'Mar 24', 'May 24', 'Jul 24', 'Sep 24', 'Nov 24', 'Jan 25', 'Mar 25', 'May 25', 'Jul 25', 'Sep 25', 'Nov 25', 'Jan 26', 'Feb 26'],
                    labels: { style: { colors: '#6F8298', fontFamily: 'Inter', fontSize: '10px' }, rotate: -45 }
                },
                yaxis: { max: 50, labels: { style: { colors: '#6F8298', fontFamily: 'Inter' }, formatter: function(v) { return v.toFixed(0) + '%'; } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                legend: { position: 'top', labels: { colors: '#D5DCE5' }, fontFamily: 'Inter' },
                tooltip: { theme: 'dark' }
            }).render();

            // 4. Campaign Pacing Top 10
            new ApexCharts(document.querySelector("#chart-campaign-pacing"), {
                series: [
                    { name: 'Realized Spend', data: [425890, 382150, 294600, 248320, 198740, 175400, 154200, 142100, 128900, 115400] },
                    { name: 'Authorized Budget', data: [1850000, 1500000, 1200000, 950000, 800000, 750000, 650000, 600000, 550000, 500000] }
                ],
                chart: { type: 'bar', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                plotOptions: { bar: { horizontal: true, barHeight: '55%' } },
                colors: ['#E88E3E', '#24598A'],
                xaxis: { labels: { style: { colors: '#6F8298', fontFamily: 'Inter' }, formatter: function(v) { return '₹' + (v/1000).toFixed(0) + 'k'; } } },
                yaxis: {
                    categories: ['Diwali 2025', 'Tech Fest 24', 'Republic Day', 'Summer Kitchen', 'Footwear Blitz', 'Fashion Sprint', 'Mobile Launch', 'Apparel Gala', 'Home Makeover', 'Fitness Week'],
                    labels: { style: { colors: '#D5DCE5', fontFamily: 'Inter', fontSize: '10px' } }
                },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                legend: { position: 'top', labels: { colors: '#D5DCE5' }, fontFamily: 'Inter' },
                tooltip: { theme: 'dark' }
            }).render();

            // 5. Digital Device / OS
            new ApexCharts(document.querySelector("#chart-device-os"), {
                series: [59.9, 29.8, 10.3],
                chart: { type: 'donut', height: 280, background: 'transparent' },
                labels: ['Mobile (Android & iOS)', 'Desktop (Windows & macOS)', 'Tablet (iPad & Other)'],
                colors: ['#2CD4E1', '#A459D0', '#FFBD4A'],
                stroke: { colors: ['#183A5F'], width: 2 },
                dataLabels: { enabled: true, formatter: function(val) { return val.toFixed(1) + '%'; }, style: { fontFamily: 'Inter', fontSize: '11px', fontWeight: 600 } },
                legend: { position: 'bottom', labels: { colors: '#D5DCE5' }, fontFamily: 'Inter' },
                tooltip: { theme: 'dark' }
            }).render();

            // 6. Digital Traffic Trend
            new ApexCharts(document.querySelector("#chart-traffic-trend"), {
                series: [
                    { name: 'Page Views', data: [32000, 35000, 38000, 41000, 39000, 42000, 44000, 41000, 39500, 43000, 45000, 41500, 42000, 44000] },
                    { name: 'Sessions', data: [6800, 7200, 7600, 8100, 7900, 8400, 8700, 8200, 7900, 8600, 8900, 8300, 8400, 8800] }
                ],
                chart: { type: 'area', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#E95B9F', '#2CD4E1'],
                stroke: { width: [2, 2], curve: 'smooth' },
                xaxis: {
                    categories: ['Jan 24', 'Mar 24', 'May 24', 'Jul 24', 'Sep 24', 'Nov 24', 'Jan 25', 'Mar 25', 'May 25', 'Jul 25', 'Sep 25', 'Nov 25', 'Jan 26', 'Feb 26'],
                    labels: { style: { colors: '#6F8298', fontSize: '10px' }, rotate: -45 }
                },
                yaxis: { labels: { style: { colors: '#6F8298' } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                legend: { position: 'top', labels: { colors: '#D5DCE5' } },
                tooltip: { theme: 'dark' }
            }).render();

            // 7. Logistics Courier SLA
            new ApexCharts(document.querySelector("#chart-courier-sla"), {
                series: [
                    { name: 'Delivered Parcels', type: 'column', data: [24500, 21800, 18900, 10200, 7140] },
                    { name: 'On-Time SLA %', type: 'line', data: [84.2, 81.5, 78.9, 74.2, 71.8] }
                ],
                chart: { height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#2CD4E1', '#A459D0'],
                stroke: { width: [0, 3] },
                xaxis: { categories: ['BlueDart', 'Delhivery', 'EcomExpress', 'Shadowfax', 'XpressBees'], labels: { style: { colors: '#D5DCE5' } } },
                yaxis: [
                    { labels: { style: { colors: '#6F8298' }, formatter: function(v) { return (v/1000).toFixed(0) + 'k'; } } },
                    { opposite: true, max: 100, labels: { style: { colors: '#6F8298' }, formatter: function(v) { return v + '%'; } } }
                ],
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                legend: { position: 'top', labels: { colors: '#D5DCE5' } },
                tooltip: { theme: 'dark' }
            }).render();

            // 8. Logistics Regional SLA
            new ApexCharts(document.querySelector("#chart-region-sla"), {
                series: [{ name: 'On-Time SLA %', data: [83.4, 81.8, 80.2, 77.5, 76.1] }],
                chart: { type: 'bar', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#38BDF8'],
                xaxis: { categories: ['Western Hub', 'Northern NCR', 'Southern Tech', 'Central Hub', 'Eastern Coastal'], labels: { style: { colors: '#D5DCE5' } } },
                yaxis: { max: 100, labels: { style: { colors: '#6F8298' }, formatter: function(v) { return v + '%'; } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                tooltip: { theme: 'dark' }
            }).render();

            // 9. Sales Category
            new ApexCharts(document.querySelector("#chart-sales-category"), {
                series: [{ name: 'Net Revenue (₹ Cr)', data: [284.15, 148.90, 115.40, 82.50, 46.00] }],
                chart: { type: 'bar', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#A459D0'],
                xaxis: { categories: ['Electronics', 'Fashion & Apparel', 'Home & Kitchen', 'Grocery & Staples', 'Beauty & Personal'], labels: { style: { colors: '#D5DCE5' } } },
                yaxis: { labels: { style: { colors: '#6F8298' }, formatter: function(v) { return '₹' + v + 'Cr'; } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                tooltip: { theme: 'dark' }
            }).render();

            // 10. Sales Trend
            new ApexCharts(document.querySelector("#chart-sales-trend"), {
                series: [{ name: 'Delivered Net Sales', data: [42.1, 45.8, 48.3, 51.2, 49.6, 53.4, 55.8, 52.1, 50.4, 54.2, 57.1, 52.9, 53.8, 56.2] }],
                chart: { type: 'line', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#2CD4E1'],
                stroke: { width: 3, curve: 'smooth' },
                xaxis: {
                    categories: ['Jan 24', 'Mar 24', 'May 24', 'Jul 24', 'Sep 24', 'Nov 24', 'Jan 25', 'Mar 25', 'May 25', 'Jul 25', 'Sep 25', 'Nov 25', 'Jan 26', 'Feb 26'],
                    labels: { style: { colors: '#6F8298', fontSize: '10px' }, rotate: -45 }
                },
                yaxis: { labels: { style: { colors: '#6F8298' }, formatter: function(v) { return '₹' + v + 'Cr'; } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                tooltip: { theme: 'dark' }
            }).render();

            // 11. Customer RFM Distribution
            new ApexCharts(document.querySelector("#chart-rfm-distribution"), {
                series: [8885, 11240, 7420, 6518, 6317],
                chart: { type: 'pie', height: 280, background: 'transparent' },
                labels: ['Champions (₹234.8 Cr)', 'Loyal Customers (₹189.2 Cr)', 'Potential Loyalists (₹84.1 Cr)', 'At Risk (₹128.2 Cr)', 'Hibernating (₹40.6 Cr)'],
                colors: ['#34D399', '#2CD4E1', '#A459D0', '#FFBD4A', '#E88E3E'],
                stroke: { colors: ['#183A5F'], width: 2 },
                dataLabels: { enabled: true, formatter: function(val) { return val.toFixed(1) + '%'; }, style: { fontFamily: 'Inter', fontSize: '11px', fontWeight: 600 } },
                legend: { position: 'bottom', labels: { colors: '#D5DCE5' }, fontFamily: 'Inter' },
                tooltip: { theme: 'dark' }
            }).render();

            // 12. Customer Retention
            new ApexCharts(document.querySelector("#chart-customer-retention"), {
                series: [{ name: 'Repeat Order Retention %', data: [100, 78.4, 69.2, 64.2, 59.8, 55.4] }],
                chart: { type: 'area', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#E95B9F'],
                xaxis: { categories: ['Month 0', 'Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5'], labels: { style: { colors: '#D5DCE5' } } },
                yaxis: { max: 100, labels: { style: { colors: '#6F8298' }, formatter: function(v) { return v + '%'; } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                tooltip: { theme: 'dark' }
            }).render();

            // 13. Operations Stock Health
            new ApexCharts(document.querySelector("#chart-ops-health"), {
                series: [84.6, 14.8, 0.52],
                chart: { type: 'donut', height: 280, background: 'transparent' },
                labels: ['Optimal Stock (96,678 slots)', 'Low Stock Trigger (16,880 slots)', 'Zero-Stock Stockout (595 slots)'],
                colors: ['#10B981', '#FFBD4A', '#F43F5E'],
                stroke: { colors: ['#183A5F'], width: 2 },
                dataLabels: { enabled: true, formatter: function(val) { return val.toFixed(1) + '%'; }, style: { fontFamily: 'Inter', fontSize: '11px', fontWeight: 600 } },
                legend: { position: 'bottom', labels: { colors: '#D5DCE5' } },
                tooltip: { theme: 'dark' }
            }).render();

            // 14. Operations Scrap Rates
            new ApexCharts(document.querySelector("#chart-ops-scrap"), {
                series: [{ name: 'Scrap Rate %', data: [1.8, 2.1, 1.9, 2.4, 3.8, 2.2, 1.7, 2.3, 3.6, 2.0] }],
                chart: { type: 'bar', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#E88E3E'],
                xaxis: { categories: ['Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5 (QA)', 'Line 6', 'Line 7', 'Line 8', 'Line 9 (QA)', 'Line 10'], labels: { style: { colors: '#D5DCE5' } } },
                yaxis: { labels: { style: { colors: '#6F8298' }, formatter: function(v) { return v + '%'; } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                tooltip: { theme: 'dark' }
            }).render();

            // 15. HR Headcount
            new ApexCharts(document.querySelector("#chart-hr-headcount"), {
                series: [850, 620, 480, 310, 240, 190, 130, 90, 50, 40],
                chart: { type: 'donut', height: 280, background: 'transparent' },
                labels: ['Operations', 'Sales', 'Logistics', 'Customer Support', 'IT & Tech', 'Marketing', 'Finance', 'Procurement', 'HR', 'Legal'],
                colors: ['#2CD4E1', '#A459D0', '#34D399', '#E88E3E', '#E95B9F', '#FFBD4A', '#38BDF8', '#C084FC', '#F43F5E', '#94A3B8'],
                stroke: { colors: ['#183A5F'], width: 2 },
                dataLabels: { enabled: true, formatter: function(val) { return val.toFixed(1) + '%'; }, style: { fontFamily: 'Inter', fontSize: '11px', fontWeight: 600 } },
                legend: { position: 'bottom', labels: { colors: '#D5DCE5' } },
                tooltip: { theme: 'dark' }
            }).render();

            // 16. HR Payroll
            new ApexCharts(document.querySelector("#chart-hr-payroll"), {
                series: [{ name: 'Monthly Payroll (₹ Lakhs)', data: [485, 392, 315, 218, 198, 142, 98, 62, 38, 32] }],
                chart: { type: 'bar', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#A459D0'],
                xaxis: { categories: ['Operations', 'Sales', 'Logistics', 'IT & Tech', 'Support', 'Marketing', 'Finance', 'Procurement', 'HR', 'Legal'], labels: { style: { colors: '#D5DCE5', fontSize: '10px' } } },
                yaxis: { labels: { style: { colors: '#6F8298' } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                tooltip: { theme: 'dark' }
            }).render();

            // 17. Finance Waterfall
            new ApexCharts(document.querySelector("#chart-fin-waterfall"), {
                series: [{
                    data: [
                        { x: 'Net Revenue', y: 676.95 },
                        { x: 'COGS', y: -418.84 },
                        { x: 'Gross Margin', y: 258.11 },
                        { x: 'Store OPEX', y: -38.80 },
                        { x: 'Corp OPEX', y: -42.15 },
                        { x: 'Operating EBIT', y: 177.16 }
                    ]
                }],
                chart: { type: 'bar', height: 280, background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                plotOptions: { bar: { columnWidth: '55%' } },
                colors: ['#2CD4E1'],
                xaxis: { labels: { style: { colors: '#D5DCE5', fontSize: '10px' } } },
                yaxis: { labels: { style: { colors: '#6F8298' }, formatter: function(v) { return '₹' + v.toFixed(0) + 'Cr'; } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                tooltip: { theme: 'dark' }
            }).render();

            // 18. Finance Settlement Rails
            new ApexCharts(document.querySelector("#chart-fin-rails"), {
                series: [312.40, 241.10, 92.50, 55.23],
                chart: { type: 'pie', height: 280, background: 'transparent' },
                labels: ['UPI Rails (₹312.4 Cr)', 'Card Gateways (₹241.1 Cr)', 'Net Banking (₹92.5 Cr)', 'Cash on Delivery (₹55.2 Cr)'],
                colors: ['#34D399', '#A459D0', '#2CD4E1', '#E88E3E'],
                stroke: { colors: ['#183A5F'], width: 2 },
                dataLabels: { enabled: true, formatter: function(val) { return val.toFixed(1) + '%'; }, style: { fontFamily: 'Inter', fontSize: '11px', fontWeight: 600 } },
                legend: { position: 'bottom', labels: { colors: '#D5DCE5' } },
                tooltip: { theme: 'dark' }
            }).render();

            // 19. Cross Functional Radar
            new ApexCharts(document.querySelector("#chart-cross-radar"), {
                series: [{ name: 'Enterprise Domain Index', data: [92, 85, 80, 88, 95, 91] }],
                chart: { height: 280, type: 'radar', background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#A459D0'],
                xaxis: { categories: ['Sales Velocity', 'Customer Loyalty', 'Logistics SLA', 'Inventory Health', 'Financial Health', 'Workforce Staffing'], labels: { style: { colors: '#D5DCE5' } } },
                yaxis: { max: 100, labels: { style: { colors: '#6F8298' } } }
            }).render();

            // 20. Cross Functional Scatter
            new ApexCharts(document.querySelector("#chart-cross-scatter"), {
                series: [
                    { name: 'Marketing ROI', data: [[10.3, 85.4], [12.1, 98.2], [14.5, 112.5], [16.8, 128.9]] },
                    { name: 'Logistics SLA Yield', data: [[8.5, 78.4], [9.2, 81.2], [11.4, 84.5], [13.2, 89.2]] }
                ],
                chart: { height: 280, type: 'scatter', background: 'transparent', toolbar: { show: false } },
                dataLabels: { enabled: false },
                colors: ['#E88E3E', '#2CD4E1'],
                xaxis: { title: { text: 'Domain Operating Spend (₹ Cr)', style: { color: '#8E9BAE' } }, labels: { style: { colors: '#6F8298' } } },
                yaxis: { title: { text: 'Delivered Commercial Yield (₹ Cr)', style: { color: '#8E9BAE' } }, labels: { style: { colors: '#6F8298' } } },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                legend: { position: 'top', labels: { colors: '#D5DCE5' } },
                tooltip: { theme: 'dark' }
            }).render();
        });
    </script>
</body>
</html>
"""

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(SCRIPTS_FILE, 'w', encoding='utf-8') as f:
    f.write(open(__file__, 'r', encoding='utf-8').read())

with open(GITHUB_SCRIPTS_FILE, 'w', encoding='utf-8') as f:
    f.write(open(__file__, 'r', encoding='utf-8').read())

print(f"Successfully generated standalone dashboard at: {INDEX_FILE} (Size: {len(html_content)} bytes)")
