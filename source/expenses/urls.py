from django.urls import path
from expenses.views import ReceiptViewSet

urls = [
    path(
        'receipts/',
        ReceiptViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='expenses-receipt-list'
    ),
    path(
        'receipts/<int:pk>/',
        ReceiptViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
        name='expenses-receipt-detail'
    ),
]
