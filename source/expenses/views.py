from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count

from drf_yasg.utils import swagger_auto_schema

from expenses.serializers import ReceiptSerializer, RetrieveReceiptSerializer, RetrieveExpenseSerializer, \
    ExpenseReceiptsIdSerializer, RetrieveNoReceiptsExpenseSerializer
from expenses.models import Receipt, Expense
from expenses.utils.receipts import create_receipt_from_validated_data
from expenses.filters import ReceiptFilterBackend, receipts_swagger_params, FiltersError


class ReceiptPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ReceiptViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):

    paginator = ReceiptPagination()
    queryset = Receipt.objects.all()
    filter_backends = [ReceiptFilterBackend]

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user).annotate(
            items_count=Count('receipt_items')
        ).prefetch_related('items', 'items__purchase')
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveReceiptSerializer
        else:
            return ReceiptSerializer

    def perform_create(self, serializer):
        receipt = create_receipt_from_validated_data(serializer.validated_data, self.request.user)
        serializer = RetrieveReceiptSerializer(receipt)
        return serializer

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: update exception handling, to return proper error message
        try:
            response_serializer = self.perform_create(serializer)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(manual_parameters=receipts_swagger_params)
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, args, kwargs)
        except FiltersError as e:
            return Response({'errors': e.errors}, status=status.HTTP_400_BAD_REQUEST)


class ExpenseViewSet(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):

    queryset = Expense.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExpenseReceiptsIdSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: update exception handling, to return proper error message
        self.perform_create(serializer)
        response_serializer = RetrieveNoReceiptsExpenseSerializer(serializer.instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
