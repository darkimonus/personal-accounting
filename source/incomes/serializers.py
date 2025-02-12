from rest_framework import serializers
from incomes.models import IncomeSource, IncomeTax, IncomeTransaction


class IncomeSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeSource
        fields = ['name', 'description', 'link']


class IncomeTaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeTax
        fields = '__all__'


class IncomeTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeTransaction
        fields = '__all__'
