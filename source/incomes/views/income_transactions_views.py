from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status

from incomes.models import IncomeTransaction
from incomes.serializers import IncomeTransactionSerializer
from incomes.utils import apply_filters
from .base import BaseIncomeViewSet


class IncomeTransactionsView(BaseIncomeViewSet):
    serializer_class = IncomeTransactionSerializer
    queryset = IncomeTransaction.objects.all()

    @swagger_auto_schema(
        operation_description="Retrieve user's income transactions list.",
        manual_parameters=[
            openapi.Parameter(
                'order_by',
                openapi.IN_QUERY,
                description="Ordering parameter.",
                type=openapi.TYPE_STRING,
                default='taxes',
            ),
            openapi.Parameter(
                'order_direction',
                openapi.IN_QUERY,
                description="Sorting direction.",
                type=openapi.TYPE_STRING,
                default='desc',
            ),
            openapi.Parameter(
                'date_filter',
                openapi.IN_QUERY,
                description="Date filtering.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: 'Serializer(many=True)', 400: "Bad Request", 401: "Unauthorized"},
    )
    def list(self, request, *args, **kwargs):
        order_by, order_direction, date_filter = super().list(request, *args, **kwargs)
        valid_order_by_args = ['date', 'taxes']
        valid_order_directions = ['asc', 'desc']
        try:
            self.validate_list_query_params(
                valid_order_by_args,
                valid_order_directions,
                order_by,
                order_direction,
                date_filter
            )
        except ValueError as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        queryset = apply_filters(
            self.get_queryset(),
            request.user,
            date_filter,
            order_by,
            order_direction,
            transaction_model=True,
        )
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'source': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of income source"
                ),
                'amount': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format='decimal',
                    description="Amount of money"
                ),
                'date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Date when income was received"
                ),
                'taxes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING,
                                         description="ID as integer or tax name"),
                    description="List of taxes (ID or name)"
                )
            },
            required=['amount']
        ),
        responses={201: IncomeTransactionSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
