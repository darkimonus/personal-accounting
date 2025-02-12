from django.db.models import Count, F
from django.db.models import QuerySet
from django.conf import settings

from datetime import datetime
from typing import Optional


def apply_filters(
        queryset: QuerySet,
        user: settings.AUTH_USER_MODEL,
        order_by: str,
        order_direction: str,
        date_filter: Optional[str]
):
    """
    Apply filters to a queryset based on user, ordering, and date criteria.

    Args:
        queryset: The initial queryset to be filtered.
        user: The user to filter the queryset by.
        order_by: The field to order the queryset by ('transactions' or 'date').
        order_direction: The direction to order the queryset ('asc' or 'desc').
        date_filter: A string representing the date to filter the queryset from, in 'YYYY-MM-DD' format.

    Returns:
        The filtered and ordered queryset.
    """
    queryset = queryset.filter(user=user)

    queryset = queryset.annotate(transactions=Count('income_transactions'))

    if order_by == 'transactions':
        queryset = queryset.order_by(
            F('transactions').desc() if order_direction == 'desc'
            else F('transactions').asc())
    elif order_by == 'date':
        queryset = queryset.order_by(
            F('created_at').desc() if order_direction == 'desc'
            else F('created_at').asc())

    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d")
            queryset = queryset.filter(created_at__gte=date_filter)
        except ValueError:
            pass

    return queryset
