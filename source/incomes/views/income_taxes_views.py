from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status

from .base import BaseIncomeViewSet
from incomes.utils import apply_filters
from incomes.models import IncomeTax
from incomes.serializers import IncomeTaxSerializer


class IncomeTaxesView(BaseIncomeViewSet):
    serializer_class = IncomeTaxSerializer
    queryset = IncomeTax.objects.all()

    @swagger_auto_schema(
        operation_description="Retrieve user's income taxes list.",
        manual_parameters=[
            openapi.Parameter(
                'order_by',
                openapi.IN_QUERY,
                description="Ordering parameter.",
                type=openapi.TYPE_STRING,
                default='transactions',
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
        valid_order_by_args = ['transactions', 'date']
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
        )
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
