from django.urls import path
from incomes.views import IncomeSourcesView,  IncomeTaxesView

urlpatterns = [
    path('sources/', IncomeSourcesView.as_view(
        actions={'get': 'list', 'post': 'create'}),
        name='income-sources'),
    path('taxes/', IncomeTaxesView.as_view(), name='income-taxes'),
]
