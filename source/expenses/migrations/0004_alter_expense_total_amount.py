# Generated by Django 5.1.6 on 2025-02-17 15:17

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_alter_expense_name_remove_expense_receipts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
