from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        
    return JsonResponse({
        "status": "ok" if db_status == "healthy" else "degraded",
        "database": db_status,
        "platform": "RetailMart V3 Analytics"
    })

def root_redirect(request):
    return redirect('executive_summary')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('', root_redirect, name='root_redirect'),
    path('', include('dashboard.urls')),
]

handler404 = 'dashboard.views.auth_views.custom_404'
handler500 = 'dashboard.views.auth_views.custom_500'
