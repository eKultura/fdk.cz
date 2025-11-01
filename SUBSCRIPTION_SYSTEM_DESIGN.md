# SUBSCRIPTION SYSTEM DESIGN DOCUMENT
## FDK.cz - Monetizace modulů ERP systému

**Verze:** 1.0
**Datum:** 2025-11-01
**Autor:** Claude (AI Assistant)
**Status:** Design dokumentace

---

## 1. PŘEHLED SYSTÉMU

### 1.1 Cíl
Implementovat komplexní subscription systém, který umožní:
- ✅ Monetizaci vybraných modulů (měsíční/roční předplatné)
- ✅ Bezplatné základní moduly pro všechny uživatele
- ✅ Flexibilní přiřazování modulů uživatelům/organizacím
- ✅ Integraci s platební bránou (Stripe/GoPay)
- ✅ Middleware pro kontrolu přístupu k placeným modulům
- ✅ UI pro správu předplatných

### 1.2 Business Model

#### **FREE moduly (vždy dostupné)**
1. **Project Management** - Základní správa projektů
2. **Task Management** - Správa úkolů (v rámci projektu i samostatně)
3. **Seznamy** (Flist) - Do 10 seznamů zdarma
4. **Adresář** - Správa kontaktů

#### **PAID moduly (vyžadují předplatné)**
1. **Granty a dotace** - 299 Kč/měsíc nebo 2990 Kč/rok
2. **Test Management** - 199 Kč/měsíc nebo 1990 Kč/rok
3. **Účetnictví** - 399 Kč/měsíc nebo 3990 Kč/rok
4. **Skladové hospodářství** - 249 Kč/měsíc nebo 2490 Kč/rok
5. **Správa smluv** - 199 Kč/měsíc nebo 1990 Kč/rok
6. **Legal Compliance & Law AI** - 499 Kč/měsíc nebo 4990 Kč/rok
7. **HR Management** - 349 Kč/měsíc nebo 3490 Kč/rok
8. **B2B Management** - 349 Kč/měsíc nebo 3490 Kč/rok
9. **Risk Management** - 299 Kč/měsíc nebo 2990 Kč/rok
10. **IT Management + ITIL** - 449 Kč/měsíc nebo 4490 Kč/rok
11. **Asset Management** - 299 Kč/měsíc nebo 2990 Kč/rok

#### **BUNDLE balíčky**
- **Starter** (PM + Tasks + Lists): Zdarma
- **Business** (+ Granty + Smlouvy + Účetnictví): 799 Kč/měsíc nebo 7990 Kč/rok (sleva 20%)
- **Enterprise** (všechny moduly): 2499 Kč/měsíc nebo 24990 Kč/rok (sleva 30%)

---

## 2. DATABÁZOVÉ MODELY

### 2.1 Module (Modul)
```python
class Module(models.Model):
    module_id = models.AutoField(primary_key=True, db_column='module_id')

    # Identifikace modulu
    name = models.CharField(max_length=100, unique=True, db_column='name')
    # 'project_management', 'grants', 'warehouse', etc.

    display_name = models.CharField(max_length=200, db_column='display_name')
    # 'Správa projektů', 'Granty a dotace', etc.

    display_name_en = models.CharField(max_length=200, null=True, blank=True, db_column='display_name_en')

    # Popis
    description = models.TextField(db_column='description')
    short_description = models.CharField(max_length=255, null=True, blank=True, db_column='short_description')

    # Ceny
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='price_monthly')
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column='price_yearly')

    # Vlastnosti
    is_free = models.BooleanField(default=False, db_column='is_free')
    is_active = models.BooleanField(default=True, db_column='is_active')
    requires_organization = models.BooleanField(default=False, db_column='requires_organization')

    # URL routing (pro middleware kontrolu)
    url_patterns = models.JSONField(default=list, db_column='url_patterns')
    # ['grants/', 'grant_', '/dotace/']

    # UI metadata
    icon = models.CharField(max_length=50, null=True, blank=True, db_column='icon')  # emoji nebo Material Icon
    color = models.CharField(max_length=7, default='#3b82f6', db_column='color')  # hex color
    order = models.IntegerField(default=0, db_column='order')  # pořadí v menu

    # Limity free verze
    free_limit = models.IntegerField(null=True, blank=True, db_column='free_limit')
    # Např. 10 seznamů zdarma

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_module'
        ordering = ['order', 'display_name']

    def __str__(self):
        return f"{self.display_name} ({self.name})"
```

