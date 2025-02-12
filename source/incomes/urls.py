from django.urls import path, include
from incomes.views import IncomeSourcesView

urlpatterns = [
    path('income-sources/', IncomeSourcesView.as_view(), name='income_sources'),
]
