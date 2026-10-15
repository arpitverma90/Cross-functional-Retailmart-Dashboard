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
        .badge-danger {
            background: rgba(244, 63, 94, 0.15);
            color: #F43F5E;
            border: 1px solid rgba(244, 63, 94, 0.3);
        }
        .badge-warning {
            background: rgba(232, 142, 62, 0.15);
            color: #E88E3E;
            border: 1px solid rgba(232, 142, 62, 0.3);
        }

        .kpi-grid-5 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.75rem;
        }
        @media (min-width: 1200px) {
            .kpi-grid-5 {
                grid-template-columns: repeat(5, 1fr);
            }
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
                <button class="nav-tab-link active" id="nav-executive" onclick="switchTab('executive')">
                    <i class="ti ti-layout-dashboard"></i> Executive
                </button>

                <!-- Domain Suite 1: Growth & Supply Chain -->
                <div class="suite-pill suite-1">
                    <span class="suite-tag tag-1">Suite 1</span>
                    <button class="nav-tab-link" id="nav-marketing" onclick="switchTab('marketing')">
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
                <!-- 1. MARKETING INTELLIGENCE DASHBOARD                       -->
                <!-- ========================================================= -->
                <div id="tab-marketing" class="tab-pane">
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
                                <!-- ========================================================= -->
                <!-- 9. CROSS-FUNCTIONAL WORKFORCE & FINANCIAL INSIGHTS         -->
                <!-- ========================================================= -->
                <div id="tab-cross" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Cross-Functional Workforce &amp; Financial Insights</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Workforce Productivity (Revenue/Employee), Labor Cost Ratio, Store Staffing Efficiency &amp; Regional Contribution
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span class="status-badge badge-neutral" style="font-size: 0.72rem; padding: 0.35rem 0.75rem;">
                                <i class="ti ti-arrows-cross"></i> HR-Finance Unified
                            </span>
                            <span class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem;">
                                <i class="ti ti-chart-arrows"></i> CTE Pre-Aggregated
                            </span>
                        </div>
                    </div>

                    <!-- Cross-Functional Headline KPI Cards -->
                    <div class="kpi-grid">
                        <!-- Card 1: Revenue Per Employee -->
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header">
                                <span class="kpi-title">Revenue Per Employee</span>
                                <span class="status-badge badge-success">Productivity</span>
                            </div>
                            <div class="kpi-value">₹22.57 Lakhs</div>
                            <div class="kpi-subtext">
                                <span>Delivered Revenue / 3,000 Headcount</span>
                            </div>
                        </div>

                        <!-- Card 2: Labor Cost to Revenue Ratio -->
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header">
                                <span class="kpi-title">Labor Cost to Revenue Ratio</span>
                                <span class="status-badge badge-neutral">Intensity</span>
                            </div>
                            <div class="kpi-value">2.66%</div>
                            <div class="kpi-subtext">
                                <span>Processed Payroll / Delivered Revenue</span>
                            </div>
                        </div>

                        <!-- Card 3: Delivered Net Revenue -->
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header">
                                <span class="kpi-title">Commercial Delivered Sales</span>
                                <span class="status-badge badge-success">Top-Line</span>
                            </div>
                            <div class="kpi-value">₹676.95 Cr</div>
                            <div class="kpi-subtext">
                                <span>Fulfilled Sales Volume</span>
                            </div>
                        </div>

                        <!-- Card 4: Processed Payroll Outflow -->
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header">
                                <span class="kpi-title">Processed Cash Payroll</span>
                                <span class="status-badge badge-neutral">LTM Payouts</span>
                            </div>
                            <div class="kpi-value">₹18.03 Cr</div>
                            <div class="kpi-subtext">
                                <span>Bank Cleared Compensation</span>
                            </div>
                        </div>

                        <!-- Card 5: Staffing Density -->
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header">
                                <span class="kpi-title">Store Staffing Density</span>
                                <span class="status-badge badge-neutral">Deployment</span>
                            </div>
                            <div class="kpi-value">15.0 Staff</div>
                            <div class="kpi-subtext">
                                <span>Average Employees per Branch</span>
                            </div>
                        </div>

                        <!-- Card 6: Store Operating Expenses -->
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header">
                                <span class="kpi-title">Store Branch OPEX</span>
                                <span class="status-badge badge-neutral">Operating</span>
                            </div>
                            <div class="kpi-value">₹10.04 Cr</div>
                            <div class="kpi-subtext">
                                <span>Branch Non-Payroll Expenses</span>
                            </div>
                        </div>
                    </div>

                    <!-- Charts Row: Monthly Cross-Functional Trajectory & Department Cost Allocation -->
                    <div class="charts-grid-2" style="margin-top: 1.5rem;">
                        <!-- Chart 1: Revenue vs Payroll vs Store OPEX -->
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-chart-line" style="color: var(--purple);"></i>
                                    Monthly Commercial Revenue vs Processed Payroll &amp; Store Costs (₹ Crores)
                                </span>
                                <span style="font-size: 0.72rem; color: var(--text-muted);">
                                    Cross-Domain Monthly Pacing
                                </span>
                            </div>
                            <div id="chart-cross-trajectory" style="min-height: 320px;"></div>
                        </div>

                        <!-- Chart 2: Department Payroll Burden vs Staff Count -->
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-chart-bar" style="color: var(--pink);"></i>
                                    Department Headcount vs Monthly Compensation Outflow (₹ Crores)
                                </span>
                                <span style="font-size: 0.72rem; color: var(--text-muted);">
                                    Organizational Burden
                                </span>
                            </div>
                            <div id="chart-dept-cost" style="min-height: 320px;"></div>
                        </div>
                    </div>

                    <!-- Table 1: Store Staffing Density vs Delivered Revenue & Contribution -->
                    <div class="table-card" style="margin-top: 1.5rem;">
                        <div class="table-header">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <i class="ti ti-building-store" style="color: var(--cyan); font-size: 1.15rem;"></i>
                                <h3 class="table-title">Store Staffing Efficiency: Delivered Sales vs Branch OPEX &amp; Annual Contribution</h3>
                            </div>
                            <span class="kpi-badge badge-neutral" style="font-size: 0.7rem;">Top 25 Representative Branches</span>
                        </div>
                        <div style="overflow-x: auto;">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Store Name</th>
                                        <th>City</th>
                                        <th>Region</th>
                                        <th style="text-align: right;">Staff Headcount</th>
                                        <th style="text-align: right;">Delivered Sales (₹ Cr)</th>
                                        <th style="text-align: right;">Revenue / Staff (₹ L)</th>
                                        <th style="text-align: right;">Store OPEX (₹)</th>
                                        <th style="text-align: right;">Annual Payroll (₹)</th>
                                        <th style="text-align: right;">Annual Contribution (₹ Cr)</th>
                                    </tr>
                                </thead>
                                <tbody>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Raipur</td>
                    <td>Raipur</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹4.26 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹25.06 L</td>
                    <td style="text-align: right; color: var(--orange);">₹459,191</td>
                    <td style="text-align: right; color: var(--text-light);">₹770,589</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹3.29 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Prayagraj</td>
                    <td>Prayagraj</td>
                    <td><span class="status-badge badge-neutral">North East</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹4.08 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹24.00 L</td>
                    <td style="text-align: right; color: var(--orange);">₹430,822</td>
                    <td style="text-align: right; color: var(--text-light);">₹922,812</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.93 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Rourkela</td>
                    <td>Rourkela</td>
                    <td><span class="status-badge badge-neutral">North East</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">13 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹4.06 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹31.25 L</td>
                    <td style="text-align: right; color: var(--orange);">₹582,837</td>
                    <td style="text-align: right; color: var(--text-light);">₹976,847</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.83 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Salem</td>
                    <td>Salem</td>
                    <td><span class="status-badge badge-neutral">North</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">12 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹4.05 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹33.71 L</td>
                    <td style="text-align: right; color: var(--orange);">₹443,022</td>
                    <td style="text-align: right; color: var(--text-light);">₹850,115</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.98 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Amritsar</td>
                    <td>Amritsar</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">18 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹4.02 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹22.36 L</td>
                    <td style="text-align: right; color: var(--orange);">₹485,874</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,490,041</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.19 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Kanpur</td>
                    <td>Kanpur</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹4.00 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹23.54 L</td>
                    <td style="text-align: right; color: var(--orange);">₹582,382</td>
                    <td style="text-align: right; color: var(--text-light);">₹779,142</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹3.01 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Surat</td>
                    <td>Surat</td>
                    <td><span class="status-badge badge-neutral">Central</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">10 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹4.00 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹40.01 L</td>
                    <td style="text-align: right; color: var(--orange);">₹487,999</td>
                    <td style="text-align: right; color: var(--text-light);">₹641,461</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹3.18 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Gaya</td>
                    <td>Gaya</td>
                    <td><span class="status-badge badge-neutral">Central</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.98 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹23.42 L</td>
                    <td style="text-align: right; color: var(--orange);">₹410,785</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,150,499</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.56 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Surat</td>
                    <td>Surat</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.93 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹23.11 L</td>
                    <td style="text-align: right; color: var(--orange);">₹380,040</td>
                    <td style="text-align: right; color: var(--text-light);">₹900,528</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.81 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Pune</td>
                    <td>Pune</td>
                    <td><span class="status-badge badge-neutral">North East</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">18 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.92 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹21.77 L</td>
                    <td style="text-align: right; color: var(--orange);">₹481,096</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,014,507</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.65 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Panaji</td>
                    <td>Panaji</td>
                    <td><span class="status-badge badge-neutral">North</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">14 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.91 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹27.92 L</td>
                    <td style="text-align: right; color: var(--orange);">₹564,207</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,067,366</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.57 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Mangalore</td>
                    <td>Mangalore</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.90 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹22.95 L</td>
                    <td style="text-align: right; color: var(--orange);">₹492,132</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,538,360</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.01 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Cuttack</td>
                    <td>Cuttack</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">11 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.88 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹35.23 L</td>
                    <td style="text-align: right; color: var(--orange);">₹600,056</td>
                    <td style="text-align: right; color: var(--text-light);">₹450,552</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹3.27 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Jamshedpur</td>
                    <td>Jamshedpur</td>
                    <td><span class="status-badge badge-neutral">North East</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">12 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.82 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹31.84 L</td>
                    <td style="text-align: right; color: var(--orange);">₹530,584</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,105,318</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.44 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Chandigarh</td>
                    <td>Chandigarh</td>
                    <td><span class="status-badge badge-neutral">North East</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">16 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.81 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹23.84 L</td>
                    <td style="text-align: right; color: var(--orange);">₹502,108</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,133,800</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.40 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Howrah</td>
                    <td>Howrah</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">13 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.80 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹29.20 L</td>
                    <td style="text-align: right; color: var(--orange);">₹522,508</td>
                    <td style="text-align: right; color: var(--text-light);">₹683,953</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.92 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Coimbatore</td>
                    <td>Coimbatore</td>
                    <td><span class="status-badge badge-neutral">North East</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">16 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.77 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹23.59 L</td>
                    <td style="text-align: right; color: var(--orange);">₹447,998</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,004,481</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.52 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Agartala</td>
                    <td>Agartala</td>
                    <td><span class="status-badge badge-neutral">Central</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.77 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹22.19 L</td>
                    <td style="text-align: right; color: var(--orange);">₹518,551</td>
                    <td style="text-align: right; color: var(--text-light);">₹934,371</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.60 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Gwalior</td>
                    <td>Gwalior</td>
                    <td><span class="status-badge badge-neutral">Central</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">10 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.76 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹37.64 L</td>
                    <td style="text-align: right; color: var(--orange);">₹500,369</td>
                    <td style="text-align: right; color: var(--text-light);">₹387,865</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹3.25 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Mysuru</td>
                    <td>Mysuru</td>
                    <td><span class="status-badge badge-neutral">North</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">17 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.76 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹22.13 L</td>
                    <td style="text-align: right; color: var(--orange);">₹516,750</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,146,003</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.33 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Jamshedpur</td>
                    <td>Jamshedpur</td>
                    <td><span class="status-badge badge-neutral">North East</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">18 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.76 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹20.88 L</td>
                    <td style="text-align: right; color: var(--orange);">₹566,286</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,172,917</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.29 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Kanpur</td>
                    <td>Kanpur</td>
                    <td><span class="status-badge badge-neutral">North</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">13 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.73 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹28.70 L</td>
                    <td style="text-align: right; color: var(--orange);">₹449,486</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,001,871</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.48 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Ludhiana</td>
                    <td>Ludhiana</td>
                    <td><span class="status-badge badge-neutral">West</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">11 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.73 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹33.89 L</td>
                    <td style="text-align: right; color: var(--orange);">₹498,716</td>
                    <td style="text-align: right; color: var(--text-light);">₹786,065</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.74 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Madurai</td>
                    <td>Madurai</td>
                    <td><span class="status-badge badge-neutral">South</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">23 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.72 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹16.15 L</td>
                    <td style="text-align: right; color: var(--orange);">₹467,928</td>
                    <td style="text-align: right; color: var(--text-light);">₹1,276,110</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.14 Cr
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">RetailMart Noida</td>
                    <td>Noida</td>
                    <td><span class="status-badge badge-neutral">North</span></td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">13 Staff</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹3.71 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹28.50 L</td>
                    <td style="text-align: right; color: var(--orange);">₹507,487</td>
                    <td style="text-align: right; color: var(--text-light);">₹837,808</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">
                        ₹2.65 Cr
                    </td>
                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Table 2: Regional Cross-Functional Synthesis -->
                    <div class="table-card" style="margin-top: 1.5rem;">
                        <div class="table-header">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <i class="ti ti-map-pin" style="color: var(--purple); font-size: 1.15rem;"></i>
                                <h3 class="table-title">Regional Synthesis: Workforce Deployment vs Financial Spread</h3>
                            </div>
                            <span class="kpi-badge badge-neutral" style="font-size: 0.7rem;">Geographic Aggregation</span>
                        </div>
                        <div style="overflow-x: auto;">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Region</th>
                                        <th style="text-align: right;">Stores</th>
                                        <th style="text-align: right;">Total Staff</th>
                                        <th style="text-align: right;">Avg Staff / Store</th>
                                        <th style="text-align: right;">Delivered Sales (₹ Cr)</th>
                                        <th style="text-align: right;">Rev / Staff (₹)</th>
                                        <th style="text-align: right;">Store Costs (₹ Cr)</th>
                                        <th style="text-align: right;">Regional Spread (₹ Cr)</th>
                                    </tr>
                                </thead>
                                <tbody>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">South</td>
                    <td style="text-align: right;">14</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">195</td>
                    <td style="text-align: right;">13.9</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹47.24 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,422,467</td>
                    <td style="text-align: right; color: var(--orange);">₹0.68 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹46.55 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North</td>
                    <td style="text-align: right;">14</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">199</td>
                    <td style="text-align: right;">14.2</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹46.29 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,326,215</td>
                    <td style="text-align: right; color: var(--orange);">₹0.70 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹45.59 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North East</td>
                    <td style="text-align: right;">13</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">179</td>
                    <td style="text-align: right;">13.8</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹45.04 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,516,307</td>
                    <td style="text-align: right; color: var(--orange);">₹0.64 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹44.40 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North</td>
                    <td style="text-align: right;">13</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">181</td>
                    <td style="text-align: right;">13.9</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹44.89 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,479,911</td>
                    <td style="text-align: right; color: var(--orange);">₹0.65 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹44.24 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North East</td>
                    <td style="text-align: right;">12</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">179</td>
                    <td style="text-align: right;">14.9</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹42.06 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,349,611</td>
                    <td style="text-align: right; color: var(--orange);">₹0.62 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹41.43 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">East</td>
                    <td style="text-align: right;">12</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">179</td>
                    <td style="text-align: right;">14.9</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹40.21 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,246,296</td>
                    <td style="text-align: right; color: var(--orange);">₹0.61 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹39.60 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North</td>
                    <td style="text-align: right;">12</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">172</td>
                    <td style="text-align: right;">14.3</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹39.86 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,317,417</td>
                    <td style="text-align: right; color: var(--orange);">₹0.63 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹39.23 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North East</td>
                    <td style="text-align: right;">11</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">182</td>
                    <td style="text-align: right;">16.5</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹37.44 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,057,412</td>
                    <td style="text-align: right; color: var(--orange);">₹0.52 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹36.92 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North</td>
                    <td style="text-align: right;">11</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">169</td>
                    <td style="text-align: right;">15.4</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹37.11 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,196,107</td>
                    <td style="text-align: right; color: var(--orange);">₹0.54 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹36.57 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">South</td>
                    <td style="text-align: right;">11</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">174</td>
                    <td style="text-align: right;">15.8</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹37.00 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,126,669</td>
                    <td style="text-align: right; color: var(--orange);">₹0.55 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹36.46 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">West</td>
                    <td style="text-align: right;">11</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">156</td>
                    <td style="text-align: right;">14.2</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹35.56 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,279,259</td>
                    <td style="text-align: right; color: var(--orange);">₹0.54 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹35.02 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">Central</td>
                    <td style="text-align: right;">10</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">145</td>
                    <td style="text-align: right;">14.5</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹34.90 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,407,141</td>
                    <td style="text-align: right; color: var(--orange);">₹0.49 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹34.42 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">South</td>
                    <td style="text-align: right;">10</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">158</td>
                    <td style="text-align: right;">15.8</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹34.12 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,159,488</td>
                    <td style="text-align: right; color: var(--orange);">₹0.49 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹33.63 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">South</td>
                    <td style="text-align: right;">9</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">138</td>
                    <td style="text-align: right;">15.3</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹30.92 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,240,365</td>
                    <td style="text-align: right; color: var(--orange);">₹0.48 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹30.44 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">Central</td>
                    <td style="text-align: right;">7</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">122</td>
                    <td style="text-align: right;">17.4</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹24.37 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹1,997,852</td>
                    <td style="text-align: right; color: var(--orange);">₹0.37 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹24.01 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North</td>
                    <td style="text-align: right;">7</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">107</td>
                    <td style="text-align: right;">15.3</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹23.91 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,234,931</td>
                    <td style="text-align: right; color: var(--orange);">₹0.38 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹23.54 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North</td>
                    <td style="text-align: right;">7</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">122</td>
                    <td style="text-align: right;">17.4</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹22.73 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹1,863,300</td>
                    <td style="text-align: right; color: var(--orange);">₹0.32 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹22.41 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North East</td>
                    <td style="text-align: right;">6</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">85</td>
                    <td style="text-align: right;">14.2</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹20.53 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,415,375</td>
                    <td style="text-align: right; color: var(--orange);">₹0.31 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹20.22 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North</td>
                    <td style="text-align: right;">5</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">80</td>
                    <td style="text-align: right;">16.0</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹17.56 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹2,195,172</td>
                    <td style="text-align: right; color: var(--orange);">₹0.27 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹17.29 Cr</td>
                </tr>
                <tr>
                    <td style="font-weight: 600; color: var(--text-white);">North East</td>
                    <td style="text-align: right;">5</td>
                    <td style="text-align: right; font-weight: 600; color: var(--pink);">78</td>
                    <td style="text-align: right;">15.6</td>
                    <td style="text-align: right; font-weight: 600; color: var(--purple);">₹15.20 Cr</td>
                    <td style="text-align: right; color: var(--cyan);">₹1,948,365</td>
                    <td style="text-align: right; color: var(--orange);">₹0.25 Cr</td>
                    <td style="text-align: right; font-weight: 600; color: var(--cyan);">₹14.95 Cr</td>
                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 10. EXECUTIVE SUMMARY DASHBOARD                           -->
                <!-- ========================================================= -->
                <div id="tab-executive" class="tab-pane active">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Executive Summary Dashboard</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Enterprise C-Suite Dossier · Validated Human Resources, Financial Health &amp; Cross-Functional Margins
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                            <div style="font-size: 0.72rem; color: var(--cyan); background: rgba(44, 212, 225, 0.1); padding: 0.35rem 0.75rem; border-radius: 6px; border: 1px solid rgba(44, 212, 225, 0.3); display: inline-flex; align-items: center; gap: 0.35rem;">
                                <i class="ti ti-database"></i> PostgreSQL 18.4 Verified
                            </div>
                            <div style="font-size: 0.72rem; color: var(--purple); background: rgba(164, 89, 208, 0.1); padding: 0.35rem 0.75rem; border-radius: 6px; border: 1px solid rgba(164, 89, 208, 0.3); display: inline-flex; align-items: center; gap: 0.35rem;">
                                <i class="ti ti-calendar"></i> Current: Feb 2026
                            </div>
                            <a href="./project_documents/documentation/RetailMart_V3_Executive_Insights_Report.pdf" target="_blank" class="status-badge badge-success" style="font-size: 0.72rem; padding: 0.35rem 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.3rem;">
                                <i class="ti ti-file-type-pdf"></i> Executive Insights Report (PDF)
                            </a>
                        </div>
                    </div>

                    <!-- 10 Validated Headline KPI Cards (5 Per Row) -->
                    <div class="kpi-grid-5">
                        <!-- Card 1: Delivered Net Revenue -->
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header">
                                <span class="kpi-title">DELIVERED NET REVENUE</span>
                                <span class="status-badge badge-danger">-14.51% MoM</span>
                            </div>
                            <div class="kpi-value">₹676.95 Cr</div>
                            <div class="kpi-subtext" style="display: flex; justify-content: space-between; align-items: center;">
                                <span>82540 Fulfilled Orders</span>
                                <a href="javascript:void(0)" onclick="switchTab('finance')" style="color: var(--purple); text-decoration: none; font-size: 0.75rem; font-weight: 600; cursor: pointer;">Finance &gt;</a>
                            </div>
                        </div>

                        <!-- Card 2: Gross Contribution Margin -->
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header">
                                <span class="kpi-title">GROSS CONTRIBUTION MARGIN</span>
                                <span class="status-badge badge-success">Markup</span>
                            </div>
                            <div class="kpi-value">27.49%</div>
                            <div class="kpi-subtext" style="display: flex; justify-content: space-between; align-items: center;">
                                <span>₹186.1 Cr Gross Profit</span>
                                <span style="color: var(--cyan); font-size: 0.72rem;">COGS: ₹490.86 Cr</span>
                            </div>
                        </div>

                        <!-- Card 3: Total Operating Outflows -->
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header">
                                <span class="kpi-title">TOTAL OPERATING OUTFLOWS</span>
                                <span class="status-badge badge-success">-14.59% MoM</span>
                            </div>
                            <div class="kpi-value">₹811.54 Cr</div>
                            <div class="kpi-subtext" style="display: flex; justify-content: space-between; align-items: center;">
                                <span>Corp: ₹801.5 Cr | Store: ₹10.0 Cr</span>
                                <a href="javascript:void(0)" onclick="switchTab('finance')" style="color: var(--orange); text-decoration: none; font-size: 0.75rem; font-weight: 600; cursor: pointer;">Expenses &gt;</a>
                            </div>
                        </div>

                        <!-- Card 4: Net Operating Spread -->
                        <div class="kpi-card accent-orange">
                            <div class="kpi-header">
                                <span class="kpi-title">NET OPERATING SPREAD</span>
                                <span class="status-badge badge-danger">Deficit Alert</span>
                            </div>
                            <div class="kpi-value">₹-134.59 Cr</div>
                            <div class="kpi-subtext">
                                <span>Delivered Revenue - Total Expenses</span>
                            </div>
                        </div>

                        <!-- Card 5: Total Active Workforce -->
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header">
                                <span class="kpi-title">TOTAL ACTIVE WORKFORCE</span>
                                <span class="status-badge badge-neutral">100% Active</span>
                            </div>
                            <div class="kpi-value">3000 Staff</div>
                            <div class="kpi-subtext" style="display: flex; justify-content: space-between; align-items: center;">
                                <span>Deployed Across 200 Stores</span>
                                <a href="javascript:void(0)" onclick="switchTab('hr')" style="color: var(--pink); text-decoration: none; font-size: 0.75rem; font-weight: 600; cursor: pointer;">HR Domain &gt;</a>
                            </div>
                        </div>

                        <!-- Card 6: Monthly Base Payroll -->
                        <div class="kpi-card accent-pink">
                            <div class="kpi-header">
                                <span class="kpi-title">MONTHLY BASE PAYROLL</span>
                                <span class="status-badge badge-neutral">Fixed</span>
                            </div>
                            <div class="kpi-value">₹18.98 Cr</div>
                            <div class="kpi-subtext">
                                <span>Annualized: ₹227.78 Cr Base</span>
                            </div>
                        </div>

                        <!-- Card 7: Average Base Compensation -->
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header">
                                <span class="kpi-title">AVERAGE BASE COMPENSATION</span>
                                <span class="status-badge badge-neutral">Monthly</span>
                            </div>
                            <div class="kpi-value">₹63274</div>
                            <div class="kpi-subtext">
                                <span>Median: ₹43959 / month</span>
                            </div>
                        </div>

                        <!-- Card 8: Attendance Compliance -->
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header">
                                <span class="kpi-title">ATTENDANCE COMPLIANCE</span>
                                <span class="status-badge badge-neutral" style="font-size: 0.65rem;">[PROXY]</span>
                            </div>
                            <div class="kpi-value">7.5%</div>
                            <div class="kpi-subtext">
                                <span>Avg Shift: 9.0 hrs / day</span>
                            </div>
                        </div>

                        <!-- Card 9: Revenue Per Employee -->
                        <div class="kpi-card accent-purple">
                            <div class="kpi-header">
                                <span class="kpi-title">REVENUE PER EMPLOYEE</span>
                                <span class="status-badge badge-success">Productivity</span>
                            </div>
                            <div class="kpi-value">₹22.57 L</div>
                            <div class="kpi-subtext" style="display: flex; justify-content: space-between; align-items: center;">
                                <span>Total Top-Line Efficiency</span>
                                <a href="javascript:void(0)" onclick="switchTab('cross')" style="color: var(--purple); text-decoration: none; font-size: 0.75rem; font-weight: 600; cursor: pointer;">Cross-Func &gt;</a>
                            </div>
                        </div>

                        <!-- Card 10: Settlement Clearance Rate -->
                        <div class="kpi-card accent-cyan">
                            <div class="kpi-header">
                                <span class="kpi-title">SETTLEMENT CLEARANCE RATE</span>
                                <span class="status-badge badge-success">High Health</span>
                            </div>
                            <div class="kpi-value">84.91%</div>
                            <div class="kpi-subtext">
                                <span>Reserves: ₹4.89 Cr Liquid</span>
                            </div>
                        </div>
                    </div>

                    <!-- Charts Row: 26-Month Trajectory & Operating Expense Distribution -->
                    <div class="charts-grid-2" style="margin-top: 1.5rem;">
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-chart-line" style="color: var(--purple);"></i>
                                    26-Month Enterprise Trajectory: Net Revenue vs Total OPEX (₹ Crores)
                                </span>
                                <span style="font-size: 0.72rem; color: var(--text-muted);">
                                    PostgreSQL Aggregated Monthly Series
                                </span>
                            </div>
                            <div id="chart-exec-trajectory" style="min-height: 320px;"></div>
                        </div>

                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title">
                                    <i class="ti ti-pie-2" style="color: var(--orange);"></i>
                                    Operating Expense Distribution (Corporate vs Store Branches)
                                </span>
                                <span style="font-size: 0.72rem; color: var(--text-muted);">
                                    Total OPEX: ₹811.54 Cr
                                </span>
                            </div>
                            <div id="chart-exec-expense-mix" style="min-height: 320px;"></div>
                        </div>
                    </div>

                    <!-- Drivers & Critical Risk Section -->
                    <div class="charts-grid-2" style="margin-top: 1.5rem;">
                        <!-- Left Column: Positive Operational & Financial Drivers -->
                        <div class="table-card" style="margin-bottom: 0;">
                            <div class="table-header">
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    <i class="ti ti-trending-up" style="color: var(--cyan); font-size: 1.15rem;"></i>
                                    <h3 class="table-title">Positive Operational &amp; Financial Drivers</h3>
                                </div>
                                <span class="kpi-badge badge-success" style="font-size: 0.7rem;">4 Verified Strengths</span>
                            </div>
                            <div style="padding: 1rem 0; display: flex; flex-direction: column; gap: 0.85rem;">
                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid var(--cyan); border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">High Payment Settlement Integrity</span>
                                        <span class="status-badge badge-success">84.9% Success</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">Electronic bank transfers, credit card, and UPI tenders achieve an 84.9% completion rate with 120,949 successfully completed transactions across 200 retail stores.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Pillar: Finance &amp; Cash Flow</div>
                                </div>

                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid var(--cyan); border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">Healthy Retail Gross Margin</span>
                                        <span class="status-badge badge-success">27.5% Mark-Up</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">Delivered net revenue of ₹676.95 Cr generates ₹186.10 Cr in gross contribution over unit product cost price across all product lines.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Pillar: Commercial Margins</div>
                                </div>

                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid var(--cyan); border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">Consistent Work Shift Duration</span>
                                        <span class="status-badge badge-success">9.0 hrs / day</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">Store retail employees maintain an average shift duration of 9.0 hours per logged clock-in day across 88,310 attendance records.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Pillar: HR &amp; Operations</div>
                                </div>

                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid var(--cyan); border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">Strong Top-Line Revenue per Head</span>
                                        <span class="status-badge badge-success">₹22.57 Lakhs / Staff</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">With 3,000 staff members driving ₹6,769.5M in net delivered sales, average productivity stands at ₹2.26M per employee across the retail store network.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Pillar: Workforce Productivity</div>
                                </div>
                            </div>
                        </div>

                        <!-- Right Column: Critical Risks & Material Exceptions -->
                        <div class="table-card" style="margin-bottom: 0;">
                            <div class="table-header">
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    <i class="ti ti-alert-triangle" style="color: var(--orange); font-size: 1.15rem;"></i>
                                    <h3 class="table-title">Critical Risks &amp; Material Exceptions</h3>
                                </div>
                                <span class="kpi-badge badge-danger" style="font-size: 0.7rem;">Action Required</span>
                            </div>
                            <div style="padding: 1rem 0; display: flex; flex-direction: column; gap: 0.85rem;">
                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid #F43F5E; border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">Operating Cash Flow Deficit</span>
                                        <span class="status-badge badge-danger">-₹134.59 Cr Spread</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">Total non-store corporate expenses (₹801.50 Cr) and branch operating costs (₹10.04 Cr) exceed total delivered commercial sales (₹676.95 Cr), resulting in an operating cash deficit.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Scope: Critical Risk</div>
                                </div>

                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid var(--orange); border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">Corporate Overhead Concentration</span>
                                        <span class="status-badge badge-warning">Top 3 Cats = 52.4%</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">IT Infrastructure (₹140.2 Cr), Marketing Campaigns (₹139.8 Cr), and Consulting/Legal fees (₹140.1 Cr) consume over half of all corporate expenditure without variable linkage to volume.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Scope: Cost Management</div>
                                </div>

                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid #F43F5E; border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">Liquidity Reserve Coverage</span>
                                        <span class="status-badge badge-danger">₹4.89 Cr Cash Reserves</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">Current liquid bank account balances of ₹4.89 Cr represent less than 1 month of base contractual payroll (₹18.98 Cr/mo), necessitating immediate liquidity backstops or credit sweeps.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Scope: Treasury Liquidity</div>
                                </div>

                                <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-left: 4px solid var(--orange); border-radius: 6px; padding: 0.85rem;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                                        <span style="font-weight: 700; font-size: 0.88rem; color: var(--text-white);">Regional Revenue &amp; Efficiency Asymmetry</span>
                                        <span class="status-badge badge-warning">2.1x Spread Gap</span>
                                    </div>
                                    <p style="font-size: 0.75rem; color: var(--text-light); line-height: 1.45; margin: 0;">Metropolitan outlets in the West and South regions average ₹2.8M in revenue per employee, while tier-3 branches in the North East average under ₹1.4M per employee.</p>
                                    <div style="font-size: 0.68rem; color: var(--text-muted); margin-top: 0.35rem;">Scope: Retail Distribution</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Board-Level Management Attention & Operational Directives -->
                    <div class="action-card" style="margin-top: 1.5rem;">
                        <div class="action-header">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <i class="ti ti-clipboard-list" style="color: var(--purple); font-size: 1.2rem;"></i>
                                <h3 style="font-size: 1.05rem; font-weight: 700; color: var(--text-white); margin: 0;">
                                    Board-Level Management Attention &amp; Operational Directives
                                </h3>
                            </div>
                            <span style="font-size: 0.75rem; color: var(--text-muted);">
                                Executive mandates assigned to Chief Financial Officer (CFO) and Chief Human Resources Officer (CHRO)
                            </span>
                        </div>

                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; padding: 0.5rem 0;">
                            <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-radius: 8px; padding: 1.15rem; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                                        <span class="status-badge badge-danger">P0 - Immediate</span>
                                        <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Target: Q2 2026</span>
                                    </div>
                                    <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-white); margin-bottom: 0.35rem;">Corporate Expense Rationalization</h4>
                                    <div style="font-size: 0.72rem; color: var(--cyan); font-weight: 600; margin-bottom: 0.6rem;">Owner: Chief Financial Officer (CFO)</div>
                                    <p style="font-size: 0.78rem; color: var(--text-light); line-height: 1.5; margin-bottom: 0.75rem;">Implement strict zero-based budgeting on non-store overhead. Conduct vendor audit across IT cloud services and corporate consulting contracts to curtail ₹801.5 Cr annualized outflow.</p>
                                </div>
                                <div style="border-top: 1px solid rgba(36, 89, 138, 0.4); padding-top: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.7rem; color: var(--text-muted);">Governance Status:</span>
                                    <span class="status-badge badge-neutral" style="font-size: 0.65rem;">Active Mandate</span>
                                </div>
                            </div>

                            <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-radius: 8px; padding: 1.15rem; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                                        <span class="status-badge badge-danger">P0 - Immediate</span>
                                        <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Target: 30 Days</span>
                                    </div>
                                    <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-white); margin-bottom: 0.35rem;">Treasury Liquidity Buffer &amp; Working Capital</h4>
                                    <div style="font-size: 0.72rem; color: var(--cyan); font-weight: 600; margin-bottom: 0.6rem;">Owner: Chief Financial Officer (CFO)</div>
                                    <p style="font-size: 0.78rem; color: var(--text-light); line-height: 1.5; margin-bottom: 0.75rem;">Establish automated treasury pooling and dynamic cash-sweep facilities across the 200 corporate bank accounts to maintain a minimum 1.5x liquid coverage (₹28.5 Cr) against monthly payroll obligations.</p>
                                </div>
                                <div style="border-top: 1px solid rgba(36, 89, 138, 0.4); padding-top: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.7rem; color: var(--text-muted);">Governance Status:</span>
                                    <span class="status-badge badge-neutral" style="font-size: 0.65rem;">Active Mandate</span>
                                </div>
                            </div>

                            <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-radius: 8px; padding: 1.15rem; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                                        <span class="status-badge badge-warning">P1 - High</span>
                                        <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Target: 60 Days</span>
                                    </div>
                                    <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-white); margin-bottom: 0.35rem;">Retail Branch Workforce Rebalancing</h4>
                                    <div style="font-size: 0.72rem; color: var(--cyan); font-weight: 600; margin-bottom: 0.6rem;">Owner: Chief Human Resources Officer (CHRO)</div>
                                    <p style="font-size: 0.78rem; color: var(--text-light); line-height: 1.5; margin-bottom: 0.75rem;">Redeploy store staff from underperforming branches (&lt;₹15L rev/employee) to high-throughput flagship stores (&gt;₹30L rev/employee) to optimize labor-to-revenue ratio and improve floor productivity.</p>
                                </div>
                                <div style="border-top: 1px solid rgba(36, 89, 138, 0.4); padding-top: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.7rem; color: var(--text-muted);">Governance Status:</span>
                                    <span class="status-badge badge-neutral" style="font-size: 0.65rem;">Active Mandate</span>
                                </div>
                            </div>

                            <div style="background: rgba(15, 31, 51, 0.7); border: 1px solid var(--blue-border); border-radius: 8px; padding: 1.15rem; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                                        <span class="status-badge badge-neutral">P2 - Medium</span>
                                        <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">Target: Q3 2026</span>
                                    </div>
                                    <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-white); margin-bottom: 0.35rem;">Incentive Compensation Alignment</h4>
                                    <div style="font-size: 0.72rem; color: var(--cyan); font-weight: 600; margin-bottom: 0.6rem;">Owner: Chief Human Resources Officer (CHRO)</div>
                                    <p style="font-size: 0.78rem; color: var(--text-light); line-height: 1.5; margin-bottom: 0.75rem;">Transition retail store manager incentive bonuses from pure revenue targets to store operational contribution margin (Delivered Sales minus COGS, Branch Expenses, and Store Payroll).</p>
                                </div>
                                <div style="border-top: 1px solid rgba(36, 89, 138, 0.4); padding-top: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 0.7rem; color: var(--text-muted);">Governance Status:</span>
                                    <span class="status-badge badge-neutral" style="font-size: 0.65rem;">Active Mandate</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ========================================================= -->
                <!-- 11. SCENARIO SIMULATOR (WHAT-IF LEVERS)                   -->
                <!-- ========================================================= -->
                                <!-- ========================================================= -->
                <!-- 11. SCENARIO SIMULATOR (WHAT-IF SENSITIVITY MODELING)       -->
                <!-- ========================================================= -->
                <div id="tab-simulator" class="tab-pane">
                    <div class="page-header">
                        <div>
                            <h2 class="page-title">Workforce, Compensation &amp; Store Expense Scenario Simulator</h2>
                            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
                                Real-Time What-If Sensitivity Modeling · PostgreSQL 18 Live Actuals Baseline
                            </div>
                        </div>
                        <div>
                            <button id="btn-reset-sim" class="btn btn-secondary">
                                <i class="ti ti-rotate-clockwise-2"></i> Reset Levers to Baseline
                            </button>
                        </div>
                    </div>

                    <!-- Analytical Governance & Mathematical Logic Banner -->
                    <div style="background: rgba(44, 212, 225, 0.05); border: 1px solid rgba(44, 212, 225, 0.25); border-radius: 10px; padding: 0.85rem 1.25rem; margin-bottom: 1.5rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; font-weight: 700; color: var(--cyan); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">
                            <i class="ti ti-shield-check" style="font-size: 1.1rem;"></i>
                            <span>Analytical Governance &amp; Mathematical Logic</span>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-light); margin-top: 0.4rem; line-height: 1.45;">
                            <strong>Store Contribution Profit</strong> = Projected Delivered Revenue &minus; Projected COGS &minus; Projected Store OPEX &minus; Projected Annual Store Payroll.
                        </div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">
                            Baseline figures reconcile directly against verified PostgreSQL actuals: 3,000 active staff, ₹18.98 Cr monthly base payroll, ₹10.04 Cr store operating expenses, and ₹676.95 Cr delivered revenue.
                        </div>
                    </div>

                    <!-- Simulator Layout: Interactive Levers on Left, Real-Time Outcomes on Right -->
                    <div class="charts-grid-2">
                        <!-- Left Column: Interactive Scenario Levers -->
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title" style="color: var(--cyan);">
                                    <i class="ti ti-adjustments-horizontal"></i>
                                    Scenario Levers (Bounded Simulation Parameters)
                                </span>
                                <span class="kpi-badge badge-neutral">Client-Side Calculation</span>
                            </div>

                            <div style="display: flex; flex-direction: column; gap: 1.5rem; padding: 0.75rem 0;">
                                <!-- Lever 1: Headcount Adjustment -->
                                <div>
                                    <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 0.4rem;">
                                        <span style="font-weight: 600; color: var(--text-white);">1. Workforce Headcount Delta</span>
                                        <span id="val-headcount" style="font-weight: 700; color: var(--pink);">0%</span>
                                    </div>
                                    <input type="range" id="sim-headcount" min="-25" max="30" step="1" value="0" style="width: 100%; accent-color: var(--pink);">
                                    <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.2rem;">
                                        <span>-25% (Rightsizing: 2,250 Staff)</span>
                                        <span>Baseline (3,000 Staff)</span>
                                        <span>+30% (Expansion: 3,900 Staff)</span>
                                    </div>
                                </div>

                                <!-- Lever 2: Salary Increment Delta -->
                                <div>
                                    <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 0.4rem;">
                                        <span style="font-weight: 600; color: var(--text-white);">2. Salary Increment / Comp Review (%)</span>
                                        <span id="val-salary" style="font-weight: 700; color: var(--cyan);">0%</span>
                                    </div>
                                    <input type="range" id="sim-salary" min="-10" max="30" step="1" value="0" style="width: 100%; accent-color: var(--cyan);">
                                    <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.2rem;">
                                        <span>-10% (Cost Freeze)</span>
                                        <span>Baseline (₹63,274 avg)</span>
                                        <span>+30% (Market Hike)</span>
                                    </div>
                                </div>

                                <!-- Lever 3: Store Expense Sensitivity -->
                                <div>
                                    <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 0.4rem;">
                                        <span style="font-weight: 600; color: var(--text-white);">3. Store Branch OPEX Sensitivity (%)</span>
                                        <span id="val-store-exp" style="font-weight: 700; color: var(--orange);">0%</span>
                                    </div>
                                    <input type="range" id="sim-store-exp" min="-30" max="30" step="1" value="0" style="width: 100%; accent-color: var(--orange);">
                                    <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.2rem;">
                                        <span>-30% (Rent / Utility Cut)</span>
                                        <span>Baseline (₹10.04 Cr)</span>
                                        <span>+30% (Inflationary Shock)</span>
                                    </div>
                                </div>

                                <!-- Lever 4: Commercial Sales Growth -->
                                <div>
                                    <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 0.4rem;">
                                        <span style="font-weight: 600; color: var(--text-white);">4. Delivered Commercial Sales Growth (%)</span>
                                        <span id="val-sales" style="font-weight: 700; color: var(--purple);">0%</span>
                                    </div>
                                    <input type="range" id="sim-sales" min="-20" max="30" step="1" value="0" style="width: 100%; accent-color: var(--purple);">
                                    <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: var(--text-muted); margin-top: 0.2rem;">
                                        <span>-20% (Macro Contraction)</span>
                                        <span>Baseline (₹676.95 Cr)</span>
                                        <span>+30% (Store Scale)</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Right Column: Simulated Financial & Workforce Outcomes -->
                        <div class="chart-card">
                            <div class="chart-header">
                                <span class="chart-title" style="color: var(--purple);">
                                    <i class="ti ti-calculator"></i>
                                    Simulated Operational &amp; Financial Outcomes
                                </span>
                                <span id="sim-var" class="status-badge badge-neutral">Baseline (0.0%)</span>
                            </div>

                            <div class="kpi-grid" style="grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
                                <!-- Projected Headcount -->
                                <div class="kpi-card accent-pink" style="padding: 1rem;">
                                    <div class="kpi-title">Projected Workforce</div>
                                    <div class="kpi-value" id="sim-headcount-val" style="font-size: 1.35rem;">3,000 Staff</div>
                                    <div class="kpi-subtext">Baseline: 3000 Staff</div>
                                </div>

                                <!-- Projected Monthly Payroll -->
                                <div class="kpi-card accent-pink" style="padding: 1rem;">
                                    <div class="kpi-title">Monthly Payroll Outflow</div>
                                    <div class="kpi-value" id="sim-payroll-val" style="font-size: 1.35rem;">₹18.98 Cr / mo</div>
                                    <div class="kpi-subtext">Baseline: ₹18.98 Cr / mo</div>
                                </div>

                                <!-- Projected Sales Revenue -->
                                <div class="kpi-card accent-purple" style="padding: 1rem;">
                                    <div class="kpi-title">Projected Delivered Sales</div>
                                    <div class="kpi-value" id="sim-rev-val" style="font-size: 1.35rem;">₹676.95 Cr</div>
                                    <div class="kpi-subtext">Baseline: ₹676.95 Cr</div>
                                </div>

                                <!-- Projected Contribution -->
                                <div class="kpi-card accent-cyan" style="padding: 1rem;">
                                    <div class="kpi-title">Store Contribution Profit</div>
                                    <div class="kpi-value" id="sim-margin-val" style="font-size: 1.35rem;">₹-51.73 Cr</div>
                                    <div class="kpi-subtext">Baseline: ₹-51.73 Cr</div>
                                </div>
                            </div>

                            <div style="background-color: rgba(15, 31, 51, 0.6); padding: 0.85rem 1rem; border-radius: 8px; border: 1px solid var(--blue-border); margin-bottom: 1.25rem; display: flex; justify-content: space-between;">
                                <div>
                                    <span style="font-size: 0.72rem; color: var(--text-muted);">Store OPEX Outflow:</span>
                                    <div id="sim-store-exp-val" style="font-weight: 700; color: var(--orange); font-size: 0.95rem;">₹10.04 Cr</div>
                                </div>
                                <div>
                                    <span style="font-size: 0.72rem; color: var(--text-muted);">Annual Labor-to-Sales:</span>
                                    <div id="sim-labor-ratio-val" style="font-weight: 700; color: var(--cyan); font-size: 0.95rem;">33.6% of Sales</div>
                                </div>
                            </div>

                            <!-- Comparative Bar Chart -->
                            <div id="sim-comparison-chart"></div>
                        </div>
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

                // =========================================================
        // WORKFORCE, COMPENSATION & OPEX SCENARIO SIMULATOR
        // =========================================================
        const simBaseline = {"base_net_revenue": 6769536004.48, "base_revenue_crores": 676.95, "base_cogs": 4908577904.87, "base_cogs_crores": 490.86, "base_cogs_rate_pct": 72.51, "base_gross_margin": 1860958099.6099997, "base_gross_margin_crores": 186.1, "base_gross_margin_pct": 27.49, "base_headcount": 3000, "base_avg_salary": 63273.6, "base_monthly_payroll": 189820814.0, "base_monthly_payroll_crores": 18.98, "base_annual_payroll": 2277849768.0, "base_annual_payroll_crores": 227.78, "base_store_expenses": 100369598.57, "base_store_expenses_crores": 10.04, "base_corp_expenses": 8015031384.29, "base_corp_expenses_crores": 801.5, "base_delivered_orders": 82540, "base_store_contribution": -517261266.9600003, "base_store_contribution_crores": -51.73, "base_net_operating_spread": -1345864978.38, "base_net_spread_crores": -134.59};
        let simChart = null;

        function formatSimINR(val) {
            if (Math.abs(val) >= 10000000) {
                return '₹' + (val / 10000000).toFixed(2) + ' Cr';
            } else if (Math.abs(val) >= 100000) {
                return '₹' + (val / 100000).toFixed(2) + ' L';
            } else {
                return '₹' + Number(val).toLocaleString('en-IN', { maximumFractionDigits: 0 });
            }
        }

        function initSimulator() {
            const sliderHeadcount = document.getElementById('sim-headcount');
            const sliderSalary = document.getElementById('sim-salary');
            const sliderStoreExp = document.getElementById('sim-store-exp');
            const sliderSales = document.getElementById('sim-sales');

            const valHeadcount = document.getElementById('val-headcount');
            const valSalary = document.getElementById('val-salary');
            const valStoreExp = document.getElementById('val-store-exp');
            const valSales = document.getElementById('val-sales');

            const simHeadcountEl = document.getElementById('sim-headcount-val');
            const simPayrollEl = document.getElementById('sim-payroll-val');
            const simRevEl = document.getElementById('sim-rev-val');
            const simMarginEl = document.getElementById('sim-margin-val');
            const simStoreExpEl = document.getElementById('sim-store-exp-val');
            const simLaborRatioEl = document.getElementById('sim-labor-ratio-val');
            const simVarEl = document.getElementById('sim-var');

            if (!sliderHeadcount) return;

            function recalculate() {
                const hcPct = parseFloat(sliderHeadcount.value) / 100;
                const salPct = parseFloat(sliderSalary.value) / 100;
                const expPct = parseFloat(sliderStoreExp.value) / 100;
                const salesPct = parseFloat(sliderSales.value) / 100;

                valHeadcount.textContent = (hcPct >= 0 ? '+' : '') + (hcPct * 100).toFixed(0) + '%';
                valSalary.textContent = (salPct >= 0 ? '+' : '') + (salPct * 100).toFixed(0) + '%';
                valStoreExp.textContent = (expPct >= 0 ? '+' : '') + (expPct * 100).toFixed(0) + '%';
                valSales.textContent = (salesPct >= 0 ? '+' : '') + (salesPct * 100).toFixed(0) + '%';

                // Model Calculations
                const simHeadcount = Math.round(simBaseline.base_headcount * (1 + hcPct));
                const simAvgSalary = simBaseline.base_avg_salary * (1 + salPct);
                const simMonthlyPayroll = simHeadcount * simAvgSalary;
                const simAnnualPayroll = simMonthlyPayroll * 12;

                const simRevenue = simBaseline.base_net_revenue * (1 + salesPct);
                const simCogs = simBaseline.base_cogs * (1 + salesPct);
                const simGrossMargin = simRevenue - simCogs;
                const simStoreExpenses = simBaseline.base_store_expenses * (1 + expPct);

                const simContribution = simGrossMargin - simStoreExpenses - simAnnualPayroll;
                const simLaborRatio = (simAnnualPayroll / simRevenue) * 100;

                const variance = simContribution - simBaseline.base_store_contribution;
                const varPct = simBaseline.base_store_contribution !== 0 
                    ? (variance / Math.abs(simBaseline.base_store_contribution)) * 100 
                    : 0;

                // Update UI elements
                simHeadcountEl.textContent = Number(simHeadcount).toLocaleString('en-IN') + ' Staff';
                simPayrollEl.textContent = formatSimINR(simMonthlyPayroll) + ' / mo';
                simRevEl.textContent = formatSimINR(simRevenue);
                simMarginEl.textContent = formatSimINR(simContribution);
                simStoreExpEl.textContent = formatSimINR(simStoreExpenses);
                simLaborRatioEl.textContent = simLaborRatio.toFixed(1) + '% of Sales';

                simVarEl.textContent = (variance >= 0 ? '+' : '') + formatSimINR(variance) + ' (' + (varPct >= 0 ? '+' : '') + varPct.toFixed(1) + '%)';
                simVarEl.className = 'status-badge ' + (variance >= 0 ? 'badge-success' : 'badge-danger');

                // Update Comparison Chart
                if (simChart) {
                    simChart.updateSeries([
                        {
                            name: 'Baseline Actuals (₹ Cr)',
                            data: [
                                Math.round(simBaseline.base_net_revenue / 10000000),
                                Math.round(simBaseline.base_gross_margin / 10000000),
                                Math.round(simBaseline.base_annual_payroll / 10000000),
                                Math.round(simBaseline.base_store_expenses / 10000000),
                                Math.round(simBaseline.base_store_contribution / 10000000)
                            ]
                        },
                        {
                            name: 'Simulated Scenario (₹ Cr)',
                            data: [
                                Math.round(simRevenue / 10000000),
                                Math.round(simGrossMargin / 10000000),
                                Math.round(simAnnualPayroll / 10000000),
                                Math.round(simStoreExpenses / 10000000),
                                Math.round(simContribution / 10000000)
                            ]
                        }
                    ]);
                }
            }

            [sliderHeadcount, sliderSalary, sliderStoreExp, sliderSales].forEach(slider => {
                slider.addEventListener('input', recalculate);
            });

            const resetBtn = document.getElementById('btn-reset-sim');
            if (resetBtn) {
                resetBtn.addEventListener('click', () => {
                    sliderHeadcount.value = 0;
                    sliderSalary.value = 0;
                    sliderStoreExp.value = 0;
                    sliderSales.value = 0;
                    recalculate();
                });
            }

            // Render Initial ApexChart
            const chartOptions = {
                series: [
                    {
                        name: 'Baseline Actuals (₹ Cr)',
                        data: [
                            Math.round(simBaseline.base_net_revenue / 10000000),
                            Math.round(simBaseline.base_gross_margin / 10000000),
                            Math.round(simBaseline.base_annual_payroll / 10000000),
                            Math.round(simBaseline.base_store_expenses / 10000000),
                            Math.round(simBaseline.base_store_contribution / 10000000)
                        ],
                        color: '#6F8298'
                    },
                    {
                        name: 'Simulated Scenario (₹ Cr)',
                        data: [
                            Math.round(simBaseline.base_net_revenue / 10000000),
                            Math.round(simBaseline.base_gross_margin / 10000000),
                            Math.round(simBaseline.base_annual_payroll / 10000000),
                            Math.round(simBaseline.base_store_expenses / 10000000),
                            Math.round(simBaseline.base_store_contribution / 10000000)
                        ],
                        color: '#2CD4E1'
                    }
                ],
                chart: {
                    type: 'bar',
                    height: 330,
                    background: 'transparent',
                    toolbar: { show: false }
                },
                dataLabels: { enabled: false },
                plotOptions: {
                    bar: {
                        horizontal: false,
                        columnWidth: '55%',
                        borderRadius: 4
                    }
                },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                xaxis: {
                    categories: ['Delivered Sales', 'Gross Margin', 'Annual Payroll', 'Store OPEX', 'Store Contribution'],
                    labels: { style: { colors: '#8E9BAE', fontSize: '11px' } }
                },
                yaxis: {
                    labels: {
                        style: { colors: '#8E9BAE' },
                        formatter: function(val) { return '₹' + val + ' Cr'; }
                    }
                },
                tooltip: {
                    theme: 'dark',
                    y: { formatter: function(val) { return '₹' + val + ' Crores'; } }
                },
                legend: {
                    labels: { colors: '#D5DCE5' },
                    position: 'top'
                }
            };

            simChart = new ApexCharts(document.querySelector("#sim-comparison-chart"), chartOptions);
            simChart.render();
            recalculate();
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
                dataLabels: { enabled: false },
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

                        // 19. Monthly Cross-Functional Trajectory Chart
            const trajData = [{"month_date": "2024-01-01", "month_name": "Jan 2024", "total_revenue": 267185168.02, "revenue_crores": 26.72, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 309661705.8, "total_exp_crores": 30.97, "labor_to_rev_pct": 0.0}, {"month_date": "2024-02-01", "month_name": "Feb 2024", "total_revenue": 244549940.56, "revenue_crores": 24.45, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 298309394.91, "total_exp_crores": 29.83, "labor_to_rev_pct": 0.0}, {"month_date": "2024-03-01", "month_name": "Mar 2024", "total_revenue": 278998373.13, "revenue_crores": 27.9, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 297388779.17, "total_exp_crores": 29.74, "labor_to_rev_pct": 0.0}, {"month_date": "2024-04-01", "month_name": "Apr 2024", "total_revenue": 259246085.05, "revenue_crores": 25.92, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 313874364.49, "total_exp_crores": 31.39, "labor_to_rev_pct": 0.0}, {"month_date": "2024-05-01", "month_name": "May 2024", "total_revenue": 267418660.55, "revenue_crores": 26.74, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 334871037.53, "total_exp_crores": 33.49, "labor_to_rev_pct": 0.0}, {"month_date": "2024-06-01", "month_name": "Jun 2024", "total_revenue": 244424928.67, "revenue_crores": 24.44, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 308627528.54, "total_exp_crores": 30.86, "labor_to_rev_pct": 0.0}, {"month_date": "2024-07-01", "month_name": "Jul 2024", "total_revenue": 265343771.94, "revenue_crores": 26.53, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 340904401.71, "total_exp_crores": 34.09, "labor_to_rev_pct": 0.0}, {"month_date": "2024-08-01", "month_name": "Aug 2024", "total_revenue": 273762352.86, "revenue_crores": 27.38, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 323002806.22, "total_exp_crores": 32.3, "labor_to_rev_pct": 0.0}, {"month_date": "2024-09-01", "month_name": "Sep 2024", "total_revenue": 251186458.3, "revenue_crores": 25.12, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 300278035.11, "total_exp_crores": 30.03, "labor_to_rev_pct": 0.0}, {"month_date": "2024-10-01", "month_name": "Oct 2024", "total_revenue": 263748922.2, "revenue_crores": 26.37, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 294131870.72, "total_exp_crores": 29.41, "labor_to_rev_pct": 0.0}, {"month_date": "2024-11-01", "month_name": "Nov 2024", "total_revenue": 257482187.49, "revenue_crores": 25.75, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 301667464.48, "total_exp_crores": 30.17, "labor_to_rev_pct": 0.0}, {"month_date": "2024-12-01", "month_name": "Dec 2024", "total_revenue": 255786204.05, "revenue_crores": 25.58, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 288388760.23, "total_exp_crores": 28.84, "labor_to_rev_pct": 0.0}, {"month_date": "2025-01-01", "month_name": "Jan 2025", "total_revenue": 257852068.67, "revenue_crores": 25.79, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 0.0, "store_exp_crores": 0.0, "total_expenses": 332368553.37, "total_exp_crores": 33.24, "labor_to_rev_pct": 0.0}, {"month_date": "2025-02-01", "month_name": "Feb 2025", "total_revenue": 245739240.79, "revenue_crores": 24.57, "payroll_amount": 0.0, "payroll_crores": 0.0, "store_expenses": 977246.32, "store_exp_crores": 0.1, "total_expenses": 280830505.4, "total_exp_crores": 28.08, "labor_to_rev_pct": 0.0}, {"month_date": "2025-03-01", "month_name": "Mar 2025", "total_revenue": 274164232.1, "revenue_crores": 27.42, "payroll_amount": 14867539.68, "payroll_crores": 1.49, "store_expenses": 8732661.35, "store_exp_crores": 0.87, "total_expenses": 333110984.97, "total_exp_crores": 33.31, "labor_to_rev_pct": 5.42}, {"month_date": "2025-04-01", "month_name": "Apr 2025", "total_revenue": 254886719.83, "revenue_crores": 25.49, "payroll_amount": 14794919.46, "payroll_crores": 1.48, "store_expenses": 8152127.42, "store_exp_crores": 0.82, "total_expenses": 321401662.13, "total_exp_crores": 32.14, "labor_to_rev_pct": 5.8}, {"month_date": "2025-05-01", "month_name": "May 2025", "total_revenue": 265567636.1, "revenue_crores": 26.56, "payroll_amount": 14747086.16, "payroll_crores": 1.47, "store_expenses": 8896985.4, "store_exp_crores": 0.89, "total_expenses": 338421434.27, "total_exp_crores": 33.84, "labor_to_rev_pct": 5.55}, {"month_date": "2025-06-01", "month_name": "Jun 2025", "total_revenue": 269997070.46, "revenue_crores": 27.0, "payroll_amount": 14948211.8, "payroll_crores": 1.49, "store_expenses": 8339924.44, "store_exp_crores": 0.83, "total_expenses": 304526367.17, "total_exp_crores": 30.45, "labor_to_rev_pct": 5.54}, {"month_date": "2025-07-01", "month_name": "Jul 2025", "total_revenue": 274367607.37, "revenue_crores": 27.44, "payroll_amount": 14722548.82, "payroll_crores": 1.47, "store_expenses": 8223501.33, "store_exp_crores": 0.82, "total_expenses": 310753107.36, "total_exp_crores": 31.08, "labor_to_rev_pct": 5.37}, {"month_date": "2025-08-01", "month_name": "Aug 2025", "total_revenue": 262457191.24, "revenue_crores": 26.25, "payroll_amount": 14774856.92, "payroll_crores": 1.48, "store_expenses": 8020936.48, "store_exp_crores": 0.8, "total_expenses": 350794314.42, "total_exp_crores": 35.08, "labor_to_rev_pct": 5.63}, {"month_date": "2025-09-01", "month_name": "Sep 2025", "total_revenue": 261491618.36, "revenue_crores": 26.15, "payroll_amount": 14994540.54, "payroll_crores": 1.5, "store_expenses": 8079625.54, "store_exp_crores": 0.81, "total_expenses": 283616317.32, "total_exp_crores": 28.36, "labor_to_rev_pct": 5.73}, {"month_date": "2025-10-01", "month_name": "Oct 2025", "total_revenue": 270411847.4, "revenue_crores": 27.04, "payroll_amount": 14813324.96, "payroll_crores": 1.48, "store_expenses": 8408593.91, "store_exp_crores": 0.84, "total_expenses": 332460513.11, "total_exp_crores": 33.25, "labor_to_rev_pct": 5.48}, {"month_date": "2025-11-01", "month_name": "Nov 2025", "total_revenue": 258434391.33, "revenue_crores": 25.84, "payroll_amount": 14923880.87, "payroll_crores": 1.49, "store_expenses": 8227347.98, "store_exp_crores": 0.82, "total_expenses": 308550876.67, "total_exp_crores": 30.86, "labor_to_rev_pct": 5.77}, {"month_date": "2025-12-01", "month_name": "Dec 2025", "total_revenue": 269918314.59, "revenue_crores": 26.99, "payroll_amount": 14950070.62, "payroll_crores": 1.5, "store_expenses": 8551967.83, "store_exp_crores": 0.86, "total_expenses": 321159483.48, "total_exp_crores": 32.12, "labor_to_rev_pct": 5.54}, {"month_date": "2026-01-01", "month_name": "Jan 2026", "total_revenue": 256136553.02, "revenue_crores": 25.61, "payroll_amount": 15809749.29, "payroll_crores": 1.58, "store_expenses": 8723296.44, "store_exp_crores": 0.87, "total_expenses": 316220797.41, "total_exp_crores": 31.62, "labor_to_rev_pct": 6.17}, {"month_date": "2026-02-01", "month_name": "Feb 2026", "total_revenue": 218978460.4, "revenue_crores": 21.9, "payroll_amount": 16000462.78, "payroll_crores": 1.6, "store_expenses": 7035384.13, "store_exp_crores": 0.7, "total_expenses": 270079916.87, "total_exp_crores": 27.01, "labor_to_rev_pct": 7.31}];
            if (trajData && trajData.length > 0) {
                const months = trajData.map(d => d.month_name);
                const revenue = trajData.map(d => d.revenue_crores);
                const payroll = trajData.map(d => d.payroll_crores);
                const storeCosts = trajData.map(d => d.store_exp_crores);

                const trajOptions = {
                    series: [
                        { name: 'Delivered Revenue (₹ Cr)', type: 'line', data: revenue, color: '#A459D0' },
                        { name: 'Processed Payroll (₹ Cr)', type: 'column', data: payroll, color: '#E95B9F' },
                        { name: 'Store OPEX (₹ Cr)', type: 'column', data: storeCosts, color: '#E88E3E' }
                    ],
                    chart: {
                        height: 320,
                        type: 'line',
                        background: 'transparent',
                        toolbar: { show: false }
                    },
                    dataLabels: { enabled: false },
                    stroke: { width: [3, 0, 0], curve: 'smooth' },
                    grid: { borderColor: '#24598A', strokeDashArray: 3 },
                    xaxis: {
                        categories: months,
                        labels: { style: { colors: '#8E9BAE', fontSize: '11px' } }
                    },
                    yaxis: [
                        {
                            title: { text: 'Delivered Revenue (₹ Cr)', style: { color: '#A459D0' } },
                            labels: {
                                style: { colors: '#8E9BAE' },
                                formatter: function(val) { return '₹' + val.toFixed(0) + ' Cr'; }
                            }
                        },
                        {
                            opposite: true,
                            title: { text: 'Monthly Outflows (₹ Cr)', style: { color: '#2CD4E1' } },
                            labels: {
                                style: { colors: '#8E9BAE' },
                                formatter: function(val) { return '₹' + val.toFixed(1) + ' Cr'; }
                            }
                        }
                    ],
                    tooltip: { theme: 'dark' },
                    legend: { labels: { colors: '#D5DCE5' }, position: 'top' }
                };
                new ApexCharts(document.querySelector("#chart-cross-trajectory"), trajOptions).render();
            }

            // 20. Department Cost Allocation Chart
            const deptData = [{"dept_name": "IT", "staff_count": 310, "avg_salary": 71392.9, "monthly_payroll": 22131800.0, "payroll_crores": 2.21, "payroll_share_pct": 11.66}, {"dept_name": "Legal", "staff_count": 339, "avg_salary": 61119.09, "monthly_payroll": 20719373.0, "payroll_crores": 2.07, "payroll_share_pct": 10.92}, {"dept_name": "Sales", "staff_count": 300, "avg_salary": 67489.22, "monthly_payroll": 20246765.0, "payroll_crores": 2.02, "payroll_share_pct": 10.67}, {"dept_name": "Finance", "staff_count": 298, "avg_salary": 67496.4, "monthly_payroll": 20113926.0, "payroll_crores": 2.01, "payroll_share_pct": 10.6}, {"dept_name": "HR", "staff_count": 302, "avg_salary": 66320.72, "monthly_payroll": 20028857.0, "payroll_crores": 2.0, "payroll_share_pct": 10.55}, {"dept_name": "Logistics", "staff_count": 299, "avg_salary": 65170.66, "monthly_payroll": 19486027.0, "payroll_crores": 1.95, "payroll_share_pct": 10.27}, {"dept_name": "Operations", "staff_count": 301, "avg_salary": 59777.06, "monthly_payroll": 17992896.0, "payroll_crores": 1.8, "payroll_share_pct": 9.48}, {"dept_name": "Marketing", "staff_count": 307, "avg_salary": 56633.43, "monthly_payroll": 17386464.0, "payroll_crores": 1.74, "payroll_share_pct": 9.16}, {"dept_name": "Procurement", "staff_count": 266, "avg_salary": 62694.11, "monthly_payroll": 16676633.0, "payroll_crores": 1.67, "payroll_share_pct": 8.79}, {"dept_name": "Customer Support", "staff_count": 278, "avg_salary": 54093.79, "monthly_payroll": 15038073.0, "payroll_crores": 1.5, "payroll_share_pct": 7.92}];
            if (deptData && deptData.length > 0) {
                const depts = deptData.map(d => d.dept_name);
                const payrollCrores = deptData.map(d => d.payroll_crores);
                const staff = deptData.map(d => d.staff_count);

                const deptOptions = {
                    series: [
                        { name: 'Monthly Payroll (₹ Cr)', data: payrollCrores, color: '#2CD4E1' },
                        { name: 'Staff Headcount', data: staff, color: '#E95B9F' }
                    ],
                    chart: {
                        type: 'bar',
                        height: 320,
                        background: 'transparent',
                        toolbar: { show: false }
                    },
                    dataLabels: { enabled: false },
                    plotOptions: {
                        bar: { horizontal: true, borderRadius: 4, barHeight: '70%' }
                    },
                    grid: { borderColor: '#24598A', strokeDashArray: 3 },
                    xaxis: {
                        labels: { style: { colors: '#8E9BAE' } }
                    },
                    yaxis: {
                        labels: { style: { colors: '#D5DCE5', fontSize: '11px' } }
                    },
                    tooltip: { theme: 'dark' },
                    legend: { labels: { colors: '#D5DCE5' }, position: 'top' }
                };
                new ApexCharts(document.querySelector("#chart-dept-cost"), deptOptions).render();
            }

            // Initialize Workforce Simulator
            initSimulator();


// 21. Executive 26-Month Trajectory
            new ApexCharts(document.querySelector("#chart-exec-trajectory"), {
                series: [
                    { name: 'Delivered Revenue (₹ Cr)', data: [26.72, 24.45, 27.90, 25.92, 26.74, 24.44, 26.53, 27.38, 25.12, 26.37, 25.75, 25.58, 25.79, 24.57, 27.42, 25.49, 26.56, 27.00, 27.44, 26.25, 26.15, 27.04, 25.84, 26.99, 25.61, 21.90] },
                    { name: 'Total Operating Expenses (₹ Cr)', data: [30.97, 29.83, 29.74, 31.39, 33.49, 30.86, 34.09, 32.30, 30.03, 29.41, 30.17, 28.84, 33.24, 28.08, 33.31, 32.14, 33.84, 30.45, 31.08, 35.08, 28.36, 33.25, 30.86, 32.12, 31.62, 27.01] },
                    { name: 'Operating Net Spread (₹ Cr)', data: [-4.25, -5.38, -1.84, -5.46, -6.75, -6.42, -7.56, -4.92, -4.91, -3.04, -4.42, -3.26, -7.45, -3.51, -5.89, -6.65, -7.29, -3.45, -3.64, -8.83, -2.21, -6.20, -5.01, -5.12, -6.01, -5.11] }
                ],
                chart: { type: 'line', height: 320, background: 'transparent', toolbar: { show: false } },
                colors: ['#A459D0', '#E88E3E', '#2CD4E1'],
                stroke: { curve: 'smooth', width: [3, 3, 2] },
                dataLabels: { enabled: false },
                grid: { borderColor: '#24598A', strokeDashArray: 3 },
                xaxis: {
                    categories: ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024', 'Jul 2024', 'Aug 2024', 'Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024', 'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025', 'Jul 2025', 'Aug 2025', 'Sep 2025', 'Oct 2025', 'Nov 2025', 'Dec 2025', 'Jan 2026', 'Feb 2026'],
                    labels: { style: { colors: '#8E9BAE', fontSize: '11px' } }
                },
                yaxis: {
                    labels: {
                        style: { colors: '#8E9BAE', fontSize: '11px' },
                        formatter: function(val) { return '₹' + val.toFixed(1) + ' Cr'; }
                    }
                },
                tooltip: {
                    theme: 'dark',
                    y: { formatter: function(val) { return '₹' + val.toFixed(2) + ' Cr'; } }
                },
                legend: {
                    labels: { colors: '#D5DCE5' },
                    position: 'top'
                }
            }).render();

            // 22. Executive Operating Expense Mix Donut
            new ApexCharts(document.querySelector("#chart-exec-expense-mix"), {
                series: [801.50, 10.04],
                labels: ['Corporate Expenses (₹801.5 Cr)', 'Store Expenses (₹10.0 Cr)'],
                colors: ['#E88E3E', '#2CD4E1'],
                chart: { type: 'donut', height: 320, background: 'transparent' },
                stroke: { colors: ['#183A5F'], width: 2 },
                dataLabels: { enabled: true, formatter: function(val) { return val.toFixed(1) + '%'; }, style: { fontFamily: 'Inter', fontSize: '11px', fontWeight: 600 } },
                legend: { position: 'bottom', labels: { colors: '#D5DCE5' } },
                plotOptions: {
                    pie: {
                        donut: {
                            size: '65%',
                            labels: {
                                show: true,
                                total: {
                                    show: true,
                                    label: 'Total OPEX',
                                    color: '#FFFFFF',
                                    formatter: function() { return '₹811.5 Cr'; }
                                }
                            }
                        }
                    }
                },
                tooltip: {
                    theme: 'dark',
                    y: { formatter: function(val) { return '₹' + Number(val).toFixed(2) + ' Cr'; } }
                }
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
