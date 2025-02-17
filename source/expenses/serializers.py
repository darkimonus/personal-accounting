from rest_framework import serializers
from expenses.models import Receipt, ReceiptItem, Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'name', 'unit_type', 'category', 'manufacturer_url', 'description', 'brand', 'created_at']
        read_only_fields = ['id', 'created_at', 'manufacturer_url', 'description']


class ReceiptItemSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer()

    class Meta:
        model = ReceiptItem
        fields = ['purchase', 'unit_price', 'quantity', 'total_price', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'unit_price']


class RetrieveReceiptItemSerializer(serializers.ModelSerializer):
    purchase = purchase = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all())

    class Meta:
        model = ReceiptItem
        fields = ['purchase', 'unit_price', 'quantity', 'total_price', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'unit_price']


class ReceiptSerializer(serializers.ModelSerializer):
    receipt_items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['id', 'date', 'store_name', 'receipt_items', 'created_at', 'total_price', 'calculate_total']
        read_only_fields = ['id', 'created_at']


class RetrieveReceiptSerializer(serializers.ModelSerializer):
    receipt_items = RetrieveReceiptItemSerializer(source='items', many=True)

    class Meta:
        model = Receipt
        fields = ['id', 'date', 'store_name', 'receipt_items', 'created_at', 'total_price', 'calculate_total']
        read_only_fields = ['id', 'created_at']
