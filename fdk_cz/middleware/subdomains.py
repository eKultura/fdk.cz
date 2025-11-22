# -------------------------------------------------------------------
# MIDDLEWARE.SUBDOMAINS.PY
# -------------------------------------------------------------------
from django.urls import set_urlconf


class SubdomainRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]

        if host == "ucetnictvi.fdk.cz":
            request.subdomain = "ucetnictvi"
            request.urlconf = "fdk_cz.urls.accounting"
        else:
            request.subdomain = None

        response = self.get_response(request)
        return response
