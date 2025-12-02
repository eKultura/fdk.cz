# -------------------------------------------------------------------
#                    MODELS.GRANTS
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class GrantProgram(models.Model):
    program_id = models.AutoField(primary_key=True, db_column='program_id')
    name = models.CharField(max_length=255, db_column='name')
    provider = models.CharField(max_length=255, db_column='provider', null=True, blank=True)
    description = models.TextField(db_column='description', null=True, blank=True)
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, db_column='total_budget',
                                       null=True, blank=True)
    is_active = models.BooleanField(default=True, db_column='is_active')

    class Meta:
        db_table = 'FDK_grant_program'

    def __str__(self):
        return self.name



class GrantCall(models.Model):
    call_id = models.AutoField(primary_key=True, db_column='call_id')
    program = models.ForeignKey(GrantProgram, on_delete=models.SET_NULL,
                                related_name='calls', db_column='program_id',
                                null=True, blank=True)
    title = models.CharField(max_length=255, db_column='title')
    provider = models.CharField(max_length=255, db_column='provider', null=True, blank=True)
    description = models.TextField(db_column='description', null=True, blank=True)
    type = models.CharField(max_length=50, db_column='type',
                            choices=[('dotace', 'Dotace'),
                                     ('grant', 'Grant'),
                                     ('stipendium', 'Stipendium')],
                            default='dotace')
    start_date = models.DateField(db_column='start_date', null=True, blank=True)
    end_date = models.DateField(db_column='end_date', null=True, blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, db_column='budget',
                                 null=True, blank=True)
    eligibility = models.TextField(db_column='eligibility', null=True, blank=True)
    status = models.CharField(max_length=20, db_column='status',
                              choices=[('upcoming', 'Upcoming'),
                                       ('open', 'Open'),
                                       ('closed', 'Closed')],
                              default='open')
    is_active = models.BooleanField(default=True, db_column='is_active')
    published_at = models.DateField(auto_now_add=True, db_column='published_at')

    # ✅ NOVÉ: Zdroj dotace a externí integrace
    source = models.CharField(
        max_length=50,
        choices=[
            ('manual', 'Manuální'),
            ('dotaceeu', 'DotaceEU'),
            ('msmt', 'MŠMT'),
            ('other_api', 'Jiné API')
        ],
        default='manual',
        db_column='source'
    )
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_column='external_id',
        help_text='ID z externí databáze (dotaceEU, MŠMT)'
    )

    # Číslo dotace (např. od Ministerstva Kultury)
    grant_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='grant_number',
        help_text='Oficiální číslo dotace (např. 1508)'
    )
    grant_subnumber = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='grant_subnumber',
        help_text='Podčíslo dotace (pokud existuje)'
    )
    source_url = models.URLField(
        null=True,
        blank=True,
        db_column='source_url',
        help_text='Odkaz na dotaci v původním systému'
    )
    external_metadata = models.JSONField(
        default=dict,
        db_column='external_metadata',
        help_text='Dodatečná data z externího API'
    )
    last_synced = models.DateTimeField(
        null=True,
        blank=True,
        db_column='last_synced'
    )

    # ✅ NOVÉ: Rozšířené informace
    tags = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column='tags',
        help_text='Tagy oddělené čárkami: startup,inovace,kultura'
    )
    min_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='min_amount'
    )
    max_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='max_amount'
    )
    priority = models.IntegerField(
        default=0,
        db_column='priority',
        help_text='Vyšší číslo = vyšší priorita zobrazení'
    )

    class Meta:
        db_table = 'FDK_grant_call'
        indexes = [
            models.Index(fields=['external_id']),
            models.Index(fields=['source', 'is_active']),
            models.Index(fields=['-priority', '-published_at']),
            models.Index(fields=['status', 'end_date']),
        ]

    def __str__(self):
        return self.title

    def is_open_for_applications(self):
        """Kontrola, zda je výzva otevřená pro podání žádostí"""
        from datetime import date
        today = date.today()
        if not self.is_active or self.status != 'open':
            return False
        if self.start_date and self.start_date > today:
            return False
        if self.end_date and self.end_date < today:
            return False
        return True

    def days_until_deadline(self):
        """Počet dní do uzávěrky"""
        from datetime import date
        if not self.end_date:
            return None
        delta = self.end_date - date.today()
        return delta.days if delta.days >= 0 else 0



