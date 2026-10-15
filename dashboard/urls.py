from django.urls import path
from django.shortcuts import redirect
from dashboard.views import (
    auth_views,
    executive_views,
    sales_views,
    customer_views,
    operations_views,
    cross_views,
    api_views
)

urlpatterns = [
    # Authentication
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Area 1: Executive Summary
    path('executive-summary/', executive_views.executive_summary_view, name='executive_summary'),
    
    # Area 2: Detailed Business Dashboard & Domain Routes
    path('business-dashboard/', lambda r: redirect('sales_dashboard'), name='business_dashboard_root'),
    path('business-dashboard/sales/', sales_views.sales_dashboard_view, name='sales_dashboard'),
    path('business-dashboard/customers/', customer_views.customer_dashboard_view, name='customer_dashboard'),
    path('business-dashboard/operations/', operations_views.operations_dashboard_view, name='operations_dashboard'),
    path('business-dashboard/cross-functional/', cross_views.cross_functional_dashboard_view, name='cross_functional_dashboard'),
    path('business-dashboard/simulator/', cross_views.simulator_view, name='scenario_simulator'),
    
    # API endpoints for interactive filtering & simulation
    path('api/stores/', api_views.api_cascade_stores, name='api_cascade_stores'),
    path('api/simulator-baseline/', api_views.api_simulator_baseline, name='api_simulator_baseline'),
    
    # Download Endpoints
    path('download/word-doc/', api_views.download_word_doc, name='download_word_doc'),
    path('download/github-zip/', api_views.download_github_zip, name='download_github_zip'),
    path('download/insights-pdf/', api_views.download_insights_pdf, name='download_insights_pdf'),
    path('download/insights-word/', api_views.download_insights_word, name='download_insights_word'),
    path('download/insights-html/', api_views.download_insights_html, name='download_insights_html'),
]
