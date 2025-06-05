from django.contrib.sites.models import Site
from django.http import HttpResponseServerError


class MultiSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        site_id = request.headers.get("X-Site-ID")
        if site_id:
            try:
                request.site = Site.objects.get(pk=site_id)
            except Site.DoesNotExist:
                return HttpResponseServerError("Oops! Something went wrong.")
        return self.get_response(request)
