"""
ASGI config for chitchat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing
from channels.auth import AuthMiddlewareStack
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chitchat.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # we employ AuthMiddlewareStack for authentication and URLRouter to route WebSocket connections
        "websocket": AuthMiddlewareStack( # ensure secure WebSocket communication
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    }
)
