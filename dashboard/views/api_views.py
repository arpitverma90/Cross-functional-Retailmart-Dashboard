import os
from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import get_filter_options
from dashboard.services.simulator_service import get_simulator_baseline

@login_required
def api_cascade_stores(request):
    """Return stores belonging to a selected region for cascading dropdown."""
    region_id = request.GET.get('region_id')
    filter_data = get_filter_options(selected_region=region_id)
    return JsonResponse({'stores': filter_data['stores']})


@login_required
def api_simulator_baseline(request):
    """API endpoint to get baseline parameters for scenario simulator."""
    baseline = get_simulator_baseline()
    return JsonResponse(baseline)


def download_word_doc(request):
    """Download the master Word document containing all Domain KPI and EDA SQL queries."""
    doc_path = os.path.join(settings.BASE_DIR, 'project_documents', 'documentation', 'RetailMart_V3_Master_KPI_and_EDA_SQL_Queries.docx')
    if not os.path.exists(doc_path):
        doc_path = os.path.join(settings.BASE_DIR, 'project_documents', 'documentation', 'approved_kpi_and_eda_queries.docx')
    if os.path.exists(doc_path):
        return FileResponse(
            open(doc_path, 'rb'),
            as_attachment=True,
            filename='RetailMart_V3_Master_KPI_and_EDA_SQL_Queries.docx',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    raise Http404("Query catalogue document not found.")


def download_github_zip(request):
    """Download the complete, clean GitHub-ready repository zip archive."""
    zip_path = os.path.join(settings.BASE_DIR, 'retailmart_bi_github.zip')
    if os.path.exists(zip_path):
        return FileResponse(
            open(zip_path, 'rb'),
            as_attachment=True,
            filename='retailmart_bi_github.zip',
            content_type='application/zip'
        )
    raise Http404("Repository archive not found.")


def download_insights_pdf(request):
    """Download the Executive Insights Report as a high-fidelity PDF."""
    pdf_path = os.path.join(settings.BASE_DIR, 'project_documents', 'documentation', 'RetailMart_V3_Executive_Insights_Report.pdf')
    if os.path.exists(pdf_path):
        return FileResponse(
            open(pdf_path, 'rb'),
            as_attachment=True,
            filename='RetailMart_V3_Executive_Insights_Report.pdf',
            content_type='application/pdf'
        )
    raise Http404("PDF Insights report not found.")


def download_insights_word(request):
    """Download the Executive Insights Report as a Word document (.docx)."""
    docx_path = os.path.join(settings.BASE_DIR, 'project_documents', 'documentation', 'RetailMart_V3_Executive_Insights_Report.docx')
    if os.path.exists(docx_path):
        return FileResponse(
            open(docx_path, 'rb'),
            as_attachment=True,
            filename='RetailMart_V3_Executive_Insights_Report.docx',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    raise Http404("Word Insights report not found.")


def download_insights_html(request):
    """Download or view the standalone interactive Executive Insights HTML report."""
    html_path = os.path.join(settings.BASE_DIR, 'project_documents', 'documentation', 'RetailMart_V3_Executive_Insights_Report.html')
    if os.path.exists(html_path):
        as_attachment = request.GET.get('attachment', 'false').lower() == 'true'
        return FileResponse(
            open(html_path, 'rb'),
            as_attachment=as_attachment,
            filename='RetailMart_V3_Executive_Insights_Report.html',
            content_type='text/html; charset=utf-8'
        )
    raise Http404("HTML Insights report not found.")
