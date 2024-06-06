from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()), # to accept slug text in the url
    re_path(r'ws/call/(?P<room_name>[\w-]+)/$', consumers.SignalingConsumer.as_asgi()), # to accept slug text in the url
]