from wagtail.models import Page
from .models import VehicleStock


class SuppressCsrfForHexonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            route = Page.route_for_request(request, request.path)
            if route and isinstance(route.page, VehicleStock):
                request.csrf_processing_done = True
        response = self.get_response(request)
        return response