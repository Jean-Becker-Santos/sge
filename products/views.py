import csv
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from openpyxl import Workbook
from products.models import Product
from . import forms 
from brands.models import Brand
from categories.models import Category

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        serie_number = self.request.GET.get('serie_number')

        if title:
            queryset = queryset.filter(title__icontains=title)
        
        if category:
            queryset = queryset.filter(category__id=category)
        
        if brand:
            queryset = queryset.filter(brand__id=brand)
        
        if serie_number:
            queryset = queryset.filter(brand__id=serie_number)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        
        return context

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_create.html' 
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_update.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


class ProductCSVExportView(View):
    """
    Retorna um arquivo CSV contendo a lista de 'product', 
    mas respeitando o mesmo filtro usado na productListView.
    """
    def get(self, request, *args, **kwargs):
        # 1. Capturar o parâmetro 'name' da URL (caso exista).
        name = request.GET.get('name', '')

        # 2. Iniciar o QuerySet e aplicar o filtro, se houver.
        queryset = Product.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)

        # 3. Cria o HttpResponse com content_type de CSV e charset UTF-8
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        # 4. Define o cabeçalho para download
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        # 5. Escreve o BOM para garantir reconhecimento de UTF-8 por aplicativos como Excel
        response.write('\ufeff')  # BOM

        writer = csv.writer(response)
        # Cabeçalho do CSV
        writer.writerow(['ID', 'Nome', 'Descrição'])

        # 6. Escreve as linhas com base no QuerySet filtrado
        for product in queryset:
            writer.writerow([
                product.id,
                product.name,
                product.description
            ])

        return response


class ProductExcelExportView(View):
    """
    Retorna um arquivo Excel (XLSX) contendo a lista de 'product', 
    mas respeitando o mesmo filtro usado na productListView.
    """
    def get(self, request, *args, **kwargs):
        # 1. Capturar o parâmetro 'name' da URL (caso exista).
        name = request.GET.get('name', '')

        # 2. Iniciar o QuerySet e aplicar o filtro, se houver.
        queryset = Product.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)

        # 3. Cria uma planilha nova
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "products"

        # Define o cabeçalho
        worksheet['A1'] = 'ID'
        worksheet['B1'] = 'Nome'
        worksheet['C1'] = 'Descrição'

        # 4. Preenche os dados filtrados
        row_num = 2
        for product in queryset:
            worksheet.cell(row=row_num, column=1, value=product.id)
            worksheet.cell(row=row_num, column=2, value=product.name)
            worksheet.cell(row=row_num, column=3, value=product.description)
            row_num += 1

        # 5. Prepara o HttpResponse para enviar como arquivo .xlsx
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
        workbook.save(response)

        return response

