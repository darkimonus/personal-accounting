"""Models for db Users."""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(
        "Phone",
        validators=[RegexValidator(regex=r"^\+?1?\d{8,15}$")],
        max_length=16,
        unique=False,
        blank=True,
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)

    class Meta:  # pylint: disable=C0115,R0903
        verbose_name = "User"
        verbose_name_plural = "Users"


class ResetPassword(models.Model):
    """
    Model for password resetting.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reset_password"
    )
    code = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # pylint: disable=C0115,R0903
        verbose_name = "Reset Password"
        verbose_name_plural = "Reset Password"

    def __str__(self):
        return f"{self.user}: {self.code}"


class UserVerification(models.Model):
    """
    Model for authentication codes.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_verification"
    )
    code = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # pylint: disable=C0115,R0903
        verbose_name = "User Verification"
        verbose_name_plural = "User Verification"

    def __str__(self):
        return f"{self.user}: {self.code}"
