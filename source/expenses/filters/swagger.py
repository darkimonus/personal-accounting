from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


receipts_date_param = openapi.Parameter(
    'date',
    openapi.IN_QUERY,
    description="Filter receipts by date. Format: YYYY-MM-DD.",
    type=openapi.TYPE_STRING
)
receipts_date_ordering_param = openapi.Parameter(
    'date_ordering',
    openapi.IN_QUERY,
    description="Ordering for date: 'greater', 'less', or 'equal' (default: equal).",
    type=openapi.TYPE_STRING
)
receipts_store_name_param = openapi.Parameter(
    'store_name',
    openapi.IN_QUERY,
    description="Filter receipts by store name (case-insensitive).",
    type=openapi.TYPE_STRING
)
receipts_total_price_param = openapi.Parameter(
    'total_price',
    openapi.IN_QUERY,
    description="Filter receipts by total price.",
    type=openapi.TYPE_NUMBER
)
receipts_price_ordering_param = openapi.Parameter(
    'price_ordering',
    openapi.IN_QUERY,
    description="Ordering for total price: 'greater', 'less', or 'equal' (default: equal).",
    type=openapi.TYPE_STRING
)
receipts_purchase_name_param = openapi.Parameter(
    'purchase_name',
    openapi.IN_QUERY,
    description="Filter receipts by related purchase name (partial match).",
    type=openapi.TYPE_STRING
)
receipts_purchase_category_param = openapi.Parameter(
    'purchase_category',
    openapi.IN_QUERY,
    description="Filter receipts by related purchase category (exact match).",
    type=openapi.TYPE_STRING
)
receipts_order_by_param = openapi.Parameter(
    'order_by',
    openapi.IN_QUERY,
    description="Field to order by. Use '-' prefix for descending order (e.g. '-date').",
    type=openapi.TYPE_STRING
)

# list of all parameters used in the Swagger schema for receipts endpoint
receipts_swagger_params = [
    receipts_date_param,
    receipts_date_ordering_param,
    receipts_store_name_param,
    receipts_total_price_param,
    receipts_price_ordering_param,
    receipts_purchase_name_param,
    receipts_purchase_category_param,
    receipts_order_by_param
]
