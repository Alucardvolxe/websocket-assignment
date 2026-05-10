"""
ASGI config for websocket_assingment project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chat.routing import websocket_urlpatters

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket_assingment.settings')
django_asgi_app = get_asgi_application()
application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatters))
    )
    # Just HTTP for now. (We can add other protocols later.)
})