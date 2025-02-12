from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from incomes.managers import IncomeSourcesManager, IncomeTaxesManager, IncomeTransactionsManager

User = settings.AUTH_USER_MODEL


class IncomeSource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = IncomeSourcesManager()

    class Meta:
        verbose_name = _('Income source')
        verbose_name_plural = _('Income source\'s')

    def __str__(self):
        return f"{self.user.email}: {self.name}"


class IncomeTax(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = IncomeTaxesManager()

    class Meta:
        verbose_name = _('Income tax')
        verbose_name_plural = _('Income tax\'s')


class IncomeTransaction(models.Model):
    source = models.ForeignKey(IncomeSource, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    taxes = models.ManyToManyField(IncomeTax, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = IncomeTransactionsManager()

    class Meta:
        verbose_name = _('Income transaction')
        verbose_name_plural = _('Income transaction\'s')
