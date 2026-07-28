from django.urls import re_path
from  myapp.consumers import NotificationConsumer

websocket_patterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]