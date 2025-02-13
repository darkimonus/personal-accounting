from django.db.models.signals import pre_save
from django.dispatch import receiver

from expenses.models import ReceiptItem, Receipt, Expense
from expenses.utils import calculate_receipt_item_unit_price, calculate_receipt_total, calculate_expense_total


@receiver(pre_save, sender=ReceiptItem)
def update_receipt_item_total_amount(sender, instance, **kwargs):
    instance.unit_price = calculate_receipt_item_unit_price(
        instance.purchase.unit_type,
        instance.total_price,
        instance.quantity,
    )


@receiver(pre_save, sender=Receipt)
def update_receipt_total_amount(sender, instance, **kwargs):
    instance.total_amount = calculate_receipt_total(instance)


@receiver(pre_save, sender=Expense)
def update_expense_total_amount(sender, instance, **kwargs):
    instance.total_amount = calculate_expense_total(instance)
