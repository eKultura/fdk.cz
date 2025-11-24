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
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True, db_column='organization')

    # Rozpočet projektu (budget)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_column='budget', help_text="Celkový rozpočet projektu v Kč")
    budget_currency = models.CharField(max_length=3, default='CZK', db_column='budget_currency')

    def __str__(self):
        return self.name

    def get_spent_budget(self):
        """Vypočítá celkové čerpání rozpočtu z faktur projektu"""
        from django.db.models import Sum
        total = self.invoices.aggregate(total=Sum('total_price'))['total']
        return total or 0

    def get_remaining_budget(self):
        """Vypočítá zbývající rozpočet"""
        if self.budget is None:
            return None
        return self.budget - self.get_spent_budget()

    def get_budget_utilization_percent(self):
        """Vrátí procento čerpání rozpočtu"""
        if self.budget is None or self.budget == 0:
            return None
        return (self.get_spent_budget() / self.budget) * 100

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
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', db_column='organization_id')
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
    test_result = models.ForeignKey(TestResult, db_column='test_result_id', on_delete=models.CASCADE, related_name='errors', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_errors', db_column='project_id') 
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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoices', db_column='company_id', null=True, blank=True)  # Legacy - kept for backwards compatibility
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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
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

class Department(models.Model):
    """Oddělení v organizaci"""
    department_id = models.AutoField(primary_key=True, db_column='department_id')

    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    # Vztahy
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='departments', db_column='organization_id')
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='sub_departments', db_column='parent_department_id')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='managed_departments', db_column='manager_id')

    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_department'
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Zaměstnanci - může být propojený s účtem nebo bez účtu"""
    employee_id = models.AutoField(primary_key=True, db_column='employee_id')

    # Propojení s účtem (volitelné)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='employee_profile', db_column='user_id')

    # Základní údaje
    first_name = models.CharField(max_length=100, db_column='first_name')
    last_name = models.CharField(max_length=100, db_column='last_name')
    personal_id_number = models.CharField(max_length=20, null=True, blank=True, db_column='personal_id_number')  # rodné číslo

    # Kontaktní údaje
    email = models.EmailField(null=True, blank=True, db_column='email')
    phone = models.CharField(max_length=20, null=True, blank=True, db_column='phone')

    # Pracovní údaje
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='employees', db_column='organization_id')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='employees', db_column='department_id')
    position = models.CharField(max_length=255, null=True, blank=True, db_column='position')
    employee_number = models.CharField(max_length=50, null=True, blank=True, db_column='employee_number')

    # Pracovní poměr
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Plný úvazek'),
        ('part_time', 'Částečný úvazek'),
        ('contract', 'Smlouva'),
        ('temporary', 'Dočasný'),
        ('intern', 'Stážista')
    ]
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, db_column='employment_type')

    hire_date = models.DateField(null=True, blank=True, db_column='hire_date')
    termination_date = models.DateField(null=True, blank=True, db_column='termination_date')

    STATUS_CHOICES = [
        ('active', 'Aktivní'),
        ('on_leave', 'Na dovolené'),
        ('suspended', 'Pozastaveno'),
        ('terminated', 'Ukončeno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_column='status')

    # Mzda (pro propojení s účetnictvím)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='salary')
    currency = models.CharField(max_length=3, default='CZK', db_column='currency')

    # Metadata
    notes = models.TextField(null=True, blank=True, db_column='notes')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_employee'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


# -------------------------------------------------------------------
#                    RISK MANAGEMENT
# -------------------------------------------------------------------

class Risk(models.Model):
    """Identifikované riziko"""
    risk_id = models.AutoField(primary_key=True, db_column='risk_id')

    # Základní údaje
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(db_column='description')

    # Vztahy
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='risks', db_column='project_id')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='risks', db_column='organization_id')

    # Kategorizace
    CATEGORY_CHOICES = [
        ('technical', 'Technické'),
        ('financial', 'Finanční'),
        ('operational', 'Provozní'),
        ('strategic', 'Strategické'),
        ('legal', 'Právní'),
        ('security', 'Bezpečnostní'),
        ('other', 'Jiné')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_column='category')

    # Hodnocení
    PROBABILITY_CHOICES = [
        (1, 'Velmi nízká'),
        (2, 'Nízká'),
        (3, 'Střední'),
        (4, 'Vysoká'),
        (5, 'Velmi vysoká')
    ]
    probability = models.IntegerField(choices=PROBABILITY_CHOICES, default=3, db_column='probability')

    IMPACT_CHOICES = [
        (1, 'Zanedbatelný'),
        (2, 'Malý'),
        (3, 'Střední'),
        (4, 'Velký'),
        (5, 'Kritický')
    ]
    impact = models.IntegerField(choices=IMPACT_CHOICES, default=3, db_column='impact')

    # Skóre rizika (probability * impact)
    risk_score = models.IntegerField(default=9, db_column='risk_score')

    # Opatření
    mitigation_strategy = models.TextField(null=True, blank=True, db_column='mitigation_strategy')
    contingency_plan = models.TextField(null=True, blank=True, db_column='contingency_plan')

    # Status
    STATUS_CHOICES = [
        ('identified', 'Identifikováno'),
        ('assessed', 'Vyhodnoceno'),
        ('mitigated', 'Zmírněno'),
        ('accepted', 'Akceptováno'),
        ('closed', 'Uzavřeno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='identified', db_column='status')

    # Zodpovědnost
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='owned_risks', db_column='owner_id')

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_risks', db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_risk'
        ordering = ['-risk_score', '-created_at']

    def save(self, *args, **kwargs):
        # Auto-calculate risk score
        self.risk_score = self.probability * self.impact
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# -------------------------------------------------------------------
#                    IT MANAGEMENT
# -------------------------------------------------------------------

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

class HelpArticle(models.Model):
    """Dokumentace a nápověda pro systém FDK.cz"""
    article_id = models.AutoField(primary_key=True, db_column='article_id')

    # Základní údaje
    title = models.CharField(max_length=255, db_column='title')
    slug = models.SlugField(max_length=255, unique=True, db_column='slug')
    content = models.TextField(db_column='content', help_text='Markdown formátovaný text')

    # Kategorizace
    CATEGORY_CHOICES = [
        ('intro', 'Obecný úvod'),
        ('module', 'Dokumentace modulu'),
        ('technical', 'Technická dokumentace'),
        ('faq', 'Často kladené otázky')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_column='category')

    # Propojení s modulem (volitelné)
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='help_articles', db_column='module_id',
                               help_text='Modul, ke kterému se článek vztahuje')

    # Řazení a viditelnost
    order = models.IntegerField(default=0, db_column='order', help_text='Pořadí zobrazení (nižší = dříve)')
    is_published = models.BooleanField(default=True, db_column='is_published')
    is_technical = models.BooleanField(default=False, db_column='is_technical',
                                      help_text='Viditelné pouze pro administrátory a testery')

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_help_articles', db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    # SEO a vyhledávání
    meta_description = models.CharField(max_length=255, null=True, blank=True, db_column='meta_description')
    keywords = models.CharField(max_length=500, null=True, blank=True, db_column='keywords',
                                help_text='Klíčová slova oddělená čárkami')

    class Meta:
        db_table = 'FDK_help_article'
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['category', 'is_published']),
            models.Index(fields=['module', 'is_published']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def get_absolute_url(self):
        return f"/napoveda/{self.slug}/"


class SwotAnalysis(models.Model):
    """
    SWOT analýza - může existovat na úrovni organizace, projektu nebo uživatele.
    Každý položka má váhu 1-10 pro vizuální umístění v kvadrantu.
    """
    swot_id = models.AutoField(primary_key=True, db_column='swot_id')
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(null=True, blank=True, db_column='description')

    # Triple context (organization/project/personal)
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='swot_analyses',
        db_column='organization_id'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='swot_analyses',
        db_column='project_id'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='personal_swot_analyses',
        db_column='owner_id'
    )

    # SWOT quadrants - each is a list of {"text": "...", "weight": 1-10}
    strengths = models.JSONField(
        default=list,
        db_column='strengths',
        help_text='Silné stránky - [{"text": "...", "weight": 1-10}, ...]'
    )
    weaknesses = models.JSONField(
        default=list,
        db_column='weaknesses',
        help_text='Slabé stránky - [{"text": "...", "weight": 1-10}, ...]'
    )
    opportunities = models.JSONField(
        default=list,
        db_column='opportunities',
        help_text='Příležitosti - [{"text": "...", "weight": 1-10}, ...]'
    )
    threats = models.JSONField(
        default=list,
        db_column='threats',
        help_text='Hrozby - [{"text": "...", "weight": 1-10}, ...]'
    )

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_swot_analyses',
        db_column='created_by_id'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_swot_analysis'
        ordering = ['-updated_at']
        verbose_name = 'SWOT analýza'
        verbose_name_plural = 'SWOT analýzy'

    def __str__(self):
        return self.title

    def get_total_items(self):
        return len(self.strengths) + len(self.weaknesses) + len(self.opportunities) + len(self.threats)
