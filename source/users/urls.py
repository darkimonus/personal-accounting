"""User URL configuration."""

from django.urls import path, include
from django.conf import settings

from users.views import (
    UserView,
    ResetPasswordCodeView,
    ResetPasswordView,
    ResendVerificationCodeView,
    VerificationCodeView,
)


urlpatterns = [
    path("", UserView.as_view(), name="user_register"),
    path(
        "password/",
        include(
            [
                path(
                    "reset/",
                    ResetPasswordView.as_view(),
                    name="user_reset_password",
                ),
                path(
                    "",
                    ResetPasswordCodeView.as_view(),
                    name="user_enter_password",
                ),
            ]
        ),
    ),
]

if settings.ENABLE_USER_VERIFICATION:
    urlpatterns += [
        path(
            "verification/",
            include(
                [
                    path(
                        "resend/",
                        ResendVerificationCodeView.as_view(),
                        name="user_resend_activation_code",
                    ),
                    path(
                        "",
                        VerificationCodeView.as_view(),
                        name="user_enter_activation_code",
                    ),
                ]
            ),
        ),
    ]
