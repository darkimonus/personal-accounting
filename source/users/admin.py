"""
Users models admin site settings here.
for more information go to admin/user
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import (
    User,
    ResetPassword,
    UserVerification,
)

from users.forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User admin site settings."""

    readonly_fields = ("date_joined",)
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups")}),
        ("Important dates", {"fields": ("date_joined",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


admin.site.register(ResetPassword)
admin.site.register(UserVerification)
