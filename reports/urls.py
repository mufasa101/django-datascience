from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='main'),
    path('save/', views.create_report_view, name='create-report'),
    path('<pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('<pk>/pdf/', views.render_pdf_view, name='pdf'),
]
 
