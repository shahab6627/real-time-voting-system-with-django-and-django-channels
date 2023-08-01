from django.urls import path 
from .consumers import PollVoteConsumer

websockets_urlpatterns = [
    path('ws/pollvote/<str:slug>', PollVoteConsumer.as_asgi())
]