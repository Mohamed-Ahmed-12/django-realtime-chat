"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# new 
 
from channels.routing import ProtocolTypeRouter , URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from mysite.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns)
            )
        ),
    }
)
'''
This root routing configuration specifies that when a connection is made to the Channels development server, the ProtocolTypeRouter will first inspect the type of connection. If it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack.

The AuthMiddlewareStack will populate the connection’s scope with a reference to the currently authenticated user, similar to how Django’s AuthenticationMiddleware populates the request object of a view function with the currently authenticated user. (Scopes will be discussed later in this tutorial.) Then the connection will be given to the URLRouter.

The URLRouter will examine the HTTP path of the connection to route it to a particular consumer, based on the provided url patterns.
'''