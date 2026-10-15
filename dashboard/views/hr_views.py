"""
RetailMart V3 - Human Resources Domain Views
Handles request routing, filter parsing, and context assembling for HR analytics:
- Headcount, demographics, and compensation structures
- Attendance compliance proxy and shift distributions
- Monthly processed salary payouts and store staffing distributions
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.filter_service import parse_filters, get_filter_options
from dashboard.services import hr_service


@login_required
def hr_dashboard_view(request):
    """HR & Workforce Analytics Controller (/business-dashboard/hr/)"""
    filters = parse_filters(request)
    filter_options = get_filter_options(selected_region=filters.get('region_id'))

    kpis = hr_service.get_hr_kpi_summary(filters)
    dept_workforce = hr_service.get_workforce_by_department(filters)
    role_workforce = hr_service.get_workforce_by_role(filters)
    attendance_trend = hr_service.get_attendance_monthly_summary(filters)
    shift_dist = hr_service.get_shift_duration_distribution(filters)
    comp_structure = hr_service.get_payroll_compensation_structure(filters)
    disbursement_trend = hr_service.get_salary_disbursement_timeline(filters)
    store_staffing = hr_service.get_store_staffing_table(filters)
    hiring_cadence = hr_service.get_hiring_cadence_timeline(filters)

    context = {
        'page_title': 'Human Resources & Workforce Intelligence',
        'active_tab': 'hr',
        'filters': filters,
        'filter_options': filter_options,
        'kpis': kpis,
        'dept_workforce': dept_workforce,
        'role_workforce': role_workforce,
        'attendance_trend': attendance_trend,
        'shift_dist': shift_dist,
        'comp_structure': comp_structure,
        'disbursement_trend': disbursement_trend,
        'store_staffing': store_staffing,
        'hiring_cadence': hiring_cadence,
    }
    return render(request, 'dashboard/hr.html', context)
