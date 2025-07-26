
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from store.consumers import OrderConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enlog_ecommerce.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/orders/$', OrderConsumer.as_asgi()),
        ])
    ),
})