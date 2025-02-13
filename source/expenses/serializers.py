from rest_framework import serializers
from expenses.models import Receipt, ReceiptItem, Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['name', 'brand', 'unit_type', 'category', 'manufacturer_url', 'description']

    @staticmethod
    def create_or_get(validated_data):
        purchase, created = Purchase.objects.get_or_create(
            name=validated_data.get('name'),
            brand=validated_data.get('brand', ''),
            unit_type=validated_data.get('unit_type'),
            defaults={
                'category': validated_data.get('category', 'other'),
                'manufacturer_url': validated_data.get('manufacturer_url', ''),
                'description': validated_data.get('description', '')
            }
        )
        return purchase


class ReceiptItemSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer()

    class Meta:
        model = ReceiptItem
        fields = ['purchase', 'quantity', 'unit_price', 'total_price']

    def create(self, validated_data):
        purchase_data = validated_data.pop('purchase')
        purchase = PurchaseSerializer.create_or_get(purchase_data)
        user = self.context['request'].user
        receipt_item = ReceiptItem.objects.create(
            user=user,
            purchase=purchase,
            **validated_data
        )
        return receipt_item


class ReceiptSerializer(serializers.ModelSerializer):
    receipt_items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['date', 'store_name', 'receipt_items']

    def create(self, validated_data):
        receipt_items_data = validated_data.pop('receipt_items')
        user = self.context['request'].user
        receipt = Receipt.objects.create(user=user, **validated_data)
        receipt_items = [ReceiptItemSerializer().create(item_data) for item_data in receipt_items_data]
        receipt.receipt_items.add(*receipt_items)

        return receipt
