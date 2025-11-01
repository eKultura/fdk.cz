# -------------------------------------------------------------------
#                    FDK.CZ.MODELS.PY
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User 

from django.utils import timezone


class ActivityLog(models.Model):
    log_id = models.AutoField(primary_key=True, db_column='log_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs', db_column='user_id')
    user_action = models.CharField(max_length=100, db_column='user_action')
    description = models.TextField(null=True, blank=True, db_column='description')
    date_time = models.DateTimeField(null=True, blank=True, db_column='date_time')

    class Meta:
        db_table = 'FDK_activity_log'

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('Page', 'Webová stránka'),          # O nás, GDPR, Kontakt
        ('Help', 'Nápověda / Dokumentace'),  # Interní nebo uživatelská nápověda
        ('Announcement', 'Oznámení / Novinka'),  # Např. "Nová verze modulu", "Výpadek"
        ('Blog', 'Blogový příspěvek'),       # Dlouhodobé texty, inspirace
        ('Internal', 'Interní poznámka'),    # Jen pro interní uživatele (role admin/editor)
    ]

    title = models.CharField(max_length=255, db_column='title')
    slug = models.SlugField(max_length=255, unique=True, db_column='slug')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Page', db_column='category')
    
    content = models.TextField(db_column='content')
    summary = models.TextField(null=True, blank=True, db_column='summary', help_text="Krátký perex nebo popis")

    meta_header = models.TextField(blank=True, help_text="HTML kód do <head> (např. knihovny, meta tagy)", db_column='meta_header')
    meta_footer = models.TextField(blank=True, help_text="HTML/JS kód před </body>", db_column='meta_footer')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', db_column='author_id')
    is_published = models.BooleanField(default=True, db_column='is_published')
    is_featured = models.BooleanField(default=False, db_column='is_featured', help_text="Zobrazit v hlavních oznámeních nebo na dashboardu")

    created_at = models.DateTimeField(default=timezone.now, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = "FDK_articles"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.slug}"

class Users2(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=100, unique=True, db_column='username')
    password_hash = models.CharField(max_length=255, db_column='password_hash')
    email = models.EmailField(max_length=255, unique=True, db_column='email')
    description = models.CharField(max_length=512, null=True, blank=True, db_column='description')
    created = models.DateTimeField(null=True, blank=True, db_column='created')
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')

    class Meta:
        db_table = 'FDK_users'


class Company(models.Model):
    company_id = models.AutoField(primary_key=True, db_column='company_id')
    name = models.CharField(max_length=255, db_column='name')
    # struktura pro adresu
    street = models.CharField(max_length=128, db_column='street')  # Ulice
    street_number = models.CharField(max_length=10, db_column='street_number')  # Číslo ulice
    city = models.CharField(max_length=128, db_column='city')  # Město
    postal_code = models.CharField(max_length=20, db_column='postal_code')  # PSČ
    state = models.CharField(max_length=128, db_column='state')  # Stát
  
    ico = models.CharField(max_length=20, unique=True, db_column='ico')  # IČO
    dic = models.CharField(max_length=20, blank=True, null=True, db_column='dic')  # DIČ (volitelně)
    phone = models.CharField(max_length=15, blank=True, null=True, db_column='phone')
    email = models.EmailField(blank=True, null=True, db_column='email')
    is_vat_payer = models.BooleanField(default=False, db_column='is_vat_payer')  # Plátce DPH
    users = models.ManyToManyField(User, related_name='companies', db_column='users')  # Uživatelé propojení s firmou
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_company'

    def __str__(self):
        return self.name


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True, db_column='organization_id')
    name = models.CharField(max_length=200)
    ico = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_organizations')
    members = models.ManyToManyField(User, through='OrganizationMembership')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'FDK_organization'
    def __str__(self):
        return self.name

class OrganizationMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('member', 'Člen'), ('viewer', 'Pozorovatel')])
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FDK_organization_membership'

