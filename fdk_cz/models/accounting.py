# -------------------------------------------------------------------
#                    MODELS.ACCOUNTING
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True, db_column='invoice_id')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='invoices', db_column='company_id', null=True, blank=True)  # Legacy - kept for backwards compatibility
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='invoices', db_column='organization_id', null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, related_name='invoices', db_column='project_id', null=True, blank=True)
    invoice_number = models.CharField(max_length=20, unique=True, db_column='invoice_number')
    issue_date = models.DateField(db_column='issue_date')
    due_date = models.DateField(db_column='due_date')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_price')
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='vat_amount')
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=21, db_column='vat_rate')  # Standardní sazba 21 %
    is_paid = models.BooleanField(default=False, db_column='is_paid')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_invoices', db_column='created_by')

    class Meta:
        db_table = 'FDK_invoice'

    def __str__(self):
        return f"Faktura {self.invoice_number}"

    def generate_invoice_number(self):
        last_invoice = Invoice.objects.filter(issue_date__year=self.issue_date.year).order_by('invoice_id').last()
        if last_invoice:
            last_number = int(last_invoice.invoice_number.split('-')[-1]) + 1
        else:
            last_number = 1
        return f"{self.issue_date.year}-{self.issue_date.month:02d}-{last_number:04d}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)





class InvoiceItem(models.Model):
    invoice_item_id = models.AutoField(primary_key=True, db_column='invoice_item_id')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', db_column='invoice_id')
    description = models.CharField(max_length=255, db_column='description')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, db_column='quantity')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='unit_price')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_price')
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=21, db_column='vat_rate')  

    class Meta:
        db_table = 'FDK_invoice_item'

    def __str__(self):
        return self.description


# -------------------------------------------------------------------
#                    ACCOUNTING EXPANSION
# -------------------------------------------------------------------


class AccountingContext(models.Model):
    """
    Kontext účetnictví - definuje, zda se jedná o osobní (OSVČ)
    nebo organizační účetnictví
    """
    context_id = models.AutoField(primary_key=True, db_column='context_id')

    # Vztahy - buď osobní (user) nebo organizační (organization)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name='accounting_contexts',
                            db_column='user_id',
                            help_text='Vlastník účetnictví')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,
                                    null=True, blank=True,
                                    related_name='accounting_contexts',
                                    db_column='organization_id',
                                    help_text='Organizace (pokud je organizační)')

    # Typ účetnictví
    ACCOUNTING_TYPE_CHOICES = [
        ('personal', 'Osobní (OSVČ)'),
        ('organizational', 'Organizační'),
    ]
    accounting_type = models.CharField(
        max_length=20,
        choices=ACCOUNTING_TYPE_CHOICES,
        db_column='accounting_type',
        help_text='Typ účetnictví'
    )

    # Metoda účetnictví
    ACCOUNTING_METHOD_CHOICES = [
        ('simple', 'Jednoduché účetnictví'),
        ('double_entry', 'Podvojné účetnictví'),
    ]
    accounting_method = models.CharField(
        max_length=20,
        choices=ACCOUNTING_METHOD_CHOICES,
        default='double_entry',
        db_column='accounting_method'
    )

    # Fiskální rok
    fiscal_year = models.IntegerField(db_column='fiscal_year',
                                     help_text='Fiskální rok (např. 2025)')

    # Název kontextu (pro rozlišení více účetních knih)
    name = models.CharField(max_length=255, db_column='name',
                           help_text='Název účetní knihy')

    # Metadata
    is_active = models.BooleanField(default=True, db_column='is_active')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_accounting_context'
        unique_together = ('user', 'organization', 'fiscal_year', 'name')
        ordering = ['-fiscal_year', 'name']

    def __str__(self):
        if self.organization:
            return f"{self.organization.name} - {self.fiscal_year} - {self.name}"
        return f"Osobní ({self.user.username}) - {self.fiscal_year} - {self.name}"



class AccountingAccount(models.Model):
    """
    Účty účtové osnovy (221, 321, 518, atd.)
    """
    account_id = models.AutoField(primary_key=True, db_column='account_id')

    # Vztahy
    context = models.ForeignKey(AccountingContext, on_delete=models.CASCADE,
                               related_name='accounts',
                               db_column='context_id')

    # Číslo a název účtu
    account_number = models.CharField(max_length=20, db_column='account_number',
                                     help_text='Číslo účtu (221, 321, 518...)')
    name = models.CharField(max_length=255, db_column='name',
                           help_text='Název účtu')

    # Typ účtu
    ACCOUNT_TYPE_CHOICES = [
        ('asset', 'Aktiva'),
        ('liability', 'Pasiva'),
        ('equity', 'Vlastní kapitál'),
        ('revenue', 'Výnosy'),
        ('expense', 'Náklady'),
    ]
    account_type = models.CharField(max_length=20,
                                   choices=ACCOUNT_TYPE_CHOICES,
                                   db_column='account_type')

    # Hierarchie - pro podúčty
    parent_account = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name='sub_accounts',
                                      db_column='parent_account_id')

    # Metadata
    description = models.TextField(null=True, blank=True, db_column='description')
    is_active = models.BooleanField(default=True, db_column='is_active')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_accounting_account'
        unique_together = ('context', 'account_number')
        ordering = ['account_number']
        indexes = [
            models.Index(fields=['context', 'account_type']),
            models.Index(fields=['account_number']),
        ]

    def __str__(self):
        return f"{self.account_number} - {self.name}"



