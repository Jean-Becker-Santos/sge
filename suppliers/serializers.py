from rest_framework import serializers
from . import models


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Supplier
        fields = '__all__'
