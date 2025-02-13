from incomes.models import IncomeTransaction


def calculate_income_after_taxes(obj: IncomeTransaction):
    total_tax_rate = sum(tax.rate for tax in obj.taxes.all())
    return obj.amount * (1 - total_tax_rate)