### 2.2 UserModuleSubscription (Předplatné uživatele)
```python
class UserModuleSubscription(models.Model):
    subscription_id = models.AutoField(primary_key=True, db_column='subscription_id')

    # Vztahy
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_subscriptions', db_column='user_id')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_subscriptions', db_column='module_id')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='module_subscriptions', db_column='organization_id')

    # Typ předplatného
    subscription_type = models.CharField(max_length=20, choices=[
        ('free', 'Zdarma'),
        ('monthly', 'Měsíční'),
        ('yearly', 'Roční'),
        ('lifetime', 'Doživotní'),
        ('trial', 'Zkušební')
    ], db_column='subscription_type')

    # Časové období
    start_date = models.DateTimeField(auto_now_add=True, db_column='start_date')
    end_date = models.DateTimeField(null=True, blank=True, db_column='end_date')
    trial_end_date = models.DateTimeField(null=True, blank=True, db_column='trial_end_date')

    # Status
    is_active = models.BooleanField(default=True, db_column='is_active')
    auto_renew = models.BooleanField(default=True, db_column='auto_renew')

    # Platební informace
    payment_method = models.CharField(max_length=50, null=True, blank=True, db_column='payment_method')
    # 'stripe', 'gopay', 'invoice'
    external_subscription_id = models.CharField(max_length=255, null=True, blank=True, db_column='external_subscription_id')
    # ID z Stripe/GoPay

    # Metadata
    notes = models.TextField(null=True, blank=True, db_column='notes')
    cancelled_at = models.DateTimeField(null=True, blank=True, db_column='cancelled_at')
    cancellation_reason = models.TextField(null=True, blank=True, db_column='cancellation_reason')

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_user_module_subscription'
        unique_together = ('user', 'module')
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['end_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.module.display_name} ({self.subscription_type})"

    def is_expired(self):
        """Kontrola, zda předplatné vypršelo"""
        if self.end_date is None:
            return False
        return timezone.now() > self.end_date

    def days_remaining(self):
        """Počet dní do konce předplatného"""
        if self.end_date is None:
            return None
        delta = self.end_date - timezone.now()
        return max(0, delta.days)
```

### 2.3 ModuleBundle (Balíčky modulů)
```python
class ModuleBundle(models.Model):
    bundle_id = models.AutoField(primary_key=True, db_column='bundle_id')

    name = models.CharField(max_length=100, db_column='name')  # 'Starter', 'Business', 'Enterprise'
    display_name = models.CharField(max_length=200, db_column='display_name')
    description = models.TextField(db_column='description')

    modules = models.ManyToManyField(Module, related_name='bundles', db_column='modules')

    # Ceny s discount
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, db_column='price_monthly')
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, db_column='price_yearly')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_column='discount_percentage')

    is_active = models.BooleanField(default=True, db_column='is_active')
    is_featured = models.BooleanField(default=False, db_column='is_featured')

    icon = models.CharField(max_length=50, null=True, blank=True, db_column='icon')
    color = models.CharField(max_length=7, default='#3b82f6', db_column='color')
    order = models.IntegerField(default=0, db_column='order')

    class Meta:
        db_table = 'FDK_module_bundle'
        ordering = ['order']

    def __str__(self):
        return self.display_name
```

### 2.4 Payment (Platby)
```python
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True, db_column='payment_id')

    # Vztahy
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', db_column='user_id')
    subscription = models.ForeignKey(UserModuleSubscription, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='payments', db_column='subscription_id')

    # Částka
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='amount')
    currency = models.CharField(max_length=3, default='CZK', db_column='currency')

    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Čeká na zpracování'),
        ('completed', 'Dokončeno'),
        ('failed', 'Selhalo'),
        ('refunded', 'Vráceno'),
        ('cancelled', 'Zrušeno')
    ], default='pending', db_column='status')

    # Platební metoda
    payment_method = models.CharField(max_length=50, db_column='payment_method')  # 'stripe', 'gopay', 'bank_transfer'
    external_payment_id = models.CharField(max_length=255, null=True, blank=True, db_column='external_payment_id')

    # Fakturace
    invoice_number = models.CharField(max_length=50, null=True, blank=True, db_column='invoice_number')
    invoice_url = models.URLField(null=True, blank=True, db_column='invoice_url')

    # Metadata
    description = models.TextField(null=True, blank=True, db_column='description')
    metadata = models.JSONField(default=dict, db_column='metadata')

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    completed_at = models.DateTimeField(null=True, blank=True, db_column='completed_at')

    class Meta:
        db_table = 'FDK_payment'
        ordering = ['-created_at']

    def __str__(self):
        return f"Platba {self.payment_id} - {self.amount} {self.currency} ({self.status})"
```

### 2.5 ModuleUsage (Využití modulů - pro analytics)
```python
class ModuleUsage(models.Model):
    usage_id = models.AutoField(primary_key=True, db_column='usage_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_usage', db_column='user_id')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='usage_logs', db_column='module_id')

    action = models.CharField(max_length=100, db_column='action')
    # 'page_view', 'create_grant_application', 'warehouse_transaction', etc.

    timestamp = models.DateTimeField(auto_now_add=True, db_column='timestamp')
    details = models.JSONField(null=True, blank=True, db_column='details')

    # IP a user agent pro analytics
    ip_address = models.GenericIPAddressField(null=True, blank=True, db_column='ip_address')
    user_agent = models.CharField(max_length=255, null=True, blank=True, db_column='user_agent')

    class Meta:
        db_table = 'FDK_module_usage'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['module', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.module.name} - {self.action}"
```