class JournalEntry(models.Model):
    """
    Účetní zápis (položka účetního deníku)
    """
    entry_id = models.AutoField(primary_key=True, db_column='entry_id')

    # Vztahy
    context = models.ForeignKey(AccountingContext, on_delete=models.CASCADE,
                               related_name='journal_entries',
                               db_column='context_id')

    # Základní údaje
    entry_number = models.CharField(max_length=50, db_column='entry_number',
                                   help_text='Číslo účetního zápisu')
    entry_date = models.DateField(db_column='entry_date',
                                  help_text='Datum účetního případu')

    # Popis a reference
    description = models.TextField(db_column='description',
                                   help_text='Popis účetního případu')
    document_number = models.CharField(max_length=100, null=True, blank=True,
                                      db_column='document_number',
                                      help_text='Číslo dokladu (faktury, pokladního dokladu...)')

    # Reference na fakturu (pokud souvisí)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='journal_entries',
                               db_column='invoice_id')

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='created_journal_entries',
                                  db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    # Status
    is_posted = models.BooleanField(default=True, db_column='is_posted',
                                   help_text='Je zaúčtováno?')

    class Meta:
        db_table = 'FDK_journal_entry'
        ordering = ['-entry_date', '-entry_number']
        indexes = [
            models.Index(fields=['context', 'entry_date']),
            models.Index(fields=['entry_number']),
        ]

    def __str__(self):
        return f"{self.entry_number} - {self.entry_date} - {self.description[:50]}"



class JournalEntryLine(models.Model):
    """
    Řádek účetního zápisu - podvojný zápis (MD/D)
    """
    line_id = models.AutoField(primary_key=True, db_column='line_id')

    # Vztahy
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE,
                                     related_name='lines',
                                     db_column='entry_id')
    account = models.ForeignKey(AccountingAccount, on_delete=models.CASCADE,
                               related_name='journal_lines',
                               db_column='account_id')

    # Částky - podvojný zápis
    debit_amount = models.DecimalField(max_digits=15, decimal_places=2,
                                      default=0,
                                      db_column='debit_amount',
                                      help_text='Má dáti (MD)')
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2,
                                       default=0,
                                       db_column='credit_amount',
                                       help_text='Dal (D)')

    # Popis řádku
    description = models.CharField(max_length=500, null=True, blank=True,
                                  db_column='description')

    # Pořadí řádků
    line_order = models.IntegerField(default=0, db_column='line_order')

    class Meta:
        db_table = 'FDK_journal_entry_line'
        ordering = ['journal_entry', 'line_order']
        indexes = [
            models.Index(fields=['journal_entry', 'account']),
        ]

    def __str__(self):
        return f"{self.account.account_number} - MD: {self.debit_amount}, D: {self.credit_amount}"



class BalanceSheet(models.Model):
    """
    Rozvaha - počáteční a konečná (podle fiskálního roku)
    """
    balance_id = models.AutoField(primary_key=True, db_column='balance_id')

    # Vztahy
    context = models.ForeignKey(AccountingContext, on_delete=models.CASCADE,
                               related_name='balance_sheets',
                               db_column='context_id')
    account = models.ForeignKey(AccountingAccount, on_delete=models.CASCADE,
                               related_name='balance_entries',
                               db_column='account_id')

    # Typ rozvahy
    BALANCE_TYPE_CHOICES = [
        ('opening', 'Počáteční'),
        ('closing', 'Konečná'),
    ]
    balance_type = models.CharField(max_length=20,
                                   choices=BALANCE_TYPE_CHOICES,
                                   db_column='balance_type')

    # Fiskální rok
    fiscal_year = models.IntegerField(db_column='fiscal_year')

    # Částky
    debit_balance = models.DecimalField(max_digits=15, decimal_places=2,
                                       default=0,
                                       db_column='debit_balance',
                                       help_text='Zůstatek MD')
    credit_balance = models.DecimalField(max_digits=15, decimal_places=2,
                                        default=0,
                                        db_column='credit_balance',
                                        help_text='Zůstatek D')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_balance_sheet'
        unique_together = ('context', 'account', 'balance_type', 'fiscal_year')
        ordering = ['fiscal_year', 'account__account_number']
        indexes = [
            models.Index(fields=['context', 'fiscal_year', 'balance_type']),
        ]

    def __str__(self):
        return f"{self.account.account_number} - {self.get_balance_type_display()} {self.fiscal_year}"


# -------------------------------------------------------------------
#                    GRANTY A DOTACE
# -------------------------------------------------------------------
STATUS_CHOICES = [
    ('draft', 'Koncept'),
    ('submitted', 'Odesláno'),
    ('approved', 'Schváleno'),
    ('rejected', 'Zamítnuto'),
    ('in_progress', 'V procesu'),
]


