from rest_framework import serializers
from incomes.models import IncomeSource, IncomeTax, IncomeTransaction


class IncomeSourceSerializer(serializers.ModelSerializer):
    """
    Serializer for the IncomeSource model, including custom validation and representation.

    Attributes:
        transactions (IntegerField): Read-only field for the number of transactions.
        created_at (DateTimeField): Read-only field for the creation date, formatted as 'YYYY-MM-DD'.

    Meta:
        model (IncomeSource): The model associated with this serializer.
        fields (list): List of fields to be serialized, including 'name', 'description', 'link',
        'transactions' and 'created_at'.

    Methods:
        to_representation(instance): Customize the representation of an instance to include transactions count.
        validate_name(value): Ensure the income source name is unique for the current user.
    """
    transactions = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d')

    class Meta:
        model = IncomeSource
        fields = ['name', 'description', 'link', 'transactions', 'created_at']
        read_only_fields = ['transactions', 'created_at']

    def to_representation(self, instance):
        """
        Override the default representation of an instance to include transactions if they exist.
        """
        representation = super().to_representation(instance)
        if hasattr(instance, 'transactions'):
            representation['transactions'] = instance.transactions

        return representation

    def validate_name(self, value):
        """
        Validate the uniqueness of an income source name for the current user.

        Args:
            value: The name of the income source to validate.

        Returns:
            The validated name if it is unique for the user.

        Raises:
            serializers.ValidationError: If an income source with the same name already exists for the user.
        """
        user = self.context['request'].user
        if IncomeSource.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError(f"Income source with the name '{value}' already exists.")
        return value


class IncomeTaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeTax
        fields = ['name', 'rate', 'description']


class IncomeTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeTransaction
        fields = '__all__'
