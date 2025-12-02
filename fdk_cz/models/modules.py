# -------------------------------------------------------------------
#                    MODELS.MODULES
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ModuleRole(models.Model):
    """
    Role pro jednotlivé moduly (warehouse, contact, invoice, atd.)
    Např.: module_manager, module_viewer
    """
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True, help_text="Stručný popis role")

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'FDK_module_roles'
        verbose_name = 'Modulová role'
        verbose_name_plural = 'Modulové role'



class ModulePermission(models.Model):
    """
    Oprávnění pro moduly (read, write, delete, manage)
    """
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.permission_name

    class Meta:
        db_table = 'FDK_module_permissions'
        verbose_name = 'Modulové oprávnění'
        verbose_name_plural = 'Modulová oprávnění'



class ModuleRolePermission(models.Model):
    """Vazba mezi modulovou rolí a oprávněními"""
    role = models.ForeignKey(ModuleRole, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(ModulePermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')
        db_table = 'FDK_module_role_permissions'



class ModuleAccess(models.Model):
    """
    Přístup uživatele k modulu v rámci projektu nebo organizace
    Např: Jan má roli 'warehouse_manager' pro modul 'warehouse' v projektu X
    """
    MODULE_CHOICES = [
        ('warehouse', 'Sklad'),
        ('contact', 'Kontakty'),
        ('invoice', 'Faktury'),
        ('task', 'Úkoly'),
        ('document', 'Dokumenty'),
        ('milestone', 'Milníky'),
    ]

    access_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_accesses')
    role = models.ForeignKey(ModuleRole, on_delete=models.CASCADE, related_name='accesses')
    module_name = models.CharField(max_length=50, choices=MODULE_CHOICES)

    # Přístup může být buď na úrovni projektu NEBO organizace
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True, related_name='module_accesses')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True, related_name='module_accesses')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FDK_module_access'
        unique_together = ('user', 'module_name', 'project', 'organization')
        verbose_name = 'Modulový přístup'
        verbose_name_plural = 'Modulové přístupy'

    def __str__(self):
        context = self.project.name if self.project else self.organization.name
        return f"{self.user.username} - {self.module_name} ({self.role.role_name}) - {context}"


# -------------------------------------------------------------------
#                    SUBSCRIPTION SYSTEM
# -------------------------------------------------------------------


class Module(models.Model):
    """Model pro moduly FDK systému (Project Management, Granty, Sklad, atd.)"""
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



class UserModuleSubscription(models.Model):
    """Předplatné uživatele na konkrétní modul"""
    subscription_id = models.AutoField(primary_key=True, db_column='subscription_id')

    # Vztahy
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_subscriptions', db_column='user_id')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_subscriptions', db_column='module_id')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='module_subscriptions', db_column='organization_id')

    # Typ předplatného
    SUBSCRIPTION_CHOICES = [
        ('free', 'Zdarma'),
        ('monthly', 'Měsíční'),
        ('yearly', 'Roční'),
        ('lifetime', 'Doživotní'),
        ('trial', 'Zkušební')
    ]
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, db_column='subscription_type')

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



class ModuleBundle(models.Model):
    """Balíčky modulů (Starter, Business, Enterprise)"""
    bundle_id = models.AutoField(primary_key=True, db_column='bundle_id')

    name = models.CharField(max_length=100, db_column='name')  # 'Starter', 'Business', 'Enterprise'
    display_name = models.CharField(max_length=200, db_column='display_name')
    description = models.TextField(db_column='description')

    modules = models.ManyToManyField(Module, related_name='bundles')

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



class Payment(models.Model):
    """Platby za předplatná"""
    payment_id = models.AutoField(primary_key=True, db_column='payment_id')

    # Vztahy
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', db_column='user_id')
    subscription = models.ForeignKey(UserModuleSubscription, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='payments', db_column='subscription_id')

    # Částka
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='amount')
    currency = models.CharField(max_length=3, default='CZK', db_column='currency')

    # Status
    STATUS_CHOICES = [
        ('pending', 'Čeká na zpracování'),
        ('completed', 'Dokončeno'),
        ('failed', 'Selhalo'),
        ('refunded', 'Vráceno'),
        ('cancelled', 'Zrušeno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_column='status')

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



class ModuleUsage(models.Model):
    """Využití modulů - pro analytics"""
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



class UserModulePreference(models.Model):
    """Uživatelské preference pro zobrazení modulů v menu (zapnout/vypnout)"""
    preference_id = models.AutoField(primary_key=True, db_column='preference_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_preferences', db_column='user_id')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_preferences', db_column='module_id')

    # Zobrazovat v menu?
    is_visible = models.BooleanField(default=True, db_column='is_visible')

    # Pořadí v menu (pro uživatelské seřazení)
    display_order = models.IntegerField(default=0, db_column='display_order')

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_user_module_preference'
        unique_together = ('user', 'module')
        ordering = ['display_order', 'module__order']

    def __str__(self):
        return f"{self.user.username} - {self.module.display_name} ({'✓' if self.is_visible else '✗'})"


# -------------------------------------------------------------------
#                    B2B MANAGEMENT
# -------------------------------------------------------------------