---

## 3. MIDDLEWARE PRO KONTROLU PŘÍSTUPU

### 3.1 ModuleAccessMiddleware

```python
# fdk_cz/middleware/module_access.py

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from fdk_cz.models import Module, UserModuleSubscription

class ModuleAccessMiddleware:
    """
    Middleware kontrolující přístup k placeným modulům.

    Workflow:
    1. Zjistí, zda request.path odpovídá nějakému modulu
    2. Pokud ano, zkontroluje, zda má uživatel aktivní subscription
    3. Pokud ne, přesměruje na stránku s cenami/upgrade
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Definice URL patternů pro každý modul
        self.MODULE_URL_PATTERNS = {
            'grants': ['/granty/', '/dotace/', '/grant_', '/grants/'],
            'test_management': ['/testy/', '/test_', '/tests/'],
            'accounting': ['/ucetnictvi/', '/accounting/', '/faktury/', '/invoice'],
            'warehouse': ['/sklad/', '/warehouse/'],
            'contracts': ['/smlouvy/', '/contract'],
            'law_ai': ['/pravo-ai/', '/law/', '/pravo/'],
            'hr_management': ['/hr/', '/zamestnanci/'],
            'b2b_management': ['/b2b/', '/business/'],
            'risk_management': ['/rizika/', '/risk/'],
            'it_management': ['/it/', '/sprava-it/'],
            'asset_management': ['/majetek/', '/asset/'],
        }

        # Moduly, které jsou vždy free (nepotřebují kontrolu)
        self.FREE_MODULES = [
            'project_management',
            'task_management',
            'lists',
            'contacts'
        ]

        # URL patterns, které jsou vždy dostupné (admin, login, static, atd.)
        self.EXEMPT_URLS = [
            '/admin/',
            '/prihlaseni/',
            '/login/',
            '/registrace/',
            '/logout/',
            '/static/',
            '/media/',
            '/api/payment-webhook/',
            '/predplatne/',  # Stránka s cenami
            '/upgrade/',
        ]

    def __call__(self, request):
        # Vynechat exempt URLs
        if any(request.path.startswith(url) for url in self.EXEMPT_URLS):
            return self.get_response(request)

        # Kontrolovat pouze přihlášené uživatele
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Zjistit, zda URL odpovídá nějakému placenému modulu
        required_module = None
        for module_name, patterns in self.MODULE_URL_PATTERNS.items():
            if any(pattern in request.path for pattern in patterns):
                required_module = module_name
                break

        # Pokud není placený modul, pokračovat
        if not required_module:
            return self.get_response(request)

        # Kontrola, zda má uživatel aktivní subscription
        has_access = self._check_user_access(request.user, required_module)

        if not has_access:
            # Uživatel NEMÁ přístup -> redirect na upgrade page
            messages.warning(
                request,
                f"Pro přístup k tomuto modulu je potřeba aktivní předplatné. "
                f"<a href='{reverse('subscription_pricing')}'>Zobrazit ceny</a>"
            )
            return redirect('subscription_pricing')

        # Logovat využití modulu (pro analytics)
        self._log_module_usage(request.user, required_module, request.path)

        return self.get_response(request)

    def _check_user_access(self, user, module_name):
        """
        Kontrola, zda má uživatel přístup k modulu.
        """
        try:
            module = Module.objects.get(name=module_name, is_active=True)

            # Pokud je modul zdarma, má každý přístup
            if module.is_free:
                return True

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

        except Module.DoesNotExist:
            # Modul neexistuje -> povolit přístup (možná je to free modul)
            return True

    def _log_module_usage(self, user, module_name, path):
        """
        Zalogovat využití modulu pro analytics.
        """
        from fdk_cz.models import ModuleUsage

        try:
            module = Module.objects.get(name=module_name)
            ModuleUsage.objects.create(
                user=user,
                module=module,
                action='page_view',
                details={'path': path}
            )
        except:
            pass  # Nechceme, aby selhalo kvůli loggingu
```

### 3.2 Registrace middleware v settings.py

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ✅ Přidat subscription middleware
    'fdk_cz.middleware.module_access.ModuleAccessMiddleware',
]
```

---

## 4. VIEWS & FORMS

### 4.1 Views struktura

```
views/
├── subscription.py              # Správa předplatného (view, upgrade, cancel)
├── subscription_payment.py      # Platební workflow (Stripe/GoPay integration)
└── subscription_admin.py        # Admin rozhraní pro správu subscriptions
```

### 4.2 subscription.py - Core views

```python
# fdk_cz/views/subscription.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from fdk_cz.models import Module, UserModuleSubscription, ModuleBundle, Payment


