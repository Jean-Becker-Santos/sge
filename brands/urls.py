from django.urls import path
from . import views

urlpatterns = [
    path('brands/list/', views.BrandListView.as_view(), name='brand_list'),
    path('brands/create/', views.BrandCreateView.as_view(), name='brand_create'),
    path('brands/<int:pk>/detail/', views.BrandDetailView.as_view(), name='brand_detail'),
    path('brands/<int:pk>/update/', views.BrandUpdateView.as_view(), name='brand_update'),
    path('brands/<int:pk>/delete/', views.BrandDeleteView.as_view(), name='brand_delete'),
    path('brands/export_csv/', views.BrandCSVExportView.as_view(), name='brand_csv_export'),
    path('brands/export_excel/', views.BrandExcelExportView.as_view(), name='brand_excel_export'),
    path('api/v1/brands/', views.BrandCreateListAPIView.as_view(), name='brand_create_list_api_view'),
    path('api/v1/brands/<int:pk>/', views.BrandRetrieveUpdateDestroyView.as_view(), name='brand_retrieve_delete_api_view'), ]
