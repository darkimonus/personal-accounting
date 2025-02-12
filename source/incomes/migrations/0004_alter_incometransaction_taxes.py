# Generated by Django 5.1.6 on 2025-02-12 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0003_alter_incomesource_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incometransaction',
            name='taxes',
            field=models.ManyToManyField(blank=True, related_name='income_transactions', to='incomes.incometax'),
        ),
    ]
