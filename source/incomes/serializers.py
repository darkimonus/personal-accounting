from rest_framework import serializers
from incomes.models import IncomeSource, IncomeTax, IncomeTransaction


class BaseIncomeSerializer(serializers.ModelSerializer):
    transactions = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    class Meta:
        fields = ['name', 'description', 'transactions', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'transactions'):
            representation['transactions'] = instance.transactions
        return representation

    def validate_name(self, value):
        user = self.context['request'].user
        model = self.Meta.model
        if model.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError(
                f"{model._meta.verbose_name} with the name '{value}' already exists."
            )
        return value


class IncomeSourceSerializer(BaseIncomeSerializer):

    class Meta(BaseIncomeSerializer.Meta):
        model = IncomeSource
        fields = BaseIncomeSerializer.Meta.fields + ['link']


class IncomeTaxSerializer(BaseIncomeSerializer):

    class Meta(BaseIncomeSerializer.Meta):
        model = IncomeTax
        fields = BaseIncomeSerializer.Meta.fields + ['rate']


class IncomeTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeTransaction
        fields = '__all__'
