from incomes.models import IncomeTax
from incomes.serializers import IncomeTaxSerializer
from .base import BaseIncomeViewSet


class IncomeTaxesView(BaseIncomeViewSet):
    serializer_class = IncomeTaxSerializer
    queryset = IncomeTax.objects.all()
