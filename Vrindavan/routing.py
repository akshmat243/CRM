# vrindavan_crm/routing.py
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import home.routing
from django.core.asgi import get_asgi_application




application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            home.routing.websocket_urlpatterns
        )
    ),
})
