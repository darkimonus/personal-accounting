from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class QuantityValidator(BaseValidator):

    def __call__(self, value):
        if value is None:
            raise ValidationError("Quantity must not be null.")

        if self.instance.purchase.unit_type == 'pcs':
            if value != int(value):
                raise ValidationError("Quantity must be an integer for items measured in pcs.")
            if value < 1:
                raise ValidationError("Quantity must be greater than or equal to 1 for items measured in pcs.")