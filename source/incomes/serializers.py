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


class TaxField(serializers.RelatedField):

    def to_internal_value(self, data):
        if isinstance(data, int):
            return IncomeTax.objects.get(id=data)
        elif isinstance(data, str):
            return IncomeTax.objects.get(name=data)
        raise serializers.ValidationError("Tax must be provided as ID or name.")

    def to_representation(self, obj):
        return {"name": obj.name, "rate": obj.rate}


class IncomeTransactionSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(
        queryset=IncomeSource.objects.all(), required=False, allow_null=True
    )
    taxes = TaxField(queryset=IncomeTax.objects.all(), many=True, required=False)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')
    total_after_taxes = serializers.SerializerMethodField()
    taxes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = IncomeTransaction
        fields = ['id', 'source', 'amount', 'date', 'taxes', 'total_after_taxes', 'created_at', 'taxes_count']
        read_only_fields = ['total_after_taxes', 'created_at', 'taxes_count']

    def get_total_after_taxes(self, obj):
        total_tax_rate = sum(tax.rate for tax in obj.taxes.all())
        return obj.amount * (1 - total_tax_rate)

    def validate(self, data):
        if data.get('amount', 0) <= 0:
            raise serializers.ValidationError({'amount': 'Amount must be a positive number.'})
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user
        taxes = validated_data.pop('taxes', [])
        transaction = super().create(validated_data)
        transaction.taxes.set(taxes)
        return transaction

    def update(self, instance, validated_data):
        taxes = validated_data.pop('taxes', None)
        instance = super().update(instance, validated_data)
        if taxes is not None:
            instance.taxes.set(taxes)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'taxes_count'):
            representation['taxes_count'] = instance.taxes_count
        return representation