@login_required
def subscription_dashboard(request):
    """
    Dashboard předplatného - přehled aktivních modulů uživatele
    """
    # Získat všechny aktivní subscriptions uživatele
    user_subscriptions = UserModuleSubscription.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('module')

    # Moduly, které uživatel NEMÁ
    subscribed_module_ids = [sub.module_id for sub in user_subscriptions]
    available_modules = Module.objects.filter(
        is_active=True,
        is_free=False
    ).exclude(module_id__in=subscribed_module_ids)

    # Kontrola expirace
    expiring_soon = []
    for sub in user_subscriptions:
        if sub.days_remaining() and sub.days_remaining() <= 7:
            expiring_soon.append(sub)

    context = {
        'active_subscriptions': user_subscriptions,
        'available_modules': available_modules,
        'expiring_soon': expiring_soon,
        'free_modules': Module.objects.filter(is_free=True, is_active=True)
    }

    return render(request, 'subscription/subscription_dashboard.html', context)


def subscription_pricing(request):
    """
    Stránka s cenami - veřejná stránka pro všechny
    """
    modules = Module.objects.filter(is_active=True).order_by('order')
    bundles = ModuleBundle.objects.filter(is_active=True).prefetch_related('modules')

    # Pokud je uživatel přihlášen, zjistit, které moduly už má
    user_subscriptions = []
    if request.user.is_authenticated:
        user_subscriptions = UserModuleSubscription.objects.filter(
            user=request.user,
            is_active=True
        ).values_list('module_id', flat=True)

    context = {
        'modules': modules,
        'bundles': bundles,
        'user_subscriptions': user_subscriptions
    }

    return render(request, 'subscription/subscription_pricing_page.html', context)


@login_required
def subscribe_to_module(request, module_id):
    """
    Zahájit nákup předplatného modulu
    """
    module = get_object_or_404(Module, module_id=module_id, is_active=True)

    # Kontrola, zda už uživatel nemá aktivní subscription
    existing = UserModuleSubscription.objects.filter(
        user=request.user,
        module=module,
        is_active=True
    ).first()

    if existing:
        messages.info(request, f"Již máte aktivní předplatné modulu {module.display_name}.")
        return redirect('subscription_dashboard')

    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type')  # 'monthly' nebo 'yearly'

        # Vytvořit pending subscription
        if subscription_type == 'monthly':
            price = module.price_monthly
            end_date = timezone.now() + timedelta(days=30)
        elif subscription_type == 'yearly':
            price = module.price_yearly
            end_date = timezone.now() + timedelta(days=365)
        else:
            messages.error(request, "Neplatný typ předplatného.")
            return redirect('subscription_pricing')

        # Vytvořit subscription (zatím neaktivní)
        subscription = UserModuleSubscription.objects.create(
            user=request.user,
            module=module,
            subscription_type=subscription_type,
            is_active=False,  # Aktivujeme po platbě
            end_date=end_date
        )

        # Přesměrovat na platební bránu
        return redirect('payment_checkout', subscription_id=subscription.subscription_id)

    context = {
        'module': module
    }

    return render(request, 'subscription/subscribe_to_module.html', context)


@login_required
def cancel_subscription(request, subscription_id):
    """
    Zrušit předplatné
    """
    subscription = get_object_or_404(
        UserModuleSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        cancellation_reason = request.POST.get('reason', '')

        subscription.is_active = False
        subscription.cancelled_at = timezone.now()
        subscription.cancellation_reason = cancellation_reason
        subscription.save()

        messages.success(request, f"Předplatné modulu {subscription.module.display_name} bylo zrušeno.")
        return redirect('subscription_dashboard')

    context = {
        'subscription': subscription
    }

    return render(request, 'subscription/cancel_subscription.html', context)


@login_required
def renew_subscription(request, subscription_id):
    """
    Obnovit předplatné
    """
    subscription = get_object_or_404(
        UserModuleSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        # Prodloužit end_date
        if subscription.subscription_type == 'monthly':
            new_end_date = timezone.now() + timedelta(days=30)
        elif subscription.subscription_type == 'yearly':
            new_end_date = timezone.now() + timedelta(days=365)

        subscription.end_date = new_end_date
        subscription.is_active = True
        subscription.save()

        # Vytvořit platbu
        return redirect('payment_checkout', subscription_id=subscription.subscription_id)

    context = {
        'subscription': subscription
    }

    return render(request, 'subscription/renew_subscription.html', context)
```

### 4.3 Forms

```python
# fdk_cz/forms/subscription.py

from django import forms
from fdk_cz.models import UserModuleSubscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserModuleSubscription
        fields = ['subscription_type']
        widgets = {
            'subscription_type': forms.RadioSelect()
        }

class CancellationForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Proč rušíte předplatné? (volitelné)'
        }),
        required=False
    )
