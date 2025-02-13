from django.db.models import Count, F
from django.db.models import QuerySet
from django.conf import settings

from datetime import datetime
from typing import Optional


def apply_filters(
        queryset: QuerySet,
        user: settings.AUTH_USER_MODEL,
        date_filter: Optional[str],
        order_by: str,
        order_direction: str = 'desc',
        transaction_model: bool = False,
):
    """
    Apply filters to a queryset based on user, ordering, and date criteria.

    Args:
        queryset: The initial queryset to be filtered.
        user: The user to filter the queryset by.
        order_by: The field to order the queryset by ('transactions' or 'date').
        order_direction: The direction to order the queryset ('asc' or 'desc').
        date_filter: A string representing the date to filter the queryset from, in 'YYYY-MM-DD' format.
        transaction_model: Whether it's a transaction model. Defaults to False.

    Returns:
        The filtered and ordered queryset.
    """
    queryset = queryset.filter(user=user)
    if transaction_model:
        queryset = queryset.annotate(taxes_count=Count('taxes'))
        if order_by == 'transactions':
            raise ValueError('For transactions model, order_by must be either "date" or "taxes".')
        if not order_by:
            order_by = 'taxes'
    else:
        queryset = queryset.annotate(transactions=Count('income_transactions'))
        if order_by == 'taxes':
            raise ValueError('order_by must be either "date" or "transactions".')
        if not order_by:
            order_by = 'transactions'

    match order_by:
        case 'transactions':
            queryset = queryset.order_by(
                F('transactions').desc() if order_direction == 'desc'
                else F('transactions').asc())
        case 'date':
            queryset = queryset.order_by(
                F('created_at').desc() if order_direction == 'desc'
                else F('created_at').asc())
        case 'taxes':
            queryset = queryset.order_by(
                F('taxes').desc() if order_direction == 'desc'
                else F('taxes').asc())
        case _:
            raise ValueError(f"Invalid order_by parameter: {order_by}. Must be one of "
                             f"['transactions', 'date', 'taxes'].")

    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d")
            queryset = queryset.filter(created_at__gte=date_filter)
        except ValueError:
            pass

    return queryset
