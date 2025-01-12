from django.urls import path
from . import views

urlpatterns = [
    path('suppliers/list/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/detail/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    path('suppliers/export_csv/', views.SupplierCSVExportView.as_view(), name='supplier_csv_export'),
    path('suppliers/export_excel/', views.SupplierExcelExportView.as_view(), name='supplier_excel_export'),

    path('api/v1/suppliers/', views.SupplierCreateListAPIView.as_view(), name='supplier_create_list_api_view'),
    path('api/v1/suppliers/<int:pk>/', views.SupplierRetrieveUpdateDestroyView.as_view(), name='supplier_retrieve_delete_api_view'),
]
