# -------------------------------------------------------------------
#                    MODELS.ASSET
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AssetCategory(models.Model):
    """Kategorie majetku"""
    category_id = models.AutoField(primary_key=True, db_column='category_id')

    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='asset_categories', db_column='organization_id')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='sub_categories', db_column='parent_category_id')

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_asset_category'
        ordering = ['name']

    def __str__(self):
        return self.name



class Asset(models.Model):
    """Obecný majetek (ne IT)"""
    asset_id = models.AutoField(primary_key=True, db_column='asset_id')

    # Základní údaje
    name = models.CharField(max_length=255, db_column='name')
    asset_number = models.CharField(max_length=100, unique=True, db_column='asset_number')
    description = models.TextField(null=True, blank=True, db_column='description')

    # Kategorizace
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='assets', db_column='category_id')

    # Vztahy
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='assets', db_column='organization_id')
    location = models.CharField(max_length=255, null=True, blank=True, db_column='location')
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='responsible_assets', db_column='responsible_person_id')

    # Finanční údaje
    purchase_date = models.DateField(null=True, blank=True, db_column='purchase_date')
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column='purchase_price')
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column='current_value')
    currency = models.CharField(max_length=3, default='CZK', db_column='currency')

    # Status
    STATUS_CHOICES = [
        ('active', 'Aktivní'),
        ('maintenance', 'Údržba'),
        ('stored', 'Uskladněno'),
        ('disposed', 'Vyřazeno'),
        ('sold', 'Prodáno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_column='status')

    # Metadata
    notes = models.TextField(null=True, blank=True, db_column='notes')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_asset'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.asset_number})"


# -------------------------------------------------------------------
#                    HELP & DOCUMENTATION SYSTEM
# -------------------------------------------------------------------

