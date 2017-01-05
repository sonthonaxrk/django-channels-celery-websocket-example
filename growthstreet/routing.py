from channels import route
from customers.consumers import connect_waiter, disconnect_waiter


# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. WebSocket messages of all
# types have a 'path' attribute, so we're using that to route the socket.
# While this is under stream/ compared to the HTML page, we could have it on the
# same URL if we wanted; Daphne separates by protocol as it negotiates with a
# browser.

from django.http import HttpResponse
from channels.handler import AsgiHandler

PHONE_PATH = r"^/phone_verify/$"

channel_routing = [
    route("websocket.connect", connect_waiter, path=PHONE_PATH),
    route("websocket.disconnect", disconnect_waiter, path=PHONE_PATH),
]
