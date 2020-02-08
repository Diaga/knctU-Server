from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from core.consumers import SubscribeConsumer
from .middlewares import TokenAuthMiddleware

websockets = [
    path('ws/subscribe/', SubscribeConsumer)
]


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': TokenAuthMiddleware(
        URLRouter(websockets)
    )
})
