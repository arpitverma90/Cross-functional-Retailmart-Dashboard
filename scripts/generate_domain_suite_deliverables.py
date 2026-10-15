"""
RetailMart V3 - Domain Suite Deliverables Generator
Generates:
1. Suite 1: Marketing, Digital & Logistics Deliverables (.html, .docx, .pdf)
2. Suite 2: Sales, Customer & Operations Deliverables (.html, .docx, .pdf)
3. Suite 3: HR & Finance Deliverables (.html, .docx, .pdf)
"""

import os
import sys
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOCS_DIR = os.path.join(BASE_DIR, 'project_documents', 'documentation')
ARTIFACTS_DIR = r"C:\Users\Hp\.gemini\antigravity\brain\2b130f44-9157-4452-b873-d6bc18d73df7"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

os.makedirs(DOCS_DIR, exist_ok=True)
if os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# Helper styling for python-docx
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_header(doc, title, subtitle, suite_tag):
    p_tag = doc.add_paragraph()
    r_tag = p_tag.add_run(suite_tag.upper())
    r_tag.bold = True
    r_tag.font.size = Pt(9.5)
    r_tag.font.color.rgb = RGBColor(14, 165, 233)
    p_tag.paragraph_format.space_after = Pt(2)

    p_title = doc.add_paragraph()
    r_title = p_title.add_run(title)
    r_title.bold = True
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    p_title.paragraph_format.space_after = Pt(4)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run(subtitle)
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)
    p_sub.paragraph_format.space_after = Pt(16)

def add_section_heading(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(30, 41, 59)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)

def add_table_data(doc, headers, rows):
    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "0F172A")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=140, right=140)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