```

---

## 5. TEMPLATES STRUKTURA

```
templates/subscription/
├── subscription_dashboard.html           # Dashboard uživatele
├── subscription_pricing_page.html        # Veřejná stránka s cenami
├── subscribe_to_module.html              # Formulář pro nákup modulu
├── cancel_subscription.html              # Zrušení předplatného
├── renew_subscription.html               # Obnovení předplatného
├── payment_checkout.html                 # Platební checkout
├── payment_success.html                  # Po úspěšné platbě
└── payment_failed.html                   # Po neúspěšné platbě
```

---

## 6. URL ROUTING

```python
# fdk_cz/urls.py

from fdk_cz.views import subscription

urlpatterns = [
    # ... existující URL patterns ...

    # Subscription URLs
    path('predplatne/', subscription.subscription_dashboard, name='subscription_dashboard'),
    path('ceny/', subscription.subscription_pricing, name='subscription_pricing'),
    path('predplatne/modul/<int:module_id>/objednat/', subscription.subscribe_to_module, name='subscribe_to_module'),
    path('predplatne/<int:subscription_id>/zrusit/', subscription.cancel_subscription, name='cancel_subscription'),
    path('predplatne/<int:subscription_id>/obnovit/', subscription.renew_subscription, name='renew_subscription'),

    # Payment URLs (implementace v další fázi)
    # path('platba/<int:subscription_id>/', payment.checkout, name='payment_checkout'),
    # path('platba/uspech/', payment.success, name='payment_success'),
    # path('platba/chyba/', payment.failed, name='payment_failed'),
]
```

---

## 7. MENU INTEGRACE

### 7.1 Dynamické menu v base.html

```django
<!-- Upravit base.html sidebar -->
<nav class="sidebar-nav">
  <div class="nav-section">
    <div class="nav-section-title">Hlavní</div>
    <!-- Základní navigace -->
  </div>

  <div class="nav-section">
    <div class="nav-section-title">Management</div>

    <!-- FREE moduly - vždy viditelné -->
    <a href="{% url 'index_project_cs' %}" class="nav-item">
      <span class="nav-icon">🛠️</span> Správa projektů
    </a>
    <a href="{% url 'task_management' %}" class="nav-item">
      <span class="nav-icon">✔️</span> Správa úkolů
    </a>

    <!-- PAID moduly - s ikonou zámku pokud uživatel NEMÁ subscription -->
    {% if user_has_module.hr_management %}
      <a href="{% url 'hr_dashboard' %}" class="nav-item">
        <span class="nav-icon">💼</span> HR Management
      </a>
    {% else %}
      <a href="{% url 'subscription_pricing' %}" class="nav-item nav-item-locked">
        <span class="nav-icon">💼</span> HR Management
        <span class="lock-icon">🔒</span>
      </a>
    {% endif %}

    <!-- Opakovat pro všechny paid moduly... -->
  </div>

  <!-- Nová sekce Předplatné -->
  <div class="nav-section">
    <div class="nav-section-title">Předplatné</div>
    <a href="{% url 'subscription_dashboard' %}" class="nav-item">
      <span class="nav-icon">💳</span> Moje předplatné
    </a>
    <a href="{% url 'subscription_pricing' %}" class="nav-item">
      <span class="nav-icon">💰</span> Ceník modulů
    </a>
  </div>
</nav>
```

### 7.2 Context Processor pro moduly

```python
# fdk_cz/context_processors.py

from fdk_cz.models import UserModuleSubscription

def user_modules(request):
    """
    Context processor, který přidá user_has_module do každého template
    """
    if not request.user.is_authenticated:
        return {'user_has_module': {}}

    # Získat všechny aktivní moduly uživatele
    subscriptions = UserModuleSubscription.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('module')

    user_has_module = {
        sub.module.name: True
        for sub in subscriptions
    }

    # Free moduly má každý
    user_has_module.update({
        'project_management': True,
        'task_management': True,
        'lists': True,
        'contacts': True
    })

    return {'user_has_module': user_has_module}
```

Registrace v settings.py:
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... existující ...
                'fdk_cz.context_processors.user_modules',
            ],
        },
    },
]
```

---

## 8. PLATEBNÍ INTEGRACE (Stripe/GoPay)

### 8.1 Stripe Integration (preferováno pro CZ/EU)

