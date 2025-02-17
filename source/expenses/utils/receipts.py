from django.conf import settings
from django.db import transaction

from expenses.models import Receipt, Expense, ReceiptItem, Purchase

from decimal import Decimal

User = settings.AUTH_USER_MODEL


def calculate_receipt_item_unit_price(unit_type,
                                      total_price,
                                      quantity) -> Decimal:
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
    total = Decimal(0.0)
    for item in instance.items.all():
        total += item.total_price
    return total


def calculate_expense_total(instance: Expense) -> Decimal:
    total = Decimal(0.0)
    for receipt in instance.receipts:
        total += receipt.total_price
    return total


def create_receipt_from_validated_data(validated_data: dict, user: User):
    with transaction.atomic():
        receipt_items = validated_data.pop('receipt_items')
        receipt = Receipt.objects.create(**validated_data, user=user)

        for receipt_item_data in receipt_items:
            purchase_data = receipt_item_data.pop('purchase')
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
