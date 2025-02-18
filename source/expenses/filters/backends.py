from rest_framework.filters import BaseFilterBackend

from expenses.choices import CATEGORY_CHOICES
from .exceptions import FiltersError

from datetime import datetime


class ReceiptFilterBackend(BaseFilterBackend):
    """
    Custom filter backend to filter Receipt objects based on various query parameters.

    Supported query parameters:
      - date: a date string (YYYY-MM-DD)
      - date_ordering: one of 'greater', 'equal', or 'less'. Default is 'equal'.
      - store_name: a substring to match in the store name.
      - total_price: a numeric value.
      - price_ordering: one of 'greater', 'equal', or 'less'. Default is 'equal'.
      - purchase_name: filter receipts by a substring match on related Purchase.name.
      - purchase_category: filter receipts by related Purchase.category (exact match, case insensitive).
      - order_by: a field name to order the final queryset.
    """

    def filter_queryset(self, request, queryset, view):

        errors = {}
        category_choices = [choice[0] for choice in CATEGORY_CHOICES]

        # Filter by date with ordering
        date_value = request.query_params.get('date')
        date_ordering = request.query_params.get('date_ordering', 'equal')
        if date_value:
            try:
                # Try to parse the date_value in the expected format.
                parsed_date = datetime.strptime(date_value, '%Y-%m-%d').date()
            except ValueError:
                errors['date'] = "Invalid date format. Expected YYYY-MM-DD."
            else:
                if date_ordering == 'greater':
                    queryset = queryset.filter(date__gte=parsed_date)
                elif date_ordering == 'less':
                    queryset = queryset.filter(date__lte=parsed_date)
                else:
                    queryset = queryset.filter(date=parsed_date)

        # Filter by store_name (case-insensitive containment)
        store_name = request.query_params.get('store_name')
        if store_name:
            queryset = queryset.filter(store_name__icontains=store_name)

        # Filter by total_price with ordering
        total_price = request.query_params.get('total_price')
        price_ordering = request.query_params.get('price_ordering', 'equal')
        if total_price:
            total_price = float(total_price)
            if total_price <= 0:
                errors['total_price'] = "Total price value should be greater than zero."
            else:
                if price_ordering == 'greater':
                    queryset = queryset.filter(total_price__gte=total_price)
                elif price_ordering == 'less':
                    queryset = queryset.filter(total_price__lte=total_price)
                else:
                    queryset = queryset.filter(total_price=total_price)

        # Filter by related purchase fields via ReceiptItem (using the reverse relation "items")
        purchase_name = request.query_params.get('purchase_name')
        if purchase_name:
            queryset = queryset.filter(items__purchase__name__icontains=purchase_name)

        purchase_category = request.query_params.get('purchase_category')
        if purchase_category:
            if purchase_category not in category_choices:
                errors['purchase_category'] = f"Invalid category. Valid categories are {category_choices}"
            queryset = queryset.filter(items__purchase__category__iexact=purchase_category)

        order_by = request.query_params.get('order_by')
        try:
            if order_by:
                queryset = queryset.order_by(order_by)
        except :
            errors['order_by'] = f"Invalid order_by parameter '{order_by}'."

        if errors:
            raise FiltersError(errors=errors)

        return queryset
