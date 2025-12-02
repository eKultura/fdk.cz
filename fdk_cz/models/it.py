# -------------------------------------------------------------------
#                    MODELS.IT
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ITAsset(models.Model):
    """IT majetek a zařízení"""
    asset_id = models.AutoField(primary_key=True, db_column='asset_id')

    # Základní údaje
    name = models.CharField(max_length=255, db_column='name')
    asset_tag = models.CharField(max_length=100, unique=True, db_column='asset_tag')  # unikátní označení
    description = models.TextField(null=True, blank=True, db_column='description')

    # Kategorizace
    ASSET_TYPE_CHOICES = [
        ('server', 'Server'),
        ('workstation', 'Pracovní stanice'),
        ('laptop', 'Notebook'),
        ('mobile', 'Mobilní zařízení'),
        ('network', 'Síťové zařízení'),
        ('storage', 'Úložiště'),
        ('printer', 'Tiskárna'),
        ('software', 'Software'),
        ('license', 'Licence'),
        ('other', 'Jiné')
    ]
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, db_column='asset_type')

    # Technické údaje
    manufacturer = models.CharField(max_length=100, null=True, blank=True, db_column='manufacturer')
    model = models.CharField(max_length=100, null=True, blank=True, db_column='model')
    serial_number = models.CharField(max_length=100, null=True, blank=True, db_column='serial_number')

    # Vztahy
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='it_assets', db_column='organization_id')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_it_assets', db_column='assigned_to_id')

    # Životní cyklus
    purchase_date = models.DateField(null=True, blank=True, db_column='purchase_date')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='purchase_price')
    warranty_expiry = models.DateField(null=True, blank=True, db_column='warranty_expiry')

    STATUS_CHOICES = [
        ('active', 'Aktivní'),
        ('in_repair', 'V opravě'),
        ('stored', 'Uskladněno'),
        ('disposed', 'Vyřazeno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_column='status')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_it_asset'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.asset_tag})"



class ITIncident(models.Model):
    """IT incidenty (ITIL Incident Management)"""
    incident_id = models.AutoField(primary_key=True, db_column='incident_id')

    # Základní údaje
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(db_column='description')
    incident_number = models.CharField(max_length=50, unique=True, db_column='incident_number')

    # Vztahy
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='it_incidents', db_column='organization_id')
    affected_asset = models.ForeignKey(ITAsset, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='incidents', db_column='affected_asset_id')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='reported_incidents', db_column='reported_by_id')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_incidents', db_column='assigned_to_id')

    # Priorita a závažnost
    PRIORITY_CHOICES = [
        ('low', 'Nízká'),
        ('medium', 'Střední'),
        ('high', 'Vysoká'),
        ('critical', 'Kritická')
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', db_column='priority')

    # Status
    STATUS_CHOICES = [
        ('new', 'Nový'),
        ('assigned', 'Přiřazeno'),
        ('in_progress', 'Řešení'),
        ('resolved', 'Vyřešeno'),
        ('closed', 'Uzavřeno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', db_column='status')

    # Časové údaje
    reported_at = models.DateTimeField(auto_now_add=True, db_column='reported_at')
    resolved_at = models.DateTimeField(null=True, blank=True, db_column='resolved_at')
    closed_at = models.DateTimeField(null=True, blank=True, db_column='closed_at')

    # Řešení
    resolution_notes = models.TextField(null=True, blank=True, db_column='resolution_notes')

    class Meta:
        db_table = 'FDK_it_incident'
        ordering = ['-reported_at']

    def __str__(self):
        return f"{self.incident_number} - {self.title}"


# -------------------------------------------------------------------
#                    ASSET MANAGEMENT
# -------------------------------------------------------------------

