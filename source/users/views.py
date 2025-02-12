from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import importlib
import os

from users.exceptions import (
    UserVerificationOffException,
    UserDoesNotExistsException,
    UserIsAlreadyVerifiedException,
)
from users.models import User, UserVerification, ResetPassword
from users.serializers import (
    UserSerializer,
    AccessDataSerializer,
    UnitedAccessDataUserSerializer,
    UserVerificationSerializer,
    UserVerificationCodeSerializer,
    UserResetPasswordSerializer,
    UserResetPasswordCodeSerializer,
    ResponseDetailSerializer,
)
from users.services.send_email_to_user_service import UserSendEmailService
from users.services.generate_token_service import GenerateTokenMixin
from django.conf import settings

try:
    trottling_module = importlib.import_module(
        f"{os.environ['DJANGO_PROJECT_NAME']}.throttling"
    )
except ModuleNotFoundError:
    raise ImportError(f"Couldn't import {os.environ['DJANGO_PROJECT_NAME']}.throttling")


class UserView(generics.GenericAPIView, GenerateTokenMixin):
    """
    # APIView for User modules.
        method: POST
        required fields: email
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer = None
    user = None
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: UnitedAccessDataUserSerializer()},
        operation_summary="Create user",
    )
    def post(self, request, *args, **kwargs):
        """
        Endpoint for creating User.
        If ENABLE_USER_VERIFICATION is True that send email.
        """
        try:
            self.serializer = self.get_serializer(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            self.serializer.save()
            if settings.ENABLE_USER_VERIFICATION:
                user_email = self.serializer.validated_data.get("email")
                self.user = User.objects.filter(email=user_email).first()
                if self.user is None:
                    raise UserDoesNotExistsException(user_email=user_email)
                UserSendEmailService(self.user).send_verification_email()
                kwargs["is_active"] = False
            return self.create(request, *args, **kwargs)
        except Exception as error:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """Method for check serializer for POST response.
        If ENABLE_USER_VERIFICATION is False
            that use AccessDataSerializer for response.
        """
        if kwargs.get("is_active") is False:
            self.user.is_active = False
            self.user.save()
        if settings.ENABLE_USER_VERIFICATION:
            data = self.serializer.data
        else:
            token_pair = self.generate_token_pair(self.serializer.instance)
            token_serializer = AccessDataSerializer(token_pair)
            united_token_user_data = {
                "token_data": token_serializer.validated_data,
                "user_data": self.serializer.validated_data,
            }
            united_serializer = UnitedAccessDataUserSerializer(
                data=united_token_user_data
            )
            united_serializer.is_valid()
            data = united_serializer.data
        return Response(data, status=status.HTTP_201_CREATED)


class ResendVerificationCodeView(generics.GenericAPIView):
    queryset = UserVerification.objects.all()
    serializer_class = UserVerificationSerializer
    throttle_classes = [trottling_module.EmailSendThrottle]

    @swagger_auto_schema(
        operation_summary="Resend Verification Code",
        responses={status.HTTP_201_CREATED: ResponseDetailSerializer()},
    )
    def post(self, request, *args, **kwargs):
        if not settings.ENABLE_USER_VERIFICATION:
            raise UserVerificationOffException
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        if user.is_active:
            raise UserIsAlreadyVerifiedException
        UserSendEmailService(user).send_verification_email()
        return Response(
            {"detail": "THE ACTIVATION CODE WAS RESENTED"},
            status=status.HTTP_201_CREATED,
        )


class VerificationCodeView(generics.GenericAPIView, GenerateTokenMixin):
    queryset = UserVerification.objects.all()
    serializer_class = UserVerificationCodeSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="Enter Verification Code")
    def post(self, request, *args, **kwargs):
        if not settings.ENABLE_USER_VERIFICATION:
            raise UserVerificationOffException
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")
        user.is_active = True
        user.save()

        token_pair = self.generate_token_pair(user)
        token_serializer = AccessDataSerializer(token_pair)

        user_serializer = UserSerializer(user)
        united_token_user_data = {
            "token_data": token_serializer.data,
            "user_data": user_serializer.data,
        }
        united_serializer = UnitedAccessDataUserSerializer(data=united_token_user_data)
        united_serializer.is_valid()

        UserVerification.objects.get(user=user).delete()

        return Response(
            united_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ResetPasswordView(generics.GenericAPIView):
    queryset = ResetPassword.objects.all()
    serializer_class = UserResetPasswordSerializer
    throttle_classes = [trottling_module.EmailSendThrottle]

    @swagger_auto_schema(
        responses={status.HTTP_202_ACCEPTED: UserResetPasswordSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email).first()
        if user is None:
            raise UserDoesNotExistsException(user_email=email)

        UserSendEmailService(user).send_reset_password_email()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ResetPasswordCodeView(generics.GenericAPIView):
    queryset = ResetPassword.objects.all()
    serializer_class = UserResetPasswordCodeSerializer

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: ResponseDetailSerializer()},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email).first()
        if user is None:
            raise UserDoesNotExistsException(user_email=email)

        password = serializer.validated_data.get("password")
        user.password = password
        user.save()

        ResetPassword.objects.get(user=user).delete()

        return Response(
            {"detail": "THE PASSWORD WAS SUCCESSFULLY CHANGED"},
            status=status.HTTP_201_CREATED,
        )