class GrantRequirement(models.Model):
    requirement_id = models.AutoField(primary_key=True, db_column='requirement_id')
    call = models.ForeignKey(GrantCall, on_delete=models.CASCADE,
                             related_name='requirements', db_column='call_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(db_column='description', null=True, blank=True)
    is_mandatory = models.BooleanField(default=True, db_column='is_mandatory')

    class Meta:
        db_table = 'FDK_grant_requirement'

    def __str__(self):
        return self.name



class GrantApplication(models.Model):
    application_id = models.AutoField(primary_key=True, db_column='application_id')
    call = models.ForeignKey(GrantCall, on_delete=models.CASCADE,
                             related_name='applications', db_column='call_id')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL,
                                related_name='grant_applications',
                                db_column='project_id', null=True, blank=True)
    organization = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                     related_name='grant_applications',
                                     db_column='organization_id', null=True, blank=True)
    applicant = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  related_name='submitted_applications',
                                  db_column='applicant_id', null=True, blank=True)
    submission_date = models.DateField(db_column='submission_date', null=True, blank=True)
    approval_date = models.DateField(db_column='approval_date', null=True, blank=True)
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                           db_column='requested_amount',
                                           null=True, blank=True)
    granted_amount = models.DecimalField(max_digits=12, decimal_places=2,
                                         db_column='granted_amount',
                                         null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='draft', db_column='status')
    notes = models.TextField(db_column='notes', null=True, blank=True)
    is_successful = models.BooleanField(default=False, db_column='is_successful')
    is_visible = models.BooleanField(default=True, db_column='is_visible')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    # ✅ NOVÉ: Fáze životního cyklu dotace
    lifecycle_stage = models.CharField(
        max_length=50,
        choices=[
            ('preparation', 'Příprava žádosti'),
            ('submitted', 'Odesláno'),
            ('under_review', 'Probíhá hodnocení'),
            ('approved', 'Schváleno'),
            ('rejected', 'Zamítnuto'),
            ('in_progress', 'V realizaci'),
            ('reporting', 'Reporting'),
            ('completed', 'Ukončeno'),
            ('archived', 'Archivováno')
        ],
        default='preparation',
        db_column='lifecycle_stage'
    )

    # ✅ NOVÉ: Reporting a monitoring
    report_deadline = models.DateField(
        null=True,
        blank=True,
        db_column='report_deadline',
        help_text='Termín odevzdání závěrečné zprávy'
    )
    last_report_submitted = models.DateTimeField(
        null=True,
        blank=True,
        db_column='last_report_submitted'
    )

    # ✅ NOVÉ: Skutečně získaná částka
    actual_received_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='actual_received_amount',
        help_text='Skutečně obdržená částka (může se lišit od schválené)'
    )

    # ✅ NOVÉ: Průběh realizace
    completion_percentage = models.IntegerField(
        default=0,
        db_column='completion_percentage',
        help_text='Stupeň dokončení projektu (0-100%)'
    )

    class Meta:
        db_table = 'FDK_grant_application'
        indexes = [
            models.Index(fields=['lifecycle_stage', '-created_at']),
            models.Index(fields=['report_deadline']),
        ]

    def __str__(self):
        return f"{self.applicant} → {self.call}"



class GrantApplicationDocument(models.Model):
    document_id = models.AutoField(primary_key=True, db_column='document_id')
    application = models.ForeignKey(GrantApplication, on_delete=models.CASCADE,
                                    related_name='documents', db_column='application_id')
    requirement = models.ForeignKey(GrantRequirement, on_delete=models.SET_NULL,
                                    related_name='application_documents',
                                    db_column='requirement_id', null=True, blank=True)
    file = models.FileField(upload_to='grant_documents/', db_column='file')
    uploaded_at = models.DateTimeField(auto_now_add=True, db_column='uploaded_at')

    class Meta:
        db_table = 'FDK_grant_application_document'

    def __str__(self):
        return f"Dokument {self.document_id} k žádosti {self.application_id}"



class GrantOpportunityBookmark(models.Model):
    """Uživatelé si mohou označit zajímavé dotační příležitosti"""
    bookmark_id = models.AutoField(primary_key=True, db_column='bookmark_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grant_bookmarks', db_column='user_id')
    call = models.ForeignKey(GrantCall, on_delete=models.CASCADE, related_name='bookmarks', db_column='call_id')

    notes = models.TextField(null=True, blank=True, db_column='notes', help_text='Osobní poznámky k příležitosti')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_grant_opportunity_bookmark'
        unique_together = ('user', 'call')

    def __str__(self):
        return f"{self.user.username} - {self.call.title}"



class GrantDocumentTemplate(models.Model):
    """Šablony dokumentů pro průvodce generováním"""
    template_id = models.AutoField(primary_key=True, db_column='template_id')

    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    document_type = models.CharField(
        max_length=100,
        choices=[
            ('project_description', 'Popis projektu'),
            ('budget', 'Rozpočet'),
            ('timeline', 'Časový harmonogram'),
            ('team', 'Složení týmu'),
            ('motivation', 'Motivační dopis'),
            ('references', 'Reference'),
            ('other', 'Jiné')
        ],
        db_column='document_type'
    )

    # JSON schéma pro dynamická pole formuláře
    fields_schema = models.JSONField(
        default=list,
        db_column='fields_schema',
        help_text='JSON pole objektů: [{"name": "field_name", "type": "text", "label": "Label", "required": true}]'
    )
    # Příklad: [{"name": "project_name", "type": "text", "label": "Název projektu", "required": true}, ...]

    # Markdown šablona s placeholdery
    template_content = models.TextField(
        db_column='template_content',
        help_text='Markdown šablona s {{placeholders}}'
    )
    # Příklad: "# {{project_name}}\n\nPopis: {{description}}"

    is_active = models.BooleanField(default=True, db_column='is_active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_grant_document_template'

    def __str__(self):
        return f"{self.name} ({self.document_type})"



# -------------------------------------------------------------------
#                    LAW
# -------------------------------------------------------------------
