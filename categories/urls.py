from django.urls import path
from . import views

urlpatterns = [
    path('categories/list/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/detail/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/export_csv/', views.CategoryCSVExportView.as_view(), name='category_csv_export'),
    path('categories/export_excel/', views.CategoryExcelExportView.as_view(), name='category_excel_export'),
    path('api/v1/categories/', views.CategoryCreateListAPIView.as_view(), name='category_create_list_api_view'),
    path('api/v1/categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category_retrieve_delete_api_view'), ]
