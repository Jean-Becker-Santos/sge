from django.contrib import admin
from . import models


class InflowAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'quantity', 'created_at', 'description',)
    search_fields = ('supplier_name', 'product__title',)

admin.site.register(models.Inflow, InflowAdmin)