from django.urls import path
from . import views

urlpatterns = [
    path('outflows/list/', views.OutflowListView.as_view(), name='outflow_list'),
    path('outflows/create/', views.OutflowCreateView.as_view(), name='outflow_create'),
    path('outflows/<int:pk>/detail/', views.OutflowDetailView.as_view(), name='outflow_detail'),
    path('outflows/export_csv/', views.OutflowCSVExportView.as_view(), name='outflow_csv_export'),
    path('outflows/export_excel/', views.OutflowExcelExportView.as_view(), name='outflow_excel_export'),
]
