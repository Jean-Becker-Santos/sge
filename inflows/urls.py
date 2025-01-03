from django.urls import path
from . import views

urlpatterns = [
    path('inflows/list/', views.InflowListView.as_view(), name='inflow_list'),
    path('inflows/create/', views.InflowCreateView.as_view(), name='inflow_create'),
    path('inflows/<int:pk>/detail/', views.InflowDetailView.as_view(), name='inflow_detail'),
    path('inflows/export_csv/', views.InflowCSVExportView.as_view(), name='inflow_csv_export'),
    path('inflows/export_excel/', views.InflowExcelExportView.as_view(), name='inflow_excel_export'),
]
