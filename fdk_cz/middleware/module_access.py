# fdk_cz/middleware/module_access.py

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from fdk_cz.models import Module, UserModuleSubscription


class ModuleAccessMiddleware:
    """
    Middleware kontrolující přístup k placeným modulům
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # URL patterns, které jsou vždy dostupné
        self.EXEMPT_URLS = [
            '/admin/',
            '/prihlaseni/',
            '/login/',
            '/registrace/',
            '/logout/',
            '/static/',
            '/media/',
            '/predplatne/',  # Stránka s cenami
            '/ceny/',
            '/api/',
            '/',  # Homepage
            '/index/',
            '/dashboard/',
        ]

        # FREE moduly - nepotřebují kontrolu
        self.FREE_URL_PATTERNS = [
            '/projekty/',
            '/projekt',
            '/ukoly/',
            '/ukol',
            '/task',
            '/seznamy/',
            '/seznam',
            '/list',
            '/kontakty/',
            '/kontakt',
            '/contact',
        ]

    def __call__(self, request):
        # Vynechat exempt URLs
        if any(request.path.startswith(url) for url in self.EXEMPT_URLS):
            return self.get_response(request)

        # Vynechat free URL patterns
        if any(pattern in request.path for pattern in self.FREE_URL_PATTERNS):
            return self.get_response(request)

        # Kontrolovat pouze přihlášené uživatele
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Zjistit, zda URL odpovídá nějakému placenému modulu
        required_module = self._get_required_module(request.path)

        if not required_module:
            # Není placený modul -> pokračovat
            return self.get_response(request)

        # Kontrola, zda má uživatel aktivní subscription
        has_access = self._check_user_access(request.user, required_module)

        if not has_access:
            # Uživatel NEMÁ přístup -> redirect na pricing page
            messages.warning(
                request,
                f'Pro přístup k modulu "{required_module.display_name}" potřebujete aktivní předplatné. '
                f'<a href="{reverse("subscription_pricing")}">Zobrazit ceny</a>',
                extra_tags='safe'
            )
            return redirect('subscription_pricing')

        return self.get_response(request)

    def _get_required_module(self, path):
        """Zjistit, který modul je vyžadován pro danou URL"""
        try:
            # Načíst všechny aktivní paid moduly
            modules = Module.objects.filter(is_active=True, is_free=False)

            for module in modules:
                # Zkontrolovat url_patterns
                if module.url_patterns:
                    for pattern in module.url_patterns:
                        if pattern in path:
                            return module
            return None
        except Exception:
            return None

    def _check_user_access(self, user, module):
        """Kontrola, zda má uživatel přístup k modulu"""
        try:
            # Zkontrolovat aktivní subscription
            subscription = UserModuleSubscription.objects.filter(
                user=user,
                module=module,
                is_active=True
            ).first()

            if not subscription:
                return False

            # Zkontrolovat expiraci
            if subscription.is_expired():
                subscription.is_active = False
                subscription.save()
                return False

            return True

        except Exception:
            return False
