# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/life_tracking/", consumers.LifeTrackerConsumer.as_asgi()),
]
