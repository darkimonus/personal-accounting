from django.contrib import admin
from expenses.models import Purchase, ReceiptItem, Receipt, Expense

# Register your models here.
admin.site.register(Purchase)
admin.site.register(ReceiptItem)
admin.site.register(Receipt)
admin.site.register(Expense)
