# -------------------------------------------------------------------
#                    MODELS.B2B
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class B2BCompany(models.Model):
    """Spolupracující firmy - externí organizace"""
    company_id = models.AutoField(primary_key=True, db_column='company_id')

    # Základní informace
    name = models.CharField(max_length=255, db_column='name')
    legal_name = models.CharField(max_length=255, null=True, blank=True, db_column='legal_name')
    company_id_number = models.CharField(max_length=50, null=True, blank=True, db_column='company_id_number')  # IČO
    tax_id = models.CharField(max_length=50, null=True, blank=True, db_column='tax_id')  # DIČ

    # Kontaktní údaje
    email = models.EmailField(null=True, blank=True, db_column='email')
    phone = models.CharField(max_length=20, null=True, blank=True, db_column='phone')
    website = models.URLField(null=True, blank=True, db_column='website')

    # Adresa
    street = models.CharField(max_length=255, null=True, blank=True, db_column='street')
    city = models.CharField(max_length=100, null=True, blank=True, db_column='city')
    postal_code = models.CharField(max_length=20, null=True, blank=True, db_column='postal_code')
    country = models.CharField(max_length=100, default='Česká republika', db_column='country')

    # Kategorizace
    CATEGORY_CHOICES = [
        ('supplier', 'Dodavatel'),
        ('customer', 'Zákazník'),
        ('partner', 'Partner'),
        ('competitor', 'Konkurent'),
        ('other', 'Jiné')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_column='category')
    tags = models.CharField(max_length=500, null=True, blank=True, db_column='tags')  # klíčová slova oddělená čárkami

    # Propojení
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='b2b_companies', db_column='organization_id')

    # Metadata
    notes = models.TextField(null=True, blank=True, db_column='notes')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_b2b_companies', db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_b2b_company'
        ordering = ['name']

    def __str__(self):
        return self.name



class B2BContract(models.Model):
    """Smlouvy s B2B firmami"""
    contract_id = models.AutoField(primary_key=True, db_column='contract_id')

    # Vztahy
    company = models.ForeignKey(B2BCompany, on_delete=models.CASCADE, related_name='contracts', db_column='company_id')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='b2b_contracts', db_column='organization_id')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='b2b_contracts', db_column='project_id')

    # Základní údaje
    contract_number = models.CharField(max_length=100, unique=True, db_column='contract_number')
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(null=True, blank=True, db_column='description')

    # Finanční údaje
    contract_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, db_column='contract_value')
    currency = models.CharField(max_length=3, default='CZK', db_column='currency')

    # Časové údaje
    start_date = models.DateField(db_column='start_date')
    end_date = models.DateField(null=True, blank=True, db_column='end_date')
    signed_date = models.DateField(null=True, blank=True, db_column='signed_date')

    # Status
    STATUS_CHOICES = [
        ('draft', 'Koncept'),
        ('negotiation', 'V jednání'),
        ('signed', 'Podepsáno'),
        ('active', 'Aktivní'),
        ('completed', 'Dokončeno'),
        ('terminated', 'Ukončeno'),
        ('cancelled', 'Zrušeno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_column='status')

    # Kategorizace (propojení s DMS)
    categories = models.CharField(max_length=500, null=True, blank=True, db_column='categories')
    keywords = models.CharField(max_length=500, null=True, blank=True, db_column='keywords')

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_b2b_contracts', db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_b2b_contract'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contract_number} - {self.title}"



class B2BDocument(models.Model):
    """Dokumenty propojené s B2B firmami a smlouvami (DMS integrace)"""
    document_id = models.AutoField(primary_key=True, db_column='document_id')

    # Vztahy
    company = models.ForeignKey(B2BCompany, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='documents', db_column='company_id')
    contract = models.ForeignKey(B2BContract, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='documents', db_column='contract_id')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='b2b_documents', db_column='organization_id')

    # Informace o dokumentu
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(null=True, blank=True, db_column='description')
    file_path = models.CharField(max_length=500, null=True, blank=True, db_column='file_path')
    file_url = models.URLField(null=True, blank=True, db_column='file_url')
    file_size = models.IntegerField(null=True, blank=True, db_column='file_size')  # v bajtech
    mime_type = models.CharField(max_length=100, null=True, blank=True, db_column='mime_type')

    # Kategorizace
    document_type = models.CharField(max_length=100, db_column='document_type')  # 'contract', 'invoice', 'quote', etc.
    categories = models.CharField(max_length=500, null=True, blank=True, db_column='categories')
    keywords = models.CharField(max_length=500, null=True, blank=True, db_column='keywords')

    # Verzování
    version = models.CharField(max_length=20, default='1.0', db_column='version')
    is_latest = models.BooleanField(default=True, db_column='is_latest')

    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='uploaded_b2b_documents', db_column='uploaded_by_id')
    uploaded_at = models.DateTimeField(auto_now_add=True, db_column='uploaded_at')

    class Meta:
        db_table = 'FDK_b2b_document'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


# -------------------------------------------------------------------
#                    HR MANAGEMENT
# -------------------------------------------------------------------