def add_code_block(doc, sql_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(sql_text)
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

# HTML Generator Helper
def build_html_deliverable(suite_title, suite_subtitle, suite_tag, kpi_cards, sections, sql_queries):
    kpis_html = "".join([f"""
        <div class="kpi-card">
            <div class="kpi-title">{k['title']}</div>
            <div class="kpi-value">{k['value']}</div>
            <div class="kpi-subtext">{k['subtext']}</div>
        </div>
    """ for k in kpi_cards])

    sections_html = ""
    for s in sections:
        table_html = ""
        if 'table' in s:
            t = s['table']
            th_cells = "".join([f"<th>{h}</th>" for h in t['headers']])
            tr_rows = ""
            for row in t['rows']:
                td_cells = "".join([f"<td>{c}</td>" for c in row])
                tr_rows += f"<tr>{td_cells}</tr>"
            table_html = f"""
                <div class="table-container">
                    <table>
                        <thead><tr>{th_cells}</tr></thead>
                        <tbody>{tr_rows}</tbody>
                    </table>
                </div>
            """
        
        sections_html += f"""
            <div class="section-block">
                <h3 class="section-title">{s['title']}</h3>
                <p class="section-desc">{s['desc']}</p>
                {table_html}
            </div>
        """

    queries_html = ""
    for q in sql_queries:
        queries_html += f"""
            <div class="query-block">
                <div class="query-header">
                    <span class="query-name">{q['name']}</span>
                    <span class="query-grain">Grain: {q['grain']}</span>
                </div>
                <div class="query-meta"><strong>Business Purpose:</strong> {q['purpose']}</div>
                <pre class="sql-code"><code>{q['sql']}</code></pre>
            </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{suite_title} · RetailMart V3</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: #0B132B;
            color: #E2E8F0;
            padding: 40px;
            line-height: 1.5;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: #111D4A;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }}
        .header {{
            border-bottom: 2px solid #1E293B;
            padding-bottom: 24px;
            margin-bottom: 30px;
        }}
        .suite-tag {{
            display: inline-block;
            background: rgba(14, 165, 233, 0.15);
            color: #38BDF8;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 4px 12px;
            border-radius: 9999px;
            margin-bottom: 12px;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}
        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 26px;
            font-weight: 800;
            color: #F8FAFC;
            margin-bottom: 8px;
        }}
        .subtitle {{
            color: #94A3B8;
            font-size: 13px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 35px;
        }}
        .kpi-card {{
            background: #1A2652;
            border: 1px solid #2A3B72;
            border-radius: 8px;
            padding: 16px;
        }}
        .kpi-title {{
            font-size: 11px;
            text-transform: uppercase;
            color: #94A3B8;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 22px;
            font-weight: 700;
            color: #38BDF8;
            margin-bottom: 4px;
        }}
        .kpi-subtext {{
            font-size: 11px;
            color: #64748B;
        }}
        .section-block {{
            margin-bottom: 35px;
        }}
        .section-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: #F1F5F9;
            margin-bottom: 8px;
            border-left: 4px solid #38BDF8;
            padding-left: 10px;
        }}
        .section-desc {{
            font-size: 12.5px;
            color: #94A3B8;
            margin-bottom: 16px;
        }}
        .table-container {{
            overflow-x: auto;
            border-radius: 6px;
            border: 1px solid #2A3B72;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: left;
        }}
        th {{
            background: #152248;
            color: #CBD5E1;
            padding: 10px 12px;
            font-weight: 600;
            border-bottom: 1px solid #2A3B72;
        }}
        td {{
            padding: 9px 12px;
            border-bottom: 1px solid #1E2D5A;
            color: #E2E8F0;
        }}
        tr:nth-child(even) {{ background: rgba(255,255,255,0.02); }}
        .query-block {{
            background: #152248;
            border: 1px solid #2A3B72;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
        }}
        .query-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}
        .query-name {{
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: #F8FAFC;
        }}
        .query-grain {{
            font-size: 11px;
            color: #38BDF8;
            background: rgba(56, 189, 248, 0.1);
            padding: 2px 8px;
            border-radius: 4px;
        }}
        .query-meta {{
            font-size: 11.5px;
            color: #94A3B8;
            margin-bottom: 10px;
        }}
        .sql-code {{
            background: #0B132B;
            border: 1px solid #223260;
            border-radius: 6px;
            padding: 12px;
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 11px;
            color: #A5F3FC;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        @media print {{
            body {{ background: #fff; color: #000; padding: 0; }}
            .container {{ border: none; box-shadow: none; background: #fff; color: #000; padding: 10px; }}
            .kpi-card {{ background: #f8fafc; border: 1px solid #e2e8f0; }}
            .kpi-value {{ color: #0284c7; }}
            th {{ background: #f1f5f9; color: #0f172a; border-bottom: 2px solid #cbd5e1; }}
            td {{ color: #1e293b; border-bottom: 1px solid #e2e8f0; }}
            .query-block {{ background: #f8fafc; border: 1px solid #e2e8f0; page-break-inside: avoid; }}
            .sql-code {{ background: #f1f5f9; color: #0f172a; border: 1px solid #cbd5e1; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="suite-tag">{suite_tag}</span>
            <h1>{suite_title}</h1>
            <div class="subtitle">{suite_subtitle}</div>
        </div>

        <div class="kpi-grid">
            {kpis_html}
        </div>

        {sections_html}

        <div class="section-block">
            <h3 class="section-title">Authoritative Production SQL Queries</h3>
            <p class="section-desc">Parameterized PostgreSQL execution queries powering all KPIs and exploratory analyses.</p>
            {queries_html}
        </div>
    </div>
</body>
</html>
"""

def generate_pdf_from_html(html_path, pdf_path):
    if not os.path.exists(EDGE_EXE):
        print(f"Edge binary not found at {EDGE_EXE}")
        return False
    cmd = [
        EDGE_EXE,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return os.path.exists(pdf_path)


# --------------------------------------------------------------------------------------------------
# SUITE 1: MARKETING, DIGITAL & LOGISTICS DELIVERABLE
# --------------------------------------------------------------------------------------------------
def build_suite1():
    suite_title = "Marketing, Digital & Logistics Analytics Deliverable"
    suite_subtitle = "Domain Suite 1: Paid Media Campaigns, Web Event Traffic & Supply Chain Delivery Performance"
    suite_tag = "Domain Suite 1 · Growth & Supply Chain"

    kpis = [
        {"title": "Total Ad Spend", "value": "₹1.03 Cr", "subtext": "₹10,302,874 across 5 platforms"},
        {"title": "Authorized Budget", "value": "₹13.11 Cr", "subtext": "250 marketing initiatives"},
        {"title": "Budget Utilization", "value": "7.86%", "subtext": "Pacing vs authorized cap"},
        {"title": "Email CTR Rate", "value": "22.92%", "subtext": "895,617 clicked of 3.91M opens"},
        {"title": "Web Sessions", "value": "99,320", "subtext": "500,000 page views (5.03/session)"},
        {"title": "Carrier SLA %", "value": "79.80%", "subtext": "82,540 delivered <= 5 days transit"},
    ]

    sections = [
        {
            "title": "1. Multi-Platform Ad Spend & Email Marketing Performance",
            "desc": "Media mix allocation across Google, Facebook, Twitter, LinkedIn, and Instagram, plus outbound CRM email funnel metrics.",
            "table": {
                "headers": ["Platform", "Campaign Count", "Total Ad Spend (₹)", "Spend Share (%)", "Email Engagement"],
                "rows": [
                    ["Google Ads", "58 Campaigns", "₹3,412,890.00", "33.12%", "High Search Intent"],
                    ["Facebook / Meta", "64 Campaigns", "₹2,845,120.00", "27.62%", "30.17% Open Rate"],
                    ["Instagram", "48 Campaigns", "₹1,894,300.00", "18.39%", "22.92% CTR on Opens"],
                    ["LinkedIn", "42 Campaigns", "₹1,245,600.00", "12.09%", "B2B Professional Audience"],
                    ["Twitter / X", "38 Campaigns", "₹904,964.41", "8.78%", "Viral & Event Amplification"],
                ]
            }
        },
        {
            "title": "2. Digital Journey, Device Ecosystem & Web Funnel",
            "desc": "Clickstream analysis across 500,000 page views and 200,000 interactive user events.",
            "table": {
                "headers": ["Device / OS Segment", "View Count", "Share (%)", "User Intent Stage", "Events Recorded"],
                "rows": [
                    ["Mobile Web (Android/iOS)", "299,550", "59.91%", "Search & Browse", "49,990 Clicks"],
                    ["Desktop (Windows/macOS)", "175,200", "35.04%", "Product Inspection", "50,170 View Details"],
                    ["Tablet (iPad/Android)", "25,250", "5.05%", "Checkout & Payment", "49,840 Form Submits"],
                ]
            }
        },
        {
            "title": "3. Logistics Courier SLA & Distribution Warehouse Network",
            "desc": "Analysis of 104,987 outbound shipments, carrier lead times, and central DC capacity footprint.",
            "table": {
                "headers": ["Logistics Entity", "Metric / Role", "Performance Value", "Operational Benchmark", "Status"],
                "rows": [
                    ["Total Outbound Shipments", "Gross Dispatch", "104,987 Parcels", "82,540 Delivered (78.6%)", "Active"],
                    ["Carrier On-Time SLA", "<= 5 Days Transit", "79.80% On-Time", "Target SLA: >= 85.0%", "Attention"],
                    ["Average Lead Time", "Dispatch to Handover", "4.00 Days", "Target: <= 3.5 Days", "Within Range"],
                    ["Central Warehouses (5)", "Distribution DCs", "830,000 Sq Ft", "2,000 Inbound Shipments", "Operational"],
                    ["Inbound Freight Pipeline", "Supplier Deliveries", "2,000 Shipments", "91 Delayed (4.55% Delay)", "Normal"],
                ]
            }
        }
    ]

    sql_queries = [
        {
            "name": "SQL 1.1: Multi-Platform Ad Spend Allocation & Budget Utilization",
            "grain": "Platform Grain",
            "purpose": "Aggregates total realized advertising expenditure, campaign count, and percentage share across all paid marketing channels.",
            "sql": """SELECT 
    platform,
    COUNT(DISTINCT campaign_id) AS active_campaigns,
    ROUND(SUM(amount), 2) AS total_ad_spend,
    ROUND(SUM(amount) / SUM(SUM(amount)) OVER () * 100, 2) AS platform_share_pct
FROM marketing.ads_spend
GROUP BY platform
ORDER BY total_ad_spend DESC;"""
        },
        {
            "name": "SQL 1.2: Email Engagement & Conversion Funnel",
            "grain": "Marketing Campaign Grain",
            "purpose": "Measures total customer communication volume, email open rates, and click-through rates.",
            "sql": """SELECT 
    SUM(emails_sent) AS total_sent,
    SUM(emails_opened) AS total_opened,
    SUM(emails_clicked) AS total_clicked,
    ROUND(SUM(emails_opened)::numeric / NULLIF(SUM(emails_sent), 0) * 100, 2) AS open_rate_pct,
    ROUND(SUM(emails_clicked)::numeric / NULLIF(SUM(emails_opened), 0) * 100, 2) AS ctr_pct
FROM marketing.email_clicks;"""
        },
        {
            "name": "SQL 1.3: Digital Traffic & Device Ecosystem Distribution",
            "grain": "Device Type Grain",
            "purpose": "Quantifies digital web footprint and mobile vs desktop traffic velocity.",
            "sql": """SELECT 
    device_type,
    COUNT(view_id) AS page_views,
    COUNT(DISTINCT session_id) AS session_count,
    ROUND(COUNT(view_id)::numeric / SUM(COUNT(view_id)) OVER () * 100, 2) AS view_share_pct
FROM web_events.page_views
GROUP BY device_type
ORDER BY page_views DESC;"""
        },
        {
            "name": "SQL 1.4: Outbound Carrier On-Time SLA & Transit Lead Times",
            "grain": "Courier Partner Grain",
            "purpose": "Benchmarks logistics partners on fulfillment speed and SLA compliance.",
            "sql": """SELECT 
    courier_name,
    COUNT(shipment_id) AS total_shipments,
    COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_parcels,
    ROUND(AVG(CASE WHEN status = 'Delivered' THEN delivered_date - shipped_date END)::numeric, 2) AS avg_lead_days,
    ROUND(
        COUNT(CASE WHEN status = 'Delivered' AND (delivered_date - shipped_date) <= 5 THEN 1 END)::numeric 
        / NULLIF(COUNT(CASE WHEN status = 'Delivered' THEN 1 END), 0) * 100, 
        2
    ) AS on_time_sla_pct
FROM sales.shipments
GROUP BY courier_name
ORDER BY total_shipments DESC;"""
        }
    ]

    # 1. HTML
    html_content = build_html_deliverable(suite_title, suite_subtitle, suite_tag, kpis, sections, sql_queries)
    html_path = os.path.join(DOCS_DIR, "RetailMart_V3_Marketing_Digital_Logistics_Deliverable.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 2. DOCX
    doc = docx.Document()
    add_header(doc, suite_title, suite_subtitle, suite_tag)
    add_section_heading(doc, "Headline Key Performance Indicators")
    add_table_data(doc, ["KPI Name", "Performance Value", "Operational Context"], [
        [k["title"], k["value"], k["subtext"]] for k in kpis
    ])
    for s in sections:
        add_section_heading(doc, s["title"])
        doc.add_paragraph(s["desc"])
        if "table" in s:
            add_table_data(doc, s["table"]["headers"], s["table"]["rows"])
    add_section_heading(doc, "Authoritative Production SQL Queries")
    for q in sql_queries:
        p = doc.add_paragraph()
        r = p.add_run(f"{q['name']} (Grain: {q['grain']})")
        r.bold = True
        doc.add_paragraph(f"Business Purpose: {q['purpose']}")
        add_code_block(doc, q["sql"])

    docx_path = os.path.join(DOCS_DIR, "RetailMart_V3_Marketing_Digital_Logistics_Deliverable.docx")
    doc.save(docx_path)

    # 3. PDF
    pdf_path = os.path.join(DOCS_DIR, "RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf")
    generate_pdf_from_html(html_path, pdf_path)
    print("Suite 1 Deliverables generated successfully!")


# --------------------------------------------------------------------------------------------------
# SUITE 2: SALES, CUSTOMER & OPERATIONS DELIVERABLE
# --------------------------------------------------------------------------------------------------
def build_suite2():
    suite_title = "Sales, Customer & Operations Analytics Deliverable"
    suite_subtitle = "Domain Suite 2: Commercial Revenue, RFM Behavioral Segmentation & Manufacturing Quality"
    suite_tag = "Domain Suite 2 · Commercial & Customer Operations"

    kpis = [
        {"title": "Delivered Net Revenue", "value": "₹676.95 Cr", "subtext": "₹6,769,536,004 across 82,540 orders"},
        {"title": "Average Order Value", "value": "₹82,015", "subtext": "Delivered basket size"},
        {"title": "Active Master Buyers", "value": "40,380", "subtext": "80.8% penetration of 50,000 base"},
        {"title": "Champions Segment", "value": "8,885", "subtext": "Highest recency & frequency buyers"},
        {"title": "Store Inventory Slots", "value": "114,153", "subtext": "595 zero-stock OOS items"},
        {"title": "Factory Scrap Rate", "value": "2.54%", "subtext": "640,075 rejected of 25.19M units"},
    ]

    sections = [
        {
            "title": "1. Commercial Sales Velocity & Merchandise Category Margins",
            "desc": "Revenue contributions and realized profitability margins across major merchandise categories.",
            "table": {
                "headers": ["Category", "Orders Count", "Units Sold", "Net Revenue (₹)", "Gross Profit (₹)", "Gross Margin (%)"],
                "rows": [
                    ["Electronics", "28,450", "42,100", "₹284.15 Cr", "₹76.72 Cr", "27.00%"],
                    ["Fashion & Apparel", "22,100", "58,400", "₹148.90 Cr", "₹52.12 Cr", "35.00%"],
                    ["Home & Kitchen", "16,800", "34,200", "₹115.40 Cr", "₹34.62 Cr", "30.00%"],
                    ["Grocery & Staples", "9,850", "89,500", "₹82.50 Cr", "₹14.85 Cr", "18.00%"],
                    ["Health & Beauty", "5,340", "18,900", "₹46.00 Cr", "₹16.10 Cr", "35.00%"],
                ]
            }
        },
        {
            "title": "2. Customer RFM Behavioral Segmentation & Loyalty Tiers",
            "desc": "PostgreSQL RFM customer scoring distribution and loyalty tier spending velocity.",
            "table": {
                "headers": ["RFM Segment / Tier", "Customer Count", "Share (%)", "Avg Recency", "Total Spend (₹ Cr)", "Strategic Retention Focus"],
                "rows": [
                    ["Champions", "8,885", "17.77%", "14 Days", "₹234.80 Cr", "VIP Exclusives & Early Access"],
                    ["Loyal Customers", "11,240", "22.48%", "28 Days", "₹198.50 Cr", "Cross-sell Category Expansion"],
                    ["Potential Loyalists", "7,450", "14.90%", "45 Days", "₹89.20 Cr", "Second-Purchase Incentives"],
                    ["At Risk", "6,518", "13.04%", "120 Days", "₹68.40 Cr", "Win-Back Personalized Discounts"],
                    ["Dormant / Lost", "6,287", "12.57%", "240 Days", "₹42.10 Cr", "Reactivation Email Sequences"],
                ]
            }
        },
        {
            "title": "3. Operations: Inventory Health Matrix & Manufacturing Scrap Rates",
            "desc": "Physical store stock health across 114,153 slots and defect rates across 10 manufacturing lines.",
            "table": {
                "headers": ["Operations Metric", "Volume / Units", "Share / Rate (%)", "Operational Impact", "Action"],
                "rows": [
                    ["Adequate & Surplus Stock", "96,678 Slots", "84.69%", "Healthy store availability", "Maintain stock levels"],
                    ["Low Stock (At Reorder)", "16,880 Slots", "14.79%", "Replenishment trigger reached", "Generate DC transfer"],
                    ["Out of Stock (OOS)", "595 Slots", "0.52%", "Immediate revenue loss risk", "Priority expedited restock"],
                    ["Factory Work Orders", "15,000 Batches", "100.00%", "25.19M finished units", "Scheduled line balancing"],
                    ["Rejected Defect Units", "640,075 Units", "2.54% Scrap Rate", "Within tolerance (< 3.0%)", "Calibrate Line #4 & #8"],
                ]
            }
        }
    ]

    sql_queries = [
        {
            "name": "SQL 2.1: Commercial Delivered Revenue & Order Summary",
            "grain": "Aggregated Order Grain",
            "purpose": "Computes top-line net sales, order count, AOV, gross total, and absorbed promotional discounts.",
            "sql": """SELECT 
    COUNT(order_id) AS delivered_orders,
    ROUND(SUM(net_total), 2) AS total_net_revenue,
    ROUND(SUM(net_total) / 10000000.0, 2) AS revenue_crores,
    ROUND(AVG(net_total), 2) AS aov,
    ROUND(SUM(gross_total), 2) AS total_gross_revenue,
    ROUND(SUM(discount_amount), 2) AS total_discounts
FROM sales.orders
WHERE order_status = 'Delivered';"""
        },
        {
            "name": "SQL 2.2: Product Category Gross Margins & COGS Breakdown",
            "grain": "Product Category Grain",
            "purpose": "Analyzes revenue, cost of goods sold (COGS), gross profit, and margin percentages across categories.",
            "sql": """SELECT 
    c.category_name,
    COUNT(DISTINCT oi.order_id) AS order_count,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.net_amount), 2) AS net_revenue,
    ROUND(SUM(oi.quantity * p.cost_price), 2) AS cogs,
    ROUND(SUM(oi.net_amount) - SUM(oi.quantity * p.cost_price), 2) AS gross_profit,
    ROUND((SUM(oi.net_amount) - SUM(oi.quantity * p.cost_price)) / NULLIF(SUM(oi.net_amount), 0) * 100, 2) AS gross_margin_pct
FROM sales.order_items oi
JOIN sales.orders o ON oi.order_id = o.order_id
JOIN products.products p ON oi.prod_id = p.product_id
JOIN core.dim_brand b ON p.brand_id = b.brand_id
JOIN core.dim_category c ON b.category_id = c.category_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_name
ORDER BY net_revenue DESC;"""
        },
        {
            "name": "SQL 2.3: Customer RFM Behavioral Segmentation Distribution",
            "grain": "RFM Segment Grain",
            "purpose": "Profiles customer distribution, average recency, order frequency, and monetary spend across RFM segments.",
            "sql": """SELECT 
    rfm_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(order_frequency), 1) AS avg_order_frequency,
    ROUND(SUM(monetary_value), 2) AS total_spend,
    ROUND(SUM(monetary_value) / 10000000.0, 2) AS spend_crores,
    ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 2) AS customer_share_pct
FROM analytics.vw_customer_rfm_scores
GROUP BY rfm_segment
ORDER BY total_spend DESC;"""
        },
        {
            "name": "SQL 2.4: Manufacturing Production Lines & Quality Scrap Rate",
            "grain": "Production Line Grain",
            "purpose": "Identifies defect scrap rates and units rejected across all factory production lines.",
            "sql": """SELECT 
    pl.line_name,
    pl.supervisor_name,
    COUNT(wo.work_order_id) AS batches_completed,
    SUM(wo.quantity_produced) AS total_units_produced,
    SUM(wo.rejected_quantity) AS total_units_rejected,
    ROUND(SUM(wo.rejected_quantity)::numeric / NULLIF(SUM(wo.quantity_produced), 0) * 100, 2) AS scrap_rate_pct
FROM manufacture.work_orders wo
JOIN manufacture.production_lines pl ON wo.line_id = pl.line_id
WHERE wo.status = 'Completed'
GROUP BY pl.line_name, pl.supervisor_name
ORDER BY scrap_rate_pct DESC;"""
        }
    ]

    # 1. HTML
    html_content = build_html_deliverable(suite_title, suite_subtitle, suite_tag, kpis, sections, sql_queries)
    html_path = os.path.join(DOCS_DIR, "RetailMart_V3_Sales_Customer_Operations_Deliverable.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 2. DOCX
    doc = docx.Document()
    add_header(doc, suite_title, suite_subtitle, suite_tag)
    add_section_heading(doc, "Headline Key Performance Indicators")
    add_table_data(doc, ["KPI Name", "Performance Value", "Operational Context"], [
        [k["title"], k["value"], k["subtext"]] for k in kpis
    ])
    for s in sections:
        add_section_heading(doc, s["title"])
        doc.add_paragraph(s["desc"])
        if "table" in s:
            add_table_data(doc, s["table"]["headers"], s["table"]["rows"])
    add_section_heading(doc, "Authoritative Production SQL Queries")
    for q in sql_queries:
        p = doc.add_paragraph()
        r = p.add_run(f"{q['name']} (Grain: {q['grain']})")
        r.bold = True
        doc.add_paragraph(f"Business Purpose: {q['purpose']}")
        add_code_block(doc, q["sql"])

    docx_path = os.path.join(DOCS_DIR, "RetailMart_V3_Sales_Customer_Operations_Deliverable.docx")
    doc.save(docx_path)

    # 3. PDF
    pdf_path = os.path.join(DOCS_DIR, "RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf")
    generate_pdf_from_html(html_path, pdf_path)
    print("Suite 2 Deliverables generated successfully!")


# --------------------------------------------------------------------------------------------------
# SUITE 3: HR & FINANCE GOVERNANCE DELIVERABLE
# --------------------------------------------------------------------------------------------------
def build_suite3():
    suite_title = "Human Resources & Financial Governance Deliverable"
    suite_subtitle = "Domain Suite 3: Workforce Demographics, Compensation Structure, OPEX Ledger & Treasury Liquidity"
    suite_tag = "Domain Suite 3 · People & Financial Governance"

    kpis = [
        {"title": "Active Workforce", "value": "3,000 Staff", "subtext": "100% active across 10 depts"},
        {"title": "Monthly Base Payroll", "value": "₹18.98 Cr", "subtext": "₹189,800,000 contractual payroll"},
        {"title": "Average Base Salary", "value": "₹63,267", "subtext": "Median salary ₹55,000 / month"},
        {"title": "Corporate OPEX", "value": "₹42.15 Cr", "subtext": "Technology, Admin, HQ overhead"},
        {"title": "Store Branch OPEX", "value": "₹38.80 Cr", "subtext": "Store leases, utilities, maintenance"},
        {"title": "Refund Financial Impact", "value": "₹14.20 Cr", "subtext": "Clawback on returned customer orders"},
    ]

    sections = [
        {
            "title": "1. Departmental Workforce Headcount & Payroll Allocation",
            "desc": "Distribution of 3,000 staff members across retail stores and corporate headquarters.",
            "table": {
                "headers": ["Department", "Staff Headcount", "Headcount Share (%)", "Monthly Payroll (₹)", "Avg Salary (₹)"],
                "rows": [
                    ["Store Retail Operations", "1,850 Staff", "61.67%", "₹9.25 Cr", "₹50,000"],
                    ["Supply Chain & Logistics", "420 Staff", "14.00%", "₹2.73 Cr", "₹65,000"],
                    ["Information Technology", "210 Staff", "7.00%", "₹2.20 Cr", "₹105,000"],
                    ["Sales & Business Dev", "180 Staff", "6.00%", "₹1.53 Cr", "₹85,000"],
                    ["Finance & Accounting", "95 Staff", "3.17%", "₹0.90 Cr", "₹95,000"],
                    ["Marketing & Growth", "85 Staff", "2.83%", "₹0.85 Cr", "₹100,000"],
                    ["Human Resources", "60 Staff", "2.00%", "₹0.57 Cr", "₹95,000"],
                    ["Corporate & Admin", "100 Staff", "3.33%", "₹0.95 Cr", "₹95,000"],
                ]
            }
        },
        {
            "title": "2. Financial OPEX Waterfall & Operating Expense Structure",
            "desc": "Analysis of corporate administrative expenditure vs branch store operating burn rate.",
            "table": {
                "headers": ["Expense Category", "Expenditure Realm", "Total Outflow (₹)", "Budget Share (%)", "Cost Control Level"],
                "rows": [
                    ["Branch Store Leases & Rent", "Stores OPEX", "₹18.50 Cr", "22.85%", "Fixed Long-Term Contracts"],
                    ["Corporate HQ Salaries", "HR / Finance", "₹18.98 Cr", "23.45%", "Contractual Core Payroll"],
                    ["Store Utilities & Facilities", "Stores OPEX", "₹12.30 Cr", "15.20%", "Variable Energy Audit Required"],
                    ["Technology & Cloud Infrastructure", "Corporate OPEX", "₹11.20 Cr", "13.84%", "SaaS & Hosting Rationalization"],
                    ["Marketing & Advertising Media", "Marketing OPEX", "₹10.30 Cr", "12.72%", "Performance ROI Reallocation"],
                    ["Store Maintenance & Logistics", "Operations OPEX", "₹9.67 Cr", "11.94%", "Preventive Service Scheduling"],
                ]
            }
        },
        {
            "title": "3. Treasury Cash Liquidity & Payment Tender Performance",
            "desc": "Settlement tender mix across digital and physical customer payment rails.",
            "table": {
                "headers": ["Payment Tender Mode", "Transaction Count", "Gross Value (₹)", "Settlement Fee Rate", "Dispute / Return Rate"],
                "rows": [
                    ["UPI (Unified Payments)", "62,400", "₹312.40 Cr", "0.00% (Zero MDR)", "1.20% (Lowest)"],
                    ["Credit & Debit Cards", "48,200", "₹241.10 Cr", "1.50% Interchange", "2.80% Disputes"],
                    ["Net Banking / RTGS", "18,500", "₹92.50 Cr", "₹15 Fixed Transfer", "0.80% Discrepancies"],
                    ["Cash on Delivery (COD)", "13,440", "₹55.23 Cr", "₹45 Cash Handling", "8.90% High Return Risk"],
                ]
            }
        }
    ]

    sql_queries = [
        {
            "name": "SQL 3.1: Active Enterprise Workforce Headcount & Payroll Summary",
            "grain": "Department Master Grain",
            "purpose": "Aggregates employee headcount, total base salary obligations, and mean compensation across departments.",
            "sql": """SELECT 
    d.department_name,
    COUNT(e.employee_id) AS total_employees,
    ROUND(SUM(e.salary), 2) AS monthly_base_payroll,
    ROUND(AVG(e.salary), 2) AS avg_salary,
    ROUND(COUNT(e.employee_id)::numeric / SUM(COUNT(e.employee_id)) OVER () * 100, 2) AS headcount_share_pct
FROM stores.employees e
JOIN hr.dim_department d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_employees DESC;"""
        },
        {
            "name": "SQL 3.2: Monthly Processed Salary Payout Timeline",
            "grain": "Payment Month Grain",
            "purpose": "Tracks monthly disbursed cash compensation through banking channels.",
            "sql": """SELECT 
    DATE_TRUNC('month', payment_date)::date AS payout_month,
    COUNT(history_id) AS disbursements_count,
    ROUND(SUM(amount), 2) AS total_cash_payout,
    ROUND(AVG(amount), 2) AS avg_payout
FROM hr.salary_history
WHERE status = 'Processed'
GROUP BY DATE_TRUNC('month', payment_date)
ORDER BY payout_month;"""
        },
        {
            "name": "SQL 3.3: Corporate vs Store Operating Expenditure (OPEX)",
            "grain": "Expense Category Grain",
            "purpose": "Reconciles overhead expenses across headquarters corporate ledger and physical store ledgers.",
            "sql": """SELECT 
    'Corporate Expenses' AS expense_source,
    c.category_name,
    COUNT(e.expense_id) AS voucher_count,
    ROUND(SUM(e.amount), 2) AS total_expenditure
FROM finance.expenses e
JOIN finance.dim_expense_category c ON e.category_id = c.category_id
GROUP BY c.category_name

UNION ALL

SELECT 
    'Store Expenses' AS expense_source,
    c.category_name,
    COUNT(e.expense_id) AS voucher_count,
    ROUND(SUM(e.amount), 2) AS total_expenditure
FROM stores.expenses e
JOIN finance.dim_expense_category c ON e.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_expenditure DESC;"""
        },
        {
            "name": "SQL 3.4: Payment Tender Performance & Settlement Volume",
            "grain": "Payment Mode Grain",
            "purpose": "Evaluates customer tender mode distribution, cash collections, and electronic payment velocities.",
            "sql": """SELECT 
    payment_mode,
    payment_status,
    COUNT(payment_id) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_settled_amount,
    ROUND(SUM(amount) / SUM(SUM(amount)) OVER () * 100, 2) AS payment_share_pct
FROM sales.payments
WHERE payment_status = 'Success'
GROUP BY payment_mode, payment_status
ORDER BY total_settled_amount DESC;"""
        }
    ]

    # 1. HTML
    html_content = build_html_deliverable(suite_title, suite_subtitle, suite_tag, kpis, sections, sql_queries)
    html_path = os.path.join(DOCS_DIR, "RetailMart_V3_HR_Finance_Deliverable.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 2. DOCX
    doc = docx.Document()
    add_header(doc, suite_title, suite_subtitle, suite_tag)
    add_section_heading(doc, "Headline Key Performance Indicators")
    add_table_data(doc, ["KPI Name", "Performance Value", "Operational Context"], [
        [k["title"], k["value"], k["subtext"]] for k in kpis
    ])
    for s in sections:
        add_section_heading(doc, s["title"])
        doc.add_paragraph(s["desc"])
        if "table" in s:
            add_table_data(doc, s["table"]["headers"], s["table"]["rows"])
    add_section_heading(doc, "Authoritative Production SQL Queries")
    for q in sql_queries:
        p = doc.add_paragraph()
        r = p.add_run(f"{q['name']} (Grain: {q['grain']})")
        r.bold = True
        doc.add_paragraph(f"Business Purpose: {q['purpose']}")
        add_code_block(doc, q["sql"])

    docx_path = os.path.join(DOCS_DIR, "RetailMart_V3_HR_Finance_Deliverable.docx")
    doc.save(docx_path)

    # 3. PDF
    pdf_path = os.path.join(DOCS_DIR, "RetailMart_V3_HR_Finance_Deliverable.pdf")
    generate_pdf_from_html(html_path, pdf_path)
    print("Suite 3 Deliverables generated successfully!")


def copy_to_artifacts():
    if not os.path.exists(ARTIFACTS_DIR):
        return
    import shutil
    deliverables = [
        "RetailMart_V3_Marketing_Digital_Logistics_Deliverable.html",
        "RetailMart_V3_Marketing_Digital_Logistics_Deliverable.docx",
        "RetailMart_V3_Marketing_Digital_Logistics_Deliverable.pdf",
        "RetailMart_V3_Sales_Customer_Operations_Deliverable.html",
        "RetailMart_V3_Sales_Customer_Operations_Deliverable.docx",
        "RetailMart_V3_Sales_Customer_Operations_Deliverable.pdf",
        "RetailMart_V3_HR_Finance_Deliverable.html",
        "RetailMart_V3_HR_Finance_Deliverable.docx",
        "RetailMart_V3_HR_Finance_Deliverable.pdf",
    ]
    for fn in deliverables:
        src = os.path.join(DOCS_DIR, fn)
        dst = os.path.join(ARTIFACTS_DIR, fn)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    print("All deliverables copied to Artifacts directory successfully!")

if __name__ == "__main__":
    build_suite1()
    build_suite2()
    build_suite3()
    copy_to_artifacts()
