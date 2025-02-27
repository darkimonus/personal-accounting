from django.urls import path
from incomes.views import IncomeSourcesView,  IncomeTaxesView, IncomeTransactionsView

urlpatterns = [
    path('sources/', IncomeSourcesView.as_view(
        actions={'get': 'list', 'post': 'create'}),
        name='income-sources'),
    path('sources/<int:pk>/', IncomeSourcesView.as_view(
        actions={'patch': 'partial_update', 'get': 'retrieve'}),
        name='income-source'),
    path('taxes/', IncomeTaxesView.as_view(
        actions={'get': 'list', 'post': 'create'}),
        name='income-taxes'),
    path('taxes/<int:pk>/', IncomeTaxesView.as_view(
        actions={'patch': 'partial_update', 'get': 'retrieve'}),
        name='income-tax'),
    path('transactions/', IncomeTransactionsView.as_view(
        actions={'get': 'list', 'post': 'create'}),
         name='income-transactions'),
    path('transactions/<int:pk>/', IncomeTransactionsView.as_view(
        actions={'patch': 'partial_update', 'get': 'retrieve'}),
         name='income-transaction'),
]
