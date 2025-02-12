"""Module for Services for Sending Emails for Users."""
import secrets
import importlib
import os

from string import ascii_uppercase, digits
from typing import Union

from users.models import User, UserVerification, ResetPassword
from django.conf import settings

try:
    celery_module = importlib.import_module(
        f"{os.environ['DJANGO_PROJECT_NAME']}.celery"
    )
except ModuleNotFoundError:
    raise ImportError(f"Couldn't import {os.environ['DJANGO_PROJECT_NAME']}.celery")


class UserSendEmailService:
    """
    Service for Sending Emails for Users.
    """

    # pylint: disable=C0116
    __email_activation_body = "Your activation code is"
    __email_reset_body = "Your password reset code is"

    def __init__(self, user: User):
        self.__user = user

    def __send_email(self, model: Union[UserVerification, ResetPassword]):
        random_code = self.__generate_code(model)
        model_instance = model.objects.filter(user=self.__user).first()
        if model_instance is None:
            model_instance = model(user=self.__user, code=random_code)
        else:
            model_instance.code = random_code
        model_instance.save()

        email_subject = settings.EMAIL_SUBJECT.format(self.__user.email)
        email_body_text = (
            self.__email_activation_body
            if issubclass(model, UserVerification)
            else self.__email_reset_body
        )
        email_body = settings.EMAIL_BODY.format(email_body_text, random_code)
        celery_module.send_verification_email.delay(
            from_email=settings.FROM_EMAIL,
            to=[self.__user.email],
            subject=email_subject,
            body=email_body,
        )

    def send_verification_email(self):
        self.__send_email(UserVerification)

    def send_reset_password_email(self):
        self.__send_email(ResetPassword)

    def __generate_code(self, model: Union[UserVerification, ResetPassword]):
        while True:
            random_code = self.__get_random_code()
            is_code_exists = model.objects.filter(code=random_code).exists()
            if not is_code_exists:
                break
        return random_code

    @staticmethod
    def __get_random_code() -> str:
        characters = ascii_uppercase + digits
        random_string = "".join(
            secrets.choice(characters) for _ in range(settings.EMAIL_CODE_LENGTH)
        )
        return random_string