class Project(models.Model):
    project_id = models.AutoField(primary_key=True, db_column='project_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    url = models.CharField(max_length=255, null=True, blank=True, db_column='url')
    public = models.BooleanField(default=False, db_column='public')
    start_date = models.DateField(null=True, blank=True, db_column='start_date')
    end_date = models.DateField(null=True, blank=True, db_column='end_date')
    created = models.DateTimeField(null=True, blank=True, db_column='created')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_projects', db_column='owner_id')

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'FDK_projects'


class ProjectCategory(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='category_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='categories', db_column='project_id')
    language = models.CharField(max_length=2, null=True, blank=True, db_column='language')

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'FDK_categories'


class ProjectMilestone(models.Model):
    milestone_id = models.AutoField(primary_key=True, db_column='milestone_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones', db_column='project_id')
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(null=True, blank=True, db_column='description')
    due_date = models.DateField(null=True, blank=True, db_column='due_date')
    status = models.CharField(max_length=50, default='planned', db_column='status')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_milestones'



class ProjectRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.role_name
    class Meta:
        db_table = 'FDK_roles'


class ProjectPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.permission_name
    class Meta:
        db_table = 'FDK_permissions'



class ProjectUser(models.Model):
    project_user_id = models.AutoField(primary_key=True, db_column='project_user_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_projects')
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        db_table = 'FDK_project_user'
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"





class ProjectRolePermission(models.Model):
    role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(ProjectPermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')
        db_table = 'FDK_role_permisssions'



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
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, null=True, related_name='tasks', db_column='category_id')
    priority = models.CharField(max_length=16, null=True, blank=True, db_column='priority')
    status = models.CharField(max_length=50, null=True, blank=True, db_column='status')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', db_column='creator_id')
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', db_column='assigned_id')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='tasks', db_column='project_id')
    organization = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', db_column='organization_id')
    due_date = models.DateField(null=True, blank=True, db_column='due_date')
    created = models.DateTimeField(null=True, blank=True, db_column='created')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks', db_column='parent_id')

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
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='comments', db_column='project_id')
    comment = models.TextField(null=True, blank=True, db_column='comment')
    posted = models.DateTimeField(null=True, blank=True, db_column='posted')

    class Meta:
        db_table = 'FDK_comments'

class ProjectDocument(models.Model):
    document_id = models.AutoField(primary_key=True, db_column='document_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents', db_column='project_id')
    document_type = models.CharField(max_length=255, db_column='document_type')
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, db_column='category', null=True, blank=True)
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
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='lists', db_column='project_id')
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
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts', db_column='project_id')
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
    location = models.CharField(max_length=255, db_column='location')
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = 'FDK_warehouse'

class WarehouseItem(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='item_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    quantity = models.PositiveIntegerField(default=0, db_column='quantity')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items', db_column='warehouse_id')
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = 'FDK_warehouse_item'

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contracts', db_column='project_id')
    document = models.FileField(upload_to='contracts/', null=True, blank=True)

    class Meta:
        db_table = 'FDK_contract'
# # # # # # # # #


# -------------------------------------------------------------------
#                    TEST MANAGEMENT
# -------------------------------------------------------------------
class TestType(models.Model):
    test_type_id = models.AutoField(primary_key=True, db_column='test_type_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_types', db_column='project_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    class Meta:
        db_table = 'FDK_test_types'

    def __str__(self):
        return self.name


class Test(models.Model):
    test_id = models.AutoField(primary_key=True, db_column='test_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tests', db_column='project_id')
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_results', db_column='project_id') 
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
    test_result = models.ForeignKey(TestResult, db_column='test_result_id', on_delete=models.CASCADE, related_name='errors')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_errors', db_column='project_id') 
    error_title = models.CharField(max_length=255, db_column='error_title')
    description = models.TextField(null=True, blank=True, db_column='description')
    steps_to_replicate = models.TextField(null=True, blank=True, db_column='steps_to_replicate')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_errors')
    date_created = models.DateTimeField(auto_now_add=True, db_column='date_created')

    class Meta:
        db_table = 'FDK_test_errors'

    def __str__(self):
        return self.error_title




# # # F A K T U R Y # # #

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True, db_column='invoice_id')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoices', db_column='company_id')
    invoice_number = models.CharField(max_length=20, unique=True, db_column='invoice_number')
    issue_date = models.DateField(db_column='issue_date')
    due_date = models.DateField(db_column='due_date')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_price')
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='vat_amount')
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=21, db_column='vat_rate')  # Standardní sazba 21 %
    is_paid = models.BooleanField(default=False, db_column='is_paid')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

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

    class Meta:
        db_table = 'FDK_grant_call'

    def __str__(self):
        return self.title


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

    class Meta:
        db_table = 'FDK_grant_application'

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
#                    MODULE
# -------------------------------------------------------------------

"""
class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # 'warehouse', 'law_ai', 'project'
    display_name = models.CharField(max_length=200)
    description = models.TextField()
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
class UserModuleSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=20, choices=[
        ('free', 'Zdarma'),
        ('monthly', 'Měsíční'),
        ('yearly', 'Roční')
    ])
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('user', 'module')

class ModuleUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # 'ai_query', 'warehouse_transaction'
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(null=True, blank=True)
"""