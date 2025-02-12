from incomes.models import IncomeSource
from incomes.serializers import IncomeSourceSerializer
from .base import BaseIncomeViewSet


class IncomeSourcesView(BaseIncomeViewSet):
    serializer_class = IncomeSourceSerializer
    queryset = IncomeSource.objects.all()
