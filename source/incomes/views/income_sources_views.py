from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from incomes.utils import apply_filters

from incomes.models import IncomeSource
from incomes.serializers import IncomeSourceSerializer


class IncomeSourcesView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    serializer_class = IncomeSourceSerializer
    queryset = IncomeSource.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.create(request, serializer)

    @swagger_auto_schema(
        operation_description="Retrieve user's income sources list.",
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
        responses={200: IncomeSourceSerializer(many=True), 400: "Bad Request", 401: "Unauthorized"},
    )
    def list(self, request, *args, **kwargs):
        order_by = request.query_params.get('order_by', 'transactions')
        order_direction = request.query_params.get('order_direction', 'desc')
        date_filter = request.query_params.get('date_filter', None)

        queryset = apply_filters(
            self.get_queryset(),
            request.user,
            order_by,
            order_direction,
            date_filter
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
