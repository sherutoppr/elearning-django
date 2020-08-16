# re_path used for urls having regular expression
from django.urls import re_path
from . import consumers

'''
In this code, you map a URL pattern with the ChatConsumer class that you defined
in the chat/consumers.py file. You use Django's re_path to define the path with
regular expressions. The URL includes an integer parameter called course_id.
This parameter will be available in the scope of the consumer and will allow you
to identify the course chat room that the user is connecting to.

'''

websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.ChatConsumer),
]