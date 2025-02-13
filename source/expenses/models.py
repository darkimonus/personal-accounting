from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from expenses.choices import UNIT_CHOICES, CATEGORY_CHOICES
from expenses.validators import QuantityValidator
from expenses.utils import calculate_receipt_item_unit_price
from expenses.managers import PurchaseManager, ReceiptItemManager, ReceiptManager, ExpenseManager

from decimal import Decimal

User = settings.AUTH_USER_MODEL


class Purchase(models.Model):

    class Meta:
        unique_together = ('name', 'brand', 'unit_type')
        verbose_name_plural = _("Purchases")
        verbose_name = _("Purchase")
        indexes = [
            models.Index(fields=['name', 'brand', 'unit_type']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
        ]

    name = models.CharField(max_length=100)
    unit_type = models.CharField(
        max_length=3,
        choices=UNIT_CHOICES
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other"
    )
    brand = models.CharField(
        max_length=100,
        blank=True
    )
    manufacturer_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PurchaseManager()

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class ReceiptItem(models.Model):

    class Meta:
        verbose_name_plural = _("Receipt Item")
        verbose_name = _("Receipt Items")
        indexes = [
            models.Index(fields=['purchase']),
            models.Index(fields=['user']),
            models.Index(fields=['total_price']),
            models.Index(fields=['unit_price']),
            models.Index(fields=['purchase', 'user']),
        ]

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="receipt_items",
        db_index=True
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[
            MinValueValidator(Decimal('0.001')),
            QuantityValidator(None),
        ]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        validators=[
            MinValueValidator(Decimal('0.01')),
        ]
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        validators=[
            MinValueValidator(Decimal('0.001')),
        ]
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )

    objects = ReceiptItemManager()

    def save(self, *args, **kwargs):
        self.unit_price = calculate_receipt_item_unit_price(
            self.purchase.unit_type,
            self.total_price,
            self.quantity,
        )
        super().save(*args, **kwargs)


class Receipt(models.Model):

    class Meta:
        verbose_name_plural = _("Receipt")
        verbose_name = _("Receipts")
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'store_name']),
        ]

    date = models.DateField()
    store_name = models.CharField(
        max_length=50,
        blank=True
    )
    receipt_items = models.ManyToManyField(
        ReceiptItem,
        related_name="receipts"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )

    objects = ReceiptManager()


class Expense(models.Model):

    class Meta:
        verbose_name_plural = _("Expense")
        verbose_name = _("Expenses")
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'date']),
            models.Index(fields=['total_amount']),
        ]

    name = models.CharField(max_length=255)
    date = models.DateField()
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
        ]
    )
    receipts = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name="receipts",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    objects = ExpenseManager()
