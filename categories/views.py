import csv
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from openpyxl import Workbook
from categories.models import Category
from . import forms 

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category_create.html' 
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category_update.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category_list')


class CategoryCSVExportView(View):
    """
    Retorna um arquivo CSV contendo a lista de 'Category', 
    mas respeitando o mesmo filtro usado na CategoryListView.
    """
    def get(self, request, *args, **kwargs):
        # 1. Capturar o parâmetro 'name' da URL (caso exista).
        name = request.GET.get('name', '')

        # 2. Iniciar o QuerySet e aplicar o filtro, se houver.
        queryset = Category.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)

        # 3. Cria o HttpResponse com content_type de CSV
        response = HttpResponse(content_type='text/csv')
        # 4. Define o cabeçalho para download
        response['Content-Disposition'] = 'attachment; filename="categories.csv"'

        writer = csv.writer(response)
        # Cabeçalho do CSV
        writer.writerow(['ID', 'Nome', 'Descrição'])

        # 5. Escreve as linhas com base no QuerySet filtrado
        for category in queryset:
            writer.writerow([category.id, category.name, category.description])

        return response


class CategoryExcelExportView(View):
    """
    Retorna um arquivo Excel (XLSX) contendo a lista de 'Category', 
    mas respeitando o mesmo filtro usado na CategoryListView.
    """
    def get(self, request, *args, **kwargs):
        # 1. Capturar o parâmetro 'name' da URL (caso exista).
        name = request.GET.get('name', '')

        # 2. Iniciar o QuerySet e aplicar o filtro, se houver.
        queryset = Category.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)

        # 3. Cria uma planilha nova
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Categories"

        # Define o cabeçalho
        worksheet['A1'] = 'ID'
        worksheet['B1'] = 'Nome'
        worksheet['C1'] = 'Descrição'

        # 4. Preenche os dados filtrados
        row_num = 2
        for category in queryset:
            worksheet.cell(row=row_num, column=1, value=category.id)
            worksheet.cell(row=row_num, column=2, value=category.name)
            worksheet.cell(row=row_num, column=3, value=category.description)
            row_num += 1

        # 5. Prepara o HttpResponse para enviar como arquivo .xlsx
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="categories.xlsx"'
        workbook.save(response)

        return response
