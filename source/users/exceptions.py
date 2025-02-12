"""Module with Exception classes for Users."""
from typing import Union

from rest_framework import status
from rest_framework.exceptions import APIException

# pylint: disable=C0115


class UserDoesNotExistsException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User Does Not Exists"
    default_code = "user_do_not_exists"

    def __init__(
        self,
        *args,
        user_id: Union[str, int] = None,
        user_email: str = None,
        **kwargs,
    ):
        if user_id is not None:
            self.default_detail = f"User With ID {user_id} Does Not Exists"
        elif user_email is not None:
            self.default_detail = (
                f"User With email {user_email} Does Not Exists"
            )
        super().__init__(*args, **kwargs)


class UserVerificationOffException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "User verification is turned off"
    default_code = "user_verification_is_turned_off"


class UserVerificationDoesNotExistsException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "Ask for account verifying first"
    default_code = "ask_for_account_verifying_first"


class UserIsAlreadyVerifiedException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "User is already verified"
    default_code = "user_is_already_verified"


class UserResetPasswordDoesNotExistsException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "Ask for password resetting first"
    default_code = "ask_for_password_resetting_first"
