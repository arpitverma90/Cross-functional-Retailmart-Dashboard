from django.urls import path
from django.shortcuts import redirect
from dashboard.views import (
    auth_views,
    executive_views,
    hr_views,
    finance_views,
    cross_views,
    api_views,
    marketing_views,
    digital_views,
    logistics_views,
    commercial_views
)

urlpatterns = [
    # Authentication
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Area 1: Executive Summary
    path('executive-summary/', executive_views.executive_summary_view, name='executive_summary'),
    
    # Domain Suite 1: Growth & Supply Chain
    path('business-dashboard/marketing/', marketing_views.marketing_dashboard_view, name='marketing_dashboard'),
    path('marketing/', marketing_views.marketing_dashboard_view, name='marketing_shortcut'),
    path('business-dashboard/digital/', digital_views.digital_dashboard_view, name='digital_dashboard'),
    path('digital/', digital_views.digital_dashboard_view, name='digital_shortcut'),
    path('business-dashboard/logistics/', logistics_views.logistics_dashboard_view, name='logistics_dashboard'),
    path('logistics/', logistics_views.logistics_dashboard_view, name='logistics_shortcut'),

    # Domain Suite 2: Commercial & Customer Operations
    path('business-dashboard/sales/', commercial_views.sales_dashboard_view, name='sales_dashboard'),
    path('sales/', commercial_views.sales_dashboard_view, name='sales_shortcut'),
    path('business-dashboard/customers/', commercial_views.customer_dashboard_view, name='customer_dashboard'),
    path('customers/', commercial_views.customer_dashboard_view, name='customer_shortcut'),
    path('business-dashboard/operations/', commercial_views.operations_dashboard_view, name='operations_dashboard'),
    path('operations/', commercial_views.operations_dashboard_view, name='operations_shortcut'),

    # Domain Suite 3: People & Financial Governance
    path('business-dashboard/hr/', hr_views.hr_dashboard_view, name='hr_dashboard'),
    path('hr/', hr_views.hr_dashboard_view, name='hr_shortcut'),
    path('business-dashboard/finance/', finance_views.finance_dashboard_view, name='finance_dashboard'),
    path('finance/', finance_views.finance_dashboard_view, name='finance_shortcut'),

    # Cross-Functional & Scenario Simulator
    path('business-dashboard/', lambda r: redirect('hr_dashboard'), name='business_dashboard_root'),
    path('business-dashboard/cross-functional/', cross_views.cross_functional_dashboard_view, name='cross_functional_dashboard'),
    path('cross-functional/', cross_views.cross_functional_dashboard_view, name='cross_functional_shortcut'),
    path('business-dashboard/simulator/', cross_views.simulator_view, name='scenario_simulator'),
    path('simulator/', cross_views.simulator_view, name='simulator_shortcut'),
    
    # API endpoints for dynamic cascading filters & scenario simulation
    path('api/stores/', api_views.api_cascade_stores, name='api_cascade_stores'),
    path('api/cascade-stores/', api_views.api_cascade_stores, name='api_cascade_stores_alias'),
    path('api/simulator-baseline/', api_views.api_simulator_baseline, name='api_simulator_baseline'),
    
    # Domain Suite Deliverable Downloads
    # Suite 1: Marketing, Digital & Logistics
    path('download/suite1-pdf/', api_views.download_suite1_pdf, name='download_suite1_pdf'),
    path('download/suite1-word/', api_views.download_suite1_word, name='download_suite1_word'),
    path('download/suite1-html/', api_views.download_suite1_html, name='download_suite1_html'),

    # Suite 2: Sales, Customer & Operations
    path('download/suite2-pdf/', api_views.download_suite2_pdf, name='download_suite2_pdf'),
    path('download/suite2-word/', api_views.download_suite2_word, name='download_suite2_word'),
    path('download/suite2-html/', api_views.download_suite2_html, name='download_suite2_html'),

    # Suite 3: HR & Finance
    path('download/suite3-pdf/', api_views.download_suite3_pdf, name='download_suite3_pdf'),
    path('download/suite3-word/', api_views.download_suite3_word, name='download_suite3_word'),
    path('download/suite3-html/', api_views.download_suite3_html, name='download_suite3_html'),

    # Executive Insights & Technical Deliverables
    path('download/insights-pdf/', api_views.download_insights_pdf, name='download_insights_pdf'),
    path('download/insights-word/', api_views.download_insights_word, name='download_insights_word'),
    path('download/insights-html/', api_views.download_insights_html, name='download_insights_html'),
    path('download/word-doc/', api_views.download_word_doc, name='download_word_doc'),
    path('download/github-zip/', api_views.download_github_zip, name='download_github_zip'),
]
