"""This module makes Token mixins."""
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauthlib.common import generate_token

# pylint: disable=W0223,R0903


class GenerateTokenMixin:
    """
    Mixin for token pair generations.
    Need for create user objects.
    """

    @staticmethod
    def generate_token_pair(user: User) -> dict:
        """Method for pairing tokens.
        return:
            dict:
                "access_token": str,
                "expires_in": int in seconds # 86400,
                "refresh_token": str,
                "token_type": str,
                "scope": str,
        """
        # pylint: disable=E1101
        try:
            app = Application.objects.first()
            token_life = settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"]
            exp = timezone.now() + timezone.timedelta(seconds=token_life)

            token = AccessToken.objects.create(
                user=user,
                application=app,
                expires=exp,
                token=generate_token(),
            )
            refresh = RefreshToken.objects.create(
                user=user,
                application=app,
                access_token=token,
                token=generate_token(),
            )
            token_pair = {
                "access_token": token.token,
                "expires_in": token_life,
                "refresh_token": refresh.token,
                "token_type": "Bearer",
                "scope": "read write",
            }
            return token_pair
        except Exception as error:
            raise ValueError(error)
