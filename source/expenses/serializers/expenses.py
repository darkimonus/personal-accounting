from rest_framework import serializers

from expenses.models import Expense, Receipt
from .receipts import RetrieveReceiptSerializer


class ExpenseReceiptsIdSerializer(serializers.ModelSerializer):
    receipts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Receipt.objects.all(),
        required=False
    )

    class Meta:
        model = Expense
        fields = ['id', 'name', 'date', 'total_amount', 'receipts', 'created_at', 'calculate_total']
        required_fields = ['name', 'date']
        read_only_fields = ['id', 'created_at',]
        depth = 1


class RetrieveExpenseSerializer(serializers.ModelSerializer):
    receipts = RetrieveReceiptSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'name', 'date', 'total_amount', 'receipts', 'created_at']
        read_only_fields = ['id', 'created_at', ]
        depth = 1


class RetrieveNoReceiptsExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'name', 'date', 'total_amount', 'created_at']
        read_only_fields = ['id', 'created_at', ]
