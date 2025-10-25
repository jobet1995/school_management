"""
ASGI config for school_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from typing import List
from django.core.asgi import get_asgi_application
from django.urls import URLPattern, URLResolver
from channels.routing import ProtocolTypeRouter, URLRouter
from cms_plugins.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_management.settings")

# Type cast to satisfy type checkers
websocket_routes: List[URLPattern | URLResolver] = list(websocket_urlpatterns)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_routes),  # type: ignore
})