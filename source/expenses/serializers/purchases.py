from rest_framework import serializers
from expenses.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'name', 'unit_type', 'category', 'manufacturer_url', 'description', 'brand', 'created_at']
        read_only_fields = ['id', 'created_at', 'manufacturer_url', 'description']
        validators = []
