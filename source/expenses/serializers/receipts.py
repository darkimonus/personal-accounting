from rest_framework import serializers

from expenses.models import Receipt
from .receipt_items import ReceiptItemSerializer


class ReceiptSerializer(serializers.ModelSerializer):
    receipt_items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['id', 'date', 'store_name', 'receipt_items', 'created_at', 'total_price', 'calculate_total']
        read_only_fields = ['id', 'created_at']


class RetrieveReceiptSerializer(serializers.ModelSerializer):
    receipt_items = ReceiptItemSerializer(source='items', many=True)
    items_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Receipt
        fields = ['id', 'date', 'store_name', 'receipt_items', 'created_at', 'total_price', 'calculate_total',
                  'items_count']
        read_only_fields = ['id', 'created_at', 'items_count']
