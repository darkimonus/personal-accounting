"""Module for throttle settings."""
from rest_framework.throttling import UserRateThrottle


class EmailSendThrottle(UserRateThrottle):
    """Throttle settings for project sending email."""

    scope = "email_send"

    def get_cache_key(self, request, view):
        """
        parameters:
            request: {user}
            view: Any
        return
            cache_format: str # 'throttle_%(scope)s_%(indent)s'
        """

        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}