```python
# fdk_cz/views/subscription_payment.py

import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from fdk_cz.models import UserModuleSubscription, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def payment_checkout(request, subscription_id):
    """
    Checkout stránka pro Stripe platbu
    """
    subscription = get_object_or_404(
        UserModuleSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    # Zjistit cenu
    if subscription.subscription_type == 'monthly':
        amount = subscription.module.price_monthly
    elif subscription.subscription_type == 'yearly':
        amount = subscription.module.price_yearly
    else:
        amount = 0

    # Vytvořit Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'czk',
                'product_data': {
                    'name': subscription.module.display_name,
                    'description': f"{subscription.get_subscription_type_display()} předplatné",
                },
                'unit_amount': int(amount * 100),  # Stripe požaduje částku v haléřích
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')) + f'?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=request.build_absolute_uri(reverse('payment_failed')),
        client_reference_id=subscription_id,
        customer_email=request.user.email,
        metadata={
            'subscription_id': subscription_id,
            'user_id': request.user.id,
        }
    )

    # Vytvořit Payment záznam
    Payment.objects.create(
        user=request.user,
        subscription=subscription,
        amount=amount,
        currency='CZK',
        status='pending',
        payment_method='stripe',
        external_payment_id=checkout_session.id
    )

    context = {
        'checkout_session_id': checkout_session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'subscription': subscription,
        'amount': amount
    }

    return render(request, 'subscription/payment_checkout.html', context)


@csrf_exempt
def stripe_webhook(request):
    """
    Webhook pro Stripe události (platba dokončena, atd.)
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Získat subscription_id z metadata
        subscription_id = session['metadata']['subscription_id']
        subscription = UserModuleSubscription.objects.get(subscription_id=subscription_id)

        # Aktivovat subscription
        subscription.is_active = True
        subscription.payment_method = 'stripe'
        subscription.external_subscription_id = session['id']
        subscription.save()

        # Aktualizovat Payment záznam
        payment = Payment.objects.filter(
            external_payment_id=session['id']
        ).first()

        if payment:
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()

    return JsonResponse({'status': 'success'})


@login_required
def payment_success(request):
    """
    Stránka po úspěšné platbě
    """
    session_id = request.GET.get('session_id')

    # Najít payment podle session_id
    payment = Payment.objects.filter(
        external_payment_id=session_id,
        user=request.user
    ).first()

    context = {
        'payment': payment,
        'subscription': payment.subscription if payment else None
    }

    return render(request, 'subscription/payment_success.html', context)


@login_required
def payment_failed(request):
    """
    Stránka po neúspěšné platbě
    """
    return render(request, 'subscription/payment_failed.html')
```

### 8.2 Settings.py konfigurace

```python
# settings.py

# Stripe API Keys
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

# GoPay API Keys (alternativa pro CZ)
GOPAY_GOID = os.getenv('GOPAY_GOID', '')
GOPAY_CLIENT_ID = os.getenv('GOPAY_CLIENT_ID', '')
GOPAY_CLIENT_SECRET = os.getenv('GOPAY_CLIENT_SECRET', '')
```

---

## 9. MANAGEMENT COMMANDS

### 9.1 Inicializace modulů

