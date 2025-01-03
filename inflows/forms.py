from django import forms
from . import models


class InflowForm(forms.ModelForm):

    class Meta:
        model = models.Inflow
        fields = ['supplier', 'product', 'quantity','description']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'Quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            }
        labels = {
            'product': 'Produto',
            'supplier': 'Fornecedor',
            'quantity': 'Quantidade',
            'description': 'Descrição'
        }
