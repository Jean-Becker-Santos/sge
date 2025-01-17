from django.db.models import Sum, F
from django.utils import timezone
from django.utils.formats import number_format
from django.core.cache import cache

from brands.models import Brand
from categories.models import Category
from products.models import Product
from outflows.models import Outflow


def get_product_metrics():
    """Métricas gerais de produtos."""
    data = cache.get('product_metrics')

    if data is None:
        products = Product.objects.all()
        total_cost_price = sum(p.cost_price * p.quantity for p in products)
        total_selling_price = sum(p.selling_price * p.quantity for p in products)
        total_quantity = sum(p.quantity for p in products)
        total_profit = total_selling_price - total_cost_price

        data = dict(
            total_cost_price=number_format(total_cost_price, decimal_pos=2, force_grouping=True),
            total_selling_price=number_format(total_selling_price, decimal_pos=2, force_grouping=True),
            total_quantity=total_quantity,
            total_profit=number_format(total_profit, decimal_pos=2, force_grouping=True),
        )
        cache.set('product_metrics', data)

    return data


def get_sales_metrics():
    """Métricas gerais de vendas."""
    data = cache.get('sales_metrics')

    if data is None:
        # total_sales = quantidade de registros de vendas (Outflow) -> "Quantidade de Vendas"
        total_sales = Outflow.objects.count()

        # total_products_sold = soma total de produtos vendidos -> "Produtos Vendidos"
        total_products_sold = Outflow.objects.aggregate(
            total_products_sold=Sum('quantity')
        )['total_products_sold'] or 0

        # Para evitar muitas consultas, use select_related:
        outflows = Outflow.objects.select_related('product').only(
            'quantity', 'product__selling_price', 'product__cost_price'
        )

        total_sales_value = sum(o.quantity * o.product.selling_price for o in outflows)
        total_sales_cost = sum(o.quantity * o.product.cost_price for o in outflows)
        total_sales_profit = total_sales_value - total_sales_cost

        # Formata os valores com separador de milhar onde necessário:
        data = dict(
            total_sales=number_format(total_sales, decimal_pos=0, force_grouping=True),
            total_products_sold=number_format(total_products_sold, decimal_pos=0, force_grouping=True),
            total_sales_value=number_format(total_sales_value, decimal_pos=2, force_grouping=True),
            total_sales_profit=number_format(total_sales_profit, decimal_pos=2, force_grouping=True),
        )

        cache.set('sales_metrics', data)

    return data


def get_daily_sales_data():
    """Retorna os valores de vendas diárias dos últimos 7 dias."""
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    values = []

    for date in dates:
        sales_total = (
            Outflow.objects
                   .filter(created_at__date=date)
                   .aggregate(total_sales=Sum(F('product__selling_price') * F('quantity')))
                   .get('total_sales') or 0
        )
        values.append(float(sales_total))

    return dict(dates=dates, values=values)


def get_daily_sales_quantity_data():
    """Retorna a quantidade de vendas diárias (em unidades) dos últimos 7 dias."""
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    quantities = []

    for date in dates:
        sales_quantity = Outflow.objects.filter(created_at__date=date).count()
        # Formata a quantidade com separador de milhar
        formatted_quantity = number_format(sales_quantity, decimal_pos=0, force_grouping=True)
        quantities.append(formatted_quantity)
    return dict(dates=dates, values=quantities)


def get_graphic_product_category_metric():
    """Retorna a contagem de produtos por categoria (para gráficos)."""
    categories = Category.objects.all()
    return {
        category.name: Product.objects.filter(category=category).count()
        for category in categories
    }


def get_graphic_product_brand_metric():
    """Retorna a contagem de produtos por marca (para gráficos)."""
    brands = Brand.objects.all()
    return {
        brand.name: number_format(
            Product.objects.filter(brand=brand).count(),
            decimal_pos=0,
            force_grouping=True
        )
        for brand in brands
    }
