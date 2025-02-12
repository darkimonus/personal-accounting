"""This module makes User forms."""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating User.
    """

    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating User.
    """

    class Meta:
        model = User
        fields = ("email",)
        exclude = ("password",)
