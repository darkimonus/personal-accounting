from decimal import Decimal

from expenses.models import Expense


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


def calculate_expense_total(expense: Expense) -> Expense:
    total = Decimal(0.0)
    for receipt in expense.receipts:
        total += receipt.total_price
    expense.total = total
    return expense
