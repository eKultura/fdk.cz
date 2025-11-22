# fdk_cz/middleware/subdomains.py

from django.shortcuts import redirect
from django.conf import settings


class SubdomainRoutingMiddleware:
    """
    Middleware pro routing podle subdomény.
    Například: ucetnictvi.fdk.cz -> přesměruje na účetnictví modul
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Mapování subdomén na URL cesty
        self.SUBDOMAIN_ROUTES = {
            'ucetnictvi': '/ucetnictvi/',
            'projekty': '/projekty/',
            'granty': '/granty/',
            'hr': '/hr/',
            'it': '/it/',
            'b2b': '/b2b/',
            'dms': '/dms/',
            'sklad': '/sklad/',
            'pravo': '/pravo/',
        }

    def __call__(self, request):
        # Získat host z requestu
        host = request.get_host().split(':')[0]  # Odstranit port

        # Zjistit subdoménu
        subdomain = self._get_subdomain(host)

        # Přidat subdoménu do requestu pro použití v šablonách
        request.subdomain = subdomain

        # Pokud je to root doména nebo www, pokračovat normálně
        if not subdomain or subdomain == 'www':
            return self.get_response(request)

        # Pokud je subdoména a jsme na homepage, přesměrovat na příslušný modul
        if subdomain in self.SUBDOMAIN_ROUTES:
            if request.path == '/' or request.path == '':
                return redirect(self.SUBDOMAIN_ROUTES[subdomain])

        return self.get_response(request)

    def _get_subdomain(self, host):
        """
        Extrahovat subdoménu z hostname.
        Například: ucetnictvi.fdk.cz -> ucetnictvi
        """
        # Získat základní doménu z nastavení nebo použít default
        base_domain = getattr(settings, 'BASE_DOMAIN', 'fdk.cz')

        # Odstranit základní doménu
        if host.endswith(base_domain):
            subdomain_part = host[:-len(base_domain)].rstrip('.')
            if subdomain_part:
                return subdomain_part

        return None
