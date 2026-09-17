from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


@database_sync_to_async
def get_user(user_id):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        scope["user"] = AnonymousUser()

        query_string = scope["query_string"].decode()
        token = query_string.split("token=")[-1]

        try:
            access_token = AccessToken(token)

            user_id = access_token["user_id"]

            scope["user"] = await get_user(user_id)

        except (TokenError, KeyError):
            pass

        return await super().__call__(scope, receive, send)
