from rest_framework import serializers

from expenses.models import ReceiptItem
from .purchases import PurchaseSerializer


class ReceiptItemSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer()

    class Meta:
        model = ReceiptItem
        fields = ['purchase', 'unit_price', 'quantity', 'total_price', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'unit_price']
