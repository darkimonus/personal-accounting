from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from expenses.models import ReceiptItem, Receipt, Expense
from expenses.utils import calculate_receipt_item_unit_price, calculate_receipt_total, calculate_expense_total


@receiver(post_save, sender=ReceiptItem)
def update_receipt_item_unit_price(sender, instance, **kwargs):
    unit_price = calculate_receipt_item_unit_price(
        instance.purchase.unit_type,
        instance.total_price,
        instance.quantity,
    )
    ReceiptItem.objects.filter(
        receipt=instance.receipt,
        purchase=instance.purchase
    ).update(unit_price=unit_price)


@receiver(post_save, sender=Expense)
def update_expense_total_amount(sender, instance, **kwargs):
    if instance.calculate_total:
        total_amount = calculate_expense_total(instance)
        Expense.objects.filter(pk=instance.pk).update(total_price=total_amount)
