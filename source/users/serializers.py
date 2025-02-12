"""Module providing a serializers for Users APIViews."""
import re

from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.exceptions import (
    UserResetPasswordDoesNotExistsException,
    UserVerificationDoesNotExistsException,
    UserDoesNotExistsException,
)
from users.models import User, UserVerification, ResetPassword

# pylint: disable=W0223,R0903, E1101

# pylint: disable=W0223,R0903, E1101


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for presenting User object in AccessDataSerializer.
    """

    class Meta:
        """
        Class for settings UserSerializer.
        """

        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """
        Method that checks user's password
        """
        password = attrs.get("password")
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$", password):
            raise ValidationError(
                {
                    "password": _(
                        "Password should contain an uppercase letter,"
                        " a lowercase letter and a number."
                    )
                }
            )
        attrs["password"] = make_password(password)
        return attrs


class AccessDataSerializer(serializers.Serializer):
    """
    Serializer for presenting token data in AccessDataSerializer.
    """

    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires_in = serializers.IntegerField()
    token_type = serializers.CharField()
    scope = serializers.CharField()


class UnitedAccessDataUserSerializer(serializers.Serializer):
    """
    Serializer for response User data
    and Token data for creating User endpoint.
    """

    user_data = UserSerializer()
    token_data = AccessDataSerializer()


class UserVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for ResendVerificationCodeView.
    """

    # pylint: disable=C0115
    class Meta:
        model = UserVerification
        fields = ("user",)


class UserVerificationCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for VerificationCodeView.
    """

    # pylint: disable=C0115
    class Meta:
        model = UserVerification
        fields = (
            "user",
            "code",
        )

    def validate(self, attrs):
        """
        Method that checks verification codes.
        """
        code = attrs.get("code")
        user = attrs.get("user")

        user_verification = UserVerification.objects.filter(user=user).first()
        if user_verification is None:
            raise UserVerificationDoesNotExistsException

        if user_verification.code != code:
            raise ValidationError({"code": "Verification code is invalid"})
        return attrs


class UserResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for ResetPasswordView.
    """

    email = serializers.EmailField()


class UserResetPasswordCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for resetting password and checking code.
    """

    email = serializers.EmailField()
    password = serializers.CharField()
    password_re = serializers.CharField()

    # pylint: disable=C0115
    class Meta:
        model = ResetPassword
        fields = (
            "email",
            "code",
            "password",
            "password_re",
        )

    def validate(self, attrs):
        """
        Method that checks user's passwords
        """

        code = attrs.get("code")
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()
        if user is None:
            raise UserDoesNotExistsException(user_email=email)

        reset_password = ResetPassword.objects.filter(user=user).first()
        if reset_password is None:
            raise UserResetPasswordDoesNotExistsException

        if reset_password.code != code:
            raise ValidationError({"code": "Reset password code is invalid"})

        password = attrs.get("password")
        password_re = attrs.get("password_re")
        if password != password_re:
            raise ValidationError({"password": "Passwords don’t match"})
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$", password):
            raise ValidationError(
                {
                    "password": _(
                        "Password should contain an uppercase letter,"
                        " a lowercase letter and a number."
                    )
                }
            )
        attrs.pop("password_re")
        attrs["password"] = make_password(password)
        return attrs


class ResponseDetailSerializer(serializers.Serializer):
    """
    Serializer for swagger default.
    """

    detail = serializers.CharField()
