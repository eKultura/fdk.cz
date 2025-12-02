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



class ProjectTask(models.Model):
    STATUS_CHOICES = [
        ('Ke zpracování', 'Ke zpracování'),
        ('Probíhá', 'Probíhá'),
        ('Hotovo', 'Hotovo'),
        ('Nice to have', 'Nice to have'), 
    ]
    task_id = models.AutoField(primary_key=True, db_column='task_id')
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(null=True, blank=True, db_column='description')
    category = models.ForeignKey('ProjectCategory', on_delete=models.CASCADE, null=True, related_name='tasks', db_column='category_id')
    priority = models.CharField(max_length=16, null=True, blank=True, db_column='priority')
    status = models.CharField(max_length=50, null=True, blank=True, db_column='status')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', db_column='creator_id')
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', db_column='assigned_id')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, related_name='tasks', db_column='project_id')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', db_column='organization_id')
    due_date = models.DateField(null=True, blank=True, db_column='due_date')
    created = models.DateTimeField(null=True, blank=True, db_column='created')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks', db_column='parent_id')
    deleted = models.BooleanField(default=False, db_column='deleted')

    class Meta:
        db_table = 'FDK_tasks'



class ProjectAttachment(models.Model):
    attachment_id = models.AutoField(primary_key=True, db_column='attachment_id')
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='attachments', db_column='task_id')
    file_name = models.CharField(max_length=255, db_column='file_name')
    file_path = models.CharField(max_length=255, db_column='file_path')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_attachments', db_column='uploaded_by')
    uploaded_date = models.DateTimeField(null=True, blank=True, db_column='uploaded_date')

    class Meta:
        db_table = 'FDK_attachments'

class ProjectComment(models.Model):
    comment_id = models.AutoField(primary_key=True, db_column='comment_id')
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE, related_name='comments', db_column='task_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments', db_column='user_id')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, related_name='comments', db_column='project_id')
    comment = models.TextField(null=True, blank=True, db_column='comment')
    posted = models.DateTimeField(null=True, blank=True, db_column='posted')

    class Meta:
        db_table = 'FDK_comments'

class ProjectDocument(models.Model):
    document_id = models.AutoField(primary_key=True, db_column='document_id')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='documents', db_column='project_id')
    document_type = models.CharField(max_length=255, db_column='document_type')
    category = models.ForeignKey('ProjectCategory', on_delete=models.SET_NULL, db_column='category', null=True, blank=True)
    title = models.CharField(max_length=255, db_column='title')
    url = models.CharField(max_length=255, db_column='url')
    description = models.TextField(null=True, blank=True, db_column='description')
    file_path = models.CharField(max_length=255, db_column='file_path')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents', db_column='uploaded_by')
    uploaded_at = models.DateTimeField(auto_now_add=True, db_column='uploaded_at')

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'FDK_documents'

class Flist(models.Model):
    list_id = models.AutoField(primary_key=True, db_column='list_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='lists', db_column='project_id')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_lists', db_column='owner_id')
    is_private = models.BooleanField(default=True, db_column='is_private')
    created = models.DateTimeField(default=timezone.now, db_column='created')  # Přidáme výchozí hodnotu
    modified = models.DateTimeField(auto_now=True, db_column='modified', null=True, blank=True)

    class Meta:
        db_table = 'FDK_lists'

class ListItem(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='item_id')
    flist = models.ForeignKey(Flist, on_delete=models.CASCADE, related_name='items', db_column='list_id')
    content = models.TextField(db_column='content')
    item_order = models.IntegerField(db_column='item_order')
    created = models.DateTimeField(default=timezone.now, db_column='created') 
    modified = models.DateTimeField(auto_now=True, db_column='modified')

    class Meta:
        db_table = 'FDK_list_items'


class ListPermission(models.Model):
    list_permission_id = models.AutoField(primary_key=True, db_column='list_permission_id')
    flist = models.ForeignKey(Flist, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_permissions')
    can_edit = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)

    class Meta:
        db_table = 'FDK_list_permissions'
        unique_together = ('flist', 'user')


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True, db_column='contact_id')
    first_name = models.CharField(max_length=100, db_column='first_name')
    last_name = models.CharField(max_length=100, null=True, blank=True, db_column='last_name')
    phone = models.CharField(max_length=20, null=True, blank=True, db_column='phone')
    email = models.EmailField(max_length=255, null=True, blank=True, db_column='email')
    company = models.CharField(max_length=255, null=True, blank=True, db_column='company')
    description = models.TextField(null=True, blank=True, db_column='description')
    added_on = models.DateTimeField(auto_now_add=True, db_column='added_on')
    last_contacted = models.DateTimeField(null=True, blank=True, db_column='last_contacted')

    # Vazba na projekt nebo účet
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts', db_column='project_id')
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts', db_column='organization_id')
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts', db_column='account_id')

    # Určení, zda je kontakt soukromý nebo sdílený s projektem
    is_private = models.BooleanField(default=True, db_column='is_private')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        db_table = 'FDK_contacts'


### MANAGEMENT SYSTEMS ###
# # # WAREHOUSE # # #
class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True, db_column='warehouse_id')
    name = models.CharField(max_length=255, db_column='name')
    location = models.CharField(max_length=255, db_column='location', null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True, related_name='stores', db_column='project_id')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True, related_name='stores', db_column='organization_id')
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = 'FDK_warehouse'

    def __str__(self):
        return self.name

