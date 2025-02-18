from django.conf import settings
from django.db import transaction

from expenses.models import Receipt, Expense, ReceiptItem, Purchase

from decimal import Decimal

User = settings.AUTH_USER_MODEL


def calculate_receipt_item_unit_price(unit_type: str,
                                      total_price: Decimal,
                                      quantity: Decimal) -> Decimal:
    match unit_type:
        case 'kg':
            unit_price = Decimal(total_price / quantity)

        case 'pcs':
            unit_price = Decimal(total_price / int(quantity))
            return unit_price
        case _:
            raise ValueError('Unknown unit type.')
    return unit_price


def calculate_receipt_total(instance: Receipt) -> Decimal:
    """
    This function calculates the total price of a receipt based on its item's total prices.
    """
    total = Decimal(0.0)
    for item in instance.items.all():
        total += item.total_price
    return total


def calculate_expense_total(instance: Expense) -> Decimal:
    """
    This function calculates the total amount of an expense based on its receipt's total prices.
    """
    total = Decimal(0.0)
    for receipt in instance.receipts.all():
        total += receipt.total_price
    return total


def normalize_purchase_data(purchase_data: dict):
    # Normalize the fields to ensure consistency
    purchase_data['name'] = purchase_data.get('name', '').strip()
    purchase_data['brand'] = purchase_data.get('brand', '').strip()
    purchase_data['unit_type'] = purchase_data.get('unit_type', '').strip().lower()  # if appropriate
    return purchase_data


def create_receipt_from_validated_data(validated_data: dict, user: User):
    """
    Create a receipt from validated data and associate it with a user.

    Args:
        validated_data (dict): A dictionary containing validated receipt data, including receipt items.
        user (User): The user associated with the receipt.

    Returns:
        Receipt: The created receipt object.

    This function uses a transaction to ensure atomicity. It creates a receipt and its associated receipt
    items from the provided validated data. If the receipt has a total price calculation, it updates the
    total price before saving the receipt.
    """
    with transaction.atomic():
        receipt_items = validated_data.pop('receipt_items')
        receipt = Receipt.objects.create(**validated_data, user=user)

        for receipt_item_data in receipt_items:
            purchase_data = receipt_item_data.pop('purchase')
            purchase_data = normalize_purchase_data(purchase_data)
            purchase, created = Purchase.objects.get_or_create(**purchase_data)
            ReceiptItem.objects.create(
                purchase=purchase,
                user=user,
                receipt=receipt,
                **receipt_item_data
            )

        if receipt.calculate_total:
            receipt.total_price = calculate_receipt_total(receipt)
            receipt.save()

        return receipt