```python
# fdk_cz/management/commands/init_modules.py

from django.core.management.base import BaseCommand
from fdk_cz.models import Module

class Command(BaseCommand):
    help = 'Inicializovat všechny moduly FDK systému'

    def handle(self, *args, **kwargs):
        modules_data = [
            # FREE moduly
            {
                'name': 'project_management',
                'display_name': 'Správa projektů',
                'display_name_en': 'Project Management',
                'description': 'Kompletní správa projektů s milníky a týmy',
                'short_description': 'Správa projektů',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'url_patterns': ['/projekty/', '/project_', '/projects/'],
                'icon': '🛠️',
                'color': '#3b82f6',
                'order': 1
            },
            {
                'name': 'task_management',
                'display_name': 'Správa úkolů',
                'display_name_en': 'Task Management',
                'description': 'Správa úkolů pro projekty i jednotlivce',
                'short_description': 'Úkoly a ToDo listy',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'url_patterns': ['/ukoly/', '/task_', '/tasks/'],
                'icon': '✅',
                'color': '#10b981',
                'order': 2
            },
            {
                'name': 'lists',
                'display_name': 'Seznamy',
                'display_name_en': 'Lists',
                'description': 'Vlastní seznamy pro organizaci dat (do 10 zdarma)',
                'short_description': 'Seznamy',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'free_limit': 10,
                'url_patterns': ['/seznamy/', '/list_', '/lists/'],
                'icon': '📋',
                'color': '#8b5cf6',
                'order': 3
            },
            {
                'name': 'contacts',
                'display_name': 'Adresář kontaktů',
                'display_name_en': 'Address Book',
                'description': 'Správa kontaktů a adres',
                'short_description': 'Kontakty',
                'price_monthly': 0,
                'price_yearly': 0,
                'is_free': True,
                'url_patterns': ['/kontakty/', '/contact', '/contacts/'],
                'icon': '👥',
                'color': '#06b6d4',
                'order': 4
            },

            # PAID moduly
            {
                'name': 'grants',
                'display_name': 'Granty a dotace',
                'display_name_en': 'Grants & Subsidies',
                'description': 'Kompletní životní cyklus dotací - vyhledávání, žádosti, reporting',
                'short_description': 'Granty a dotace',
                'price_monthly': 299,
                'price_yearly': 2990,
                'is_free': False,
                'url_patterns': ['/granty/', '/dotace/', '/grant_', '/grants/'],
                'icon': '💰',
                'color': '#f59e0b',
                'order': 10
            },
            {
                'name': 'test_management',
                'display_name': 'Test Management',
                'display_name_en': 'Test Management',
                'description': 'Testování aplikací, bug tracking, test reporting',
                'short_description': 'Testování aplikací',
                'price_monthly': 199,
                'price_yearly': 1990,
                'is_free': False,
                'url_patterns': ['/testy/', '/test_', '/tests/'],
                'icon': '🧪',
                'color': '#ef4444',
                'order': 11
            },
            {
                'name': 'accounting',
                'display_name': 'Účetnictví',
                'display_name_en': 'Accounting',
                'description': 'Kompletní účetnictví s fakturací a DPH',
                'short_description': 'Faktury a účetnictví',
                'price_monthly': 399,
                'price_yearly': 3990,
                'is_free': False,
                'url_patterns': ['/ucetnictvi/', '/accounting/', '/faktury/', '/invoice'],
                'icon': '📊',
                'color': '#14b8a6',
                'order': 12
            },
            {
                'name': 'warehouse',
                'display_name': 'Skladové hospodářství',
                'display_name_en': 'Warehouse Management',
                'description': 'Správa skladu, příjemky, výdejky',
                'short_description': 'Sklad',
                'price_monthly': 249,
                'price_yearly': 2490,
                'is_free': False,
                'url_patterns': ['/sklad/', '/warehouse/'],
                'icon': '📦',
                'color': '#f97316',
                'order': 13
            },
            {
                'name': 'contracts',
                'display_name': 'Správa smluv',
                'display_name_en': 'Contract Management',
                'description': 'Správa smluv a dokumentů',
                'short_description': 'Smlouvy',
                'price_monthly': 199,
                'price_yearly': 1990,
                'is_free': False,
                'url_patterns': ['/smlouvy/', '/contract'],
                'icon': '📄',
                'color': '#6366f1',
                'order': 14
            },
            {
                'name': 'law_ai',
                'display_name': 'Legal Compliance & Law AI',
                'display_name_en': 'Legal Compliance & Law AI',
                'description': 'Právní compliance a AI asistent pro právní dotazy',
                'short_description': 'Právo AI',
                'price_monthly': 499,
                'price_yearly': 4990,
                'is_free': False,
                'url_patterns': ['/pravo-ai/', '/law/', '/pravo/'],
                'icon': '⚖️',
                'color': '#8b5cf6',
                'order': 15
            },
            {
                'name': 'hr_management',
                'display_name': 'HR Management',
                'display_name_en': 'HR Management',
                'description': 'Správa zaměstnanců, docházka, mzdy',
                'short_description': 'HR',
                'price_monthly': 349,
                'price_yearly': 3490,
                'is_free': False,
                'url_patterns': ['/hr/', '/zamestnanci/'],
                'icon': '💼',
                'color': '#ec4899',
                'order': 16
            },
            {
                'name': 'b2b_management',
                'display_name': 'B2B Management',
                'display_name_en': 'B2B Management',
                'description': 'Správa B2B vztahů a obchodních příležitostí',
                'short_description': 'B2B',
                'price_monthly': 349,
                'price_yearly': 3490,
                'is_free': False,
                'url_patterns': ['/b2b/', '/business/'],
                'icon': '🤝',
                'color': '#06b6d4',
                'order': 17
            },
            {
                'name': 'risk_management',
                'display_name': 'Správa rizik',
                'display_name_en': 'Risk Management',
                'description': 'Identifikace a správa rizik projektu/organizace',
                'short_description': 'Rizika',
                'price_monthly': 299,
                'price_yearly': 2990,
                'is_free': False,
                'url_patterns': ['/rizika/', '/risk/'],
                'icon': '⚠️',
                'color': '#f59e0b',
                'order': 18
            },
            {
                'name': 'it_management',
                'display_name': 'Správa IT + ITIL',
                'display_name_en': 'IT Management + ITIL',
                'description': 'IT správa s ITIL procesy (Incident, Change, Problem Management)',
                'short_description': 'IT Management',
                'price_monthly': 449,
                'price_yearly': 4490,
                'is_free': False,
                'url_patterns': ['/it/', '/sprava-it/', '/itil/'],
                'icon': '💻',
                'color': '#3b82f6',
                'order': 19
            },
            {
                'name': 'asset_management',
                'display_name': 'Správa majetku',
                'display_name_en': 'Asset Management',
                'description': 'Správa majetku organizace, inventarizace',
                'short_description': 'Majetek',
                'price_monthly': 299,
                'price_yearly': 2990,
                'is_free': False,
                'url_patterns': ['/majetek/', '/asset/'],
                'icon': '🏢',
                'color': '#64748b',
                'order': 20
            },
        ]

        for data in modules_data:
            module, created = Module.objects.update_or_create(
                name=data['name'],
                defaults=data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Vytvořen modul: {module.display_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'🔄 Aktualizován modul: {module.display_name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Inicializace dokončena! Vytvořeno/aktualizováno {len(modules_data)} modulů.'))
```

