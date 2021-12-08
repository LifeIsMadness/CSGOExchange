from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class TradelinkRequiredMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def process_request(self, request):
        url = reverse('exchanger:tradelink_required'),
        if not request.user.inventory.trade_link:
            if request.path != url:
                return redirect(url) # or http response
        return self.get_response(request)
