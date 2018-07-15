from django.conf.urls import url

from .consumers import MainConsumer

websocket_urlpatterns = [
    url(r'^ws/main/$', MainConsumer),
]
