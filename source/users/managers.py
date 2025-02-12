"""Module providing a managers for Users models."""
from typing import Optional

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Class representing an object manager for User model.
    """

    use_in_migrations = True

    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields
    ):
        """
        Method for creating default user.
        this user has no permissions to log in to admin site
        """
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Method for creating superuser.
        this user can be login to admin site and has all permissions
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        if not password:
            raise ValueError("Superuser must have password")
        return self.create_user(email=email, password=password, **extra_fields)

    def create_staff(self, email: str, password: str, **extra_fields):
        """
        Method for creating staff user.
        this user can be login to admin site
        and has permissions which you give to.
        """
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        if not password:
            raise ValueError("Staff must have password")
        return self.create_user(email=email, password=password, **extra_fields)