Spuštění:
```bash
python manage.py init_modules
```

### 9.2 Kontrola expirovaných subscriptions

```python
# fdk_cz/management/commands/check_expired_subscriptions.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from fdk_cz.models import UserModuleSubscription

class Command(BaseCommand):
    help = 'Deaktivovat vypršená předplatná'

    def handle(self, *args, **kwargs):
        expired = UserModuleSubscription.objects.filter(
            is_active=True,
            end_date__lt=timezone.now()
        )

        count = expired.count()

        for sub in expired:
            sub.is_active = False
            sub.save()
            self.stdout.write(f'❌ Deaktivováno: {sub.user.username} - {sub.module.display_name}')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Deaktivováno {count} vypršených předplatných.'))
```

Nastavit Cron job:
```bash
# Každý den v 1:00 ráno
0 1 * * * cd /path/to/fdk.cz && python manage.py check_expired_subscriptions
```

---

## 10. IMPLEMENTAČNÍ FÁZE

### Fáze 1: Databáze & Modely (1 den)
- ✅ Odkomentovat a rozšířit modely v models.py
- ✅ Vytvořit migrace
- ✅ Spustit migrate
- ✅ Vytvořit init_modules command
- ✅ Inicializovat moduly

### Fáze 2: Middleware & Access Control (1 den)
- ✅ Implementovat ModuleAccessMiddleware
- ✅ Registrovat v settings.py
- ✅ Vytvořit context processor pro user_modules
- ✅ Testovat kontrolu přístupu

### Fáze 3: Views & Forms (2 dny)
- ✅ Implementovat subscription.py views
- ✅ Vytvořit subscription forms
- ✅ Vytvořit URL routing
- ✅ Testovat flow

### Fáze 4: Templates & UI (2 dny)
- ✅ Vytvořit subscription templates
- ✅ Upravit base.html menu
- ✅ Přidat dynamické zobrazení locked/unlocked modulů
- ✅ Styling

### Fáze 5: Platební integrace (2-3 dny)
- ✅ Nastavit Stripe API keys
- ✅ Implementovat payment_checkout
- ✅ Implementovat webhook
- ✅ Testovat platby (sandbox mode)

### Fáze 6: Testing & Debug (1-2 dny)
- ✅ Unit testy
- ✅ Integration testy
- ✅ Manual testing
- ✅ Bug fixing

**Celkový čas: 9-11 dní**

---

## 11. BEZPEČNOSTNÍ OPATŘENÍ

1. **Middleware security**
   - Kontrolovat expiraci při každém requestu
   - Cachovat subscription check (max 5 minut)
   - Log všechny pokusy o přístup k locked modulům

2. **Platební security**
   - HTTPS only pro payment pages
   - Stripe webhook signature verification
   - CSRF tokens
   - Rate limiting na payment endpoints

3. **Database security**
   - Index na (user_id, is_active)
   - Soft delete pro subscriptions (archivace)
   - Audit log pro všechny subscription changes

---

## 12. ANALYTICS & REPORTING

### 12.1 Metriky k trackování
- Počet aktivních subscriptions podle modulu
- Monthly Recurring Revenue (MRR)
- Churn rate
- Conversion rate (free → paid)
- Nejoblíbenější moduly
- Využití modulů (ModuleUsage table)

### 12.2 Dashboard pro adminy
```python
# Admin dashboard endpoint
path('admin/subscription-stats/', admin_views.subscription_stats, name='admin_subscription_stats')
```

---

## 13. DALŠÍ ROZŠÍŘENÍ (budoucnost)

1. **Trial periody** - 14 dní zdarma pro placené moduly
2. **Affiliate program** - Provize za doporučení
3. **Team subscriptions** - Předplatné pro celou organizaci
4. **API access** - REST API jako placený addon
5. **White label** - Vlastní branding jako Enterprise feature
6. **Custom modules** - Zákazník si objedná custom modul

---

## 14. ZÁVĚR

Tento design document poskytuje kompletní architekturu subscription systému pro FDK.cz. Systém je:

- ✅ **Škálovatelný** - Podporuje 1000+ organizací
- ✅ **Flexibilní** - Snadné přidání nových modulů
- ✅ **Bezpečný** - Middleware kontrola + platební integrace
- ✅ **Monetizovatelný** - Stripe/GoPay integrace
- ✅ **Uživatelsky přívětivý** - Jasné UI pro správu předplatných

**Další krok: Začít implementaci Fáze 1 - Databáze & Modely**

---

**Konec dokumentu**
