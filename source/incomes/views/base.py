from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from datetime import datetime


class BaseIncomeViewSet(GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.create(request, serializer)

    def list(self, request, *args, **kwargs):
        order_by = request.query_params.get('order_by', None)
        order_direction = request.query_params.get('order_direction', None)
        date_filter = request.query_params.get('date_filter', None)

        return order_by, order_direction, date_filter

    @staticmethod
    def validate_list_query_params(valid_order_by_args: list,
                                   valid_order_directions: list,
                                   order_by=None,
                                   order_direction=None,
                                   date_filter=None):
        """
        Validate query parameters for list operations.

        Args:
            valid_order_by_args (list): A list of valid order_by arguments.
            valid_order_directions (list): A list of valid order directions.
            order_by (str, optional): The field to order by. Defaults to None.
            order_direction (str, optional): The direction of ordering. Defaults to None.
            date_filter (str, optional): A date filter in YYYY-MM-DD format. Defaults to None.

        Raises:
            ValueError: If order_by is not in valid_order_by_args.
            ValueError: If order_direction is not in valid_order_directions.
            ValueError: If date_filter is not a valid date in YYYY-MM-DD format.
        """
        if order_by and order_by not in valid_order_by_args:
            raise ValueError(f"Provided order_by value '{order_by}' is invalid. "
                             f"Please provide one of this values {valid_order_by_args}")
        if order_direction not in valid_order_directions:
            raise ValueError(f"Provided order_direction value '{order_direction}' is invalid. "
                             f'Please provide one of this values {valid_order_directions}')
        if date_filter:
            try:
                datetime.strptime(date_filter, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Provided date_filter value '{date_filter}' is invalid. "
                                 f"Please provide a valid date in YYYY-MM-DD format.")

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
