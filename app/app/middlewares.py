from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async

from urllib import parse


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query_string = parse.parse_qs(scope['query_string'])
        if b'authorization' in query_string:
            try:
                token_key = query_string[b'authorization'][0]
                token_key = token_key.decode().split()[0]
                token = Token.objects.get(key=token_key)
                scope['user'] = token.user
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = \
    lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
