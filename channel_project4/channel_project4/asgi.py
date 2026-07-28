import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from myapp.routing import websocket_patterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channel_project4.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_patterns))
    }
)
