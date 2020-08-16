from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

'''
In this code, you use URLRouter to map websocket connections to the URL patterns
defined in the websocket_urlpatterns list of the chat application routing file.
The standard ProtocolTypeRouter router automatically maps HTTP requests to
the standard Django views if no specific http mapping is provided. You also use
AuthMiddlewareStack. The AuthMiddlewareStack class provided by Channels
supports standard Django authentication, where the user details are stored in
the session. You plan to access the user instance in the scope of the consumer to
identify the user who sends a message.

'''

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})