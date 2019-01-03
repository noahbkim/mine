import secrets
from django.contrib.auth.backends import ModelBackend
from django.middleware.common import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from . import models


class TokenBackend(ModelBackend):
    """A simple token-based authentication system."""

    @classmethod
    def generate(cls):
        """Generate a random token."""

        return secrets.token_hex(32)

    def authenticate(self, request, **credentials):
        """Authenticate a user."""

        username = credentials.get("username")
        password = credentials.get("password")
        if username is not None and password is not None:

            # Standard authentication
            user = super().authenticate(request, username, password)
            if user is None:
                return None

            # Create or access the token
            session = models.Session.objects.filter(user=user).first()
            if session is None:
                token = self.generate()
                models.Session.objects.create(user=user, token=token).save()
                request.token = token
            else:
                request.token = session.token
            return user

        return None


class TokenMiddleware(MiddlewareMixin):
    """Middleware for accessing the user making a request."""

    def process_request(self, request):

        request.user = SimpleLazyObject(lambda: get_user(request))