class WarehouseCategory(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='category_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    class Meta:
        db_table = 'FDK_warehouse_category'
        verbose_name_plural = 'Warehouse Categories'

    def __str__(self):
        return self.name

class WarehouseItem(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='item_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    quantity = models.PositiveIntegerField(default=0, db_column='quantity')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items', db_column='warehouse_id')
    category = models.ForeignKey(WarehouseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items', db_column='category_id')
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = 'FDK_warehouse_item'

    def __str__(self):
        return self.name

class WarehouseTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, db_column='transaction_id')
    item = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE, related_name='transactions', db_column='item_id')
    transaction_type = models.CharField(max_length=10, choices=[('IN', 'Příjem'), ('OUT', 'Výdej')], db_column='transaction_type')
    quantity = models.PositiveIntegerField(db_column='quantity')
    date = models.DateTimeField(auto_now_add=True, db_column='date')

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity})"
    class Meta:
        db_table = 'FDK_warehouse_transaction'

# kategorie - cena (historie)




# # # # # # # # #
class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True, db_column='contract_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    start_date = models.DateField(null=True, blank=True, db_column='start_date')
    end_date = models.DateField(null=True, blank=True, db_column='end_date')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='contracts', db_column='project_id')
    document = models.FileField(upload_to='contracts/', null=True, blank=True)

    class Meta:
        db_table = 'FDK_contract'
# # # # # # # # #


# -------------------------------------------------------------------
#                    TEST MANAGEMENT
# -------------------------------------------------------------------
class TestType(models.Model):
    test_type_id = models.AutoField(primary_key=True, db_column='test_type_id')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='test_types', db_column='project_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    class Meta:
        db_table = 'FDK_test_types'

    def __str__(self):
        return self.name


class Test(models.Model):
    test_id = models.AutoField(primary_key=True, db_column='test_id')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tests', db_column='project_id')
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE, related_name='tests', db_column='test_type_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    grid_location = models.CharField(max_length=2, null=True, blank=True, db_column='grid_location')  # A1, B2, etc.
    date_created = models.DateTimeField(auto_now_add=True, db_column='date_created')

    class Meta:
        db_table = 'FDK_tests'

    def __str__(self):
        return self.name


class TestResult(models.Model):
    test_result_id = models.AutoField(primary_key=True, db_column='test_result_id')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='test_results', db_column='project_id') 
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results', db_column='test_id')
    executed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='executed_tests', db_column='executed_by')
    result = models.CharField(max_length=50, db_column='result')  # Pass, Fail, Blocked, etc.
    execution_date = models.DateTimeField(auto_now_add=True, db_column='execution_date')

    class Meta:
        db_table = 'FDK_test_results'

    def __str__(self):
        return f"{self.test.name} - {self.result}"


class TestError(models.Model):
    STATUS_CHOICES = [
        ('open', 'Otevřená'),
        ('closed', 'Uzavřená'),
        ('in_progress', 'V procesu'),
    ]
    test_error_id = models.AutoField(primary_key=True, db_column='test_error_id')
    test_result = models.ForeignKey(TestResult, db_column='test_result_id', on_delete=models.CASCADE, related_name='errors', null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='test_errors', db_column='project_id') 
    error_title = models.CharField(max_length=255, db_column='error_title')
    description = models.TextField(null=True, blank=True, db_column='description')
    steps_to_replicate = models.TextField(null=True, blank=True, db_column='steps_to_replicate')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_errors')
    date_created = models.DateTimeField(auto_now_add=True, db_column='date_created')
    deleted = models.BooleanField(default=False, db_column='deleted')

    class Meta:
        db_table = 'FDK_test_errors'

    def __str__(self):
        return self.error_title


class TestScenario(models.Model):
    """Testovací scénáře - může existovat na úrovni organizace, projektu nebo uživatele"""
    scenario_id = models.AutoField(primary_key=True, db_column='scenario_id')

    # Základní údaje
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    # Scénář - kroky k provedení
    steps = models.TextField(db_column='steps', help_text='Kroky testovacího scénáře')
    expected_result = models.TextField(null=True, blank=True, db_column='expected_result')

    # Trojjediný kontext (organization/project/personal)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='test_scenarios', db_column='organization_id')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='test_scenarios', db_column='project_id')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='owned_test_scenarios', db_column='owner_id')

    # Kategorie a priorita
    PRIORITY_CHOICES = [
        ('low', 'Nízká'),
        ('medium', 'Střední'),
        ('high', 'Vysoká'),
        ('critical', 'Kritická')
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', db_column='priority')

    STATUS_CHOICES = [
        ('draft', 'Koncept'),
        ('active', 'Aktivní'),
        ('deprecated', 'Zastaralý')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_column='status')

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_test_scenarios', db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_test_scenario'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# # # F A K T U R Y # # #

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
    project = models.ForeignKey('Project', on_delete=models.SET_NULL,
                                related_name='grant_applications',
                                db_column='project_id', null=True, blank=True)
    organization = models.ForeignKey('Company', on_delete=models.SET_NULL,
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
class Law(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    title = models.CharField(max_length=300, db_column='title')
    number = models.CharField(max_length=50, db_column='number')
    year = models.IntegerField(db_column='year')
    content = models.TextField(db_column='content')
    category = models.CharField(max_length=100, db_column='category')
    effective_date = models.DateField(db_column='effective_date')
    created_at = models.DateTimeField(db_column='created_at')

    class Meta:
        db_table = 'FDK_law'

    def __str__(self):
        return f"{self.number}/{self.year} – {self.title}"

class LawDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FDK_law_document'


class LawQuery(models.Model):
    query_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    question = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FDK_law_query'

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

