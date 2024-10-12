### fdk_cz.models



from django.db import models
from django.contrib.auth.models import User 

from django.utils import timezone


class user(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=100, unique=True, db_column='username')
    password_hash = models.CharField(max_length=255, db_column='password_hash')
    email = models.EmailField(max_length=255, unique=True, db_column='email')
    description = models.CharField(max_length=512, null=True, blank=True, db_column='description')
    created = models.DateTimeField(null=True, blank=True, db_column='created')
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')


    class Meta:
        db_table = 'FDK_users'


class project(models.Model):
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


class category(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='category_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    project = models.ForeignKey(project, on_delete=models.SET_NULL, null=True, related_name='categories', db_column='project_id')
    language = models.CharField(max_length=2, null=True, blank=True, db_column='language')

    class Meta:
        db_table = 'FDK_categories'


class milestone(models.Model):
    milestone_id = models.AutoField(primary_key=True, db_column='milestone_id')
    project = models.ForeignKey(project, on_delete=models.CASCADE, related_name='milestones', db_column='project_id')
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(null=True, blank=True, db_column='description')
    due_date = models.DateField(null=True, blank=True, db_column='due_date')
    status = models.CharField(max_length=50, default='planned', db_column='status')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_milestones'


class project_user(models.Model):
    project_user_id = models.AutoField(primary_key=True, db_column='project_user_id')
    project = models.ForeignKey(project, on_delete=models.CASCADE, related_name='project_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_projects')
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"

    class Meta:
        db_table = 'FDK_project_user'



class role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.role_name
    class Meta:
        db_table = 'FDK_roles'


class permission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.permission_name
    class Meta:
        db_table = 'FDK_permissions'



class role_permission(models.Model):
    role = models.ForeignKey(role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')
        db_table = 'FDK_role_permisssions'



class task(models.Model):
    task_id = models.AutoField(primary_key=True, db_column='task_id')
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(null=True, blank=True, db_column='description')
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, related_name='tasks', db_column='category_id')
    priority = models.CharField(max_length=16, null=True, blank=True, db_column='priority')
    status = models.CharField(max_length=50, null=True, blank=True, db_column='status')
    creator = models.CharField(max_length=50, null=True, blank=True, db_column='creator')
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', db_column='assigned_id')
    project = models.ForeignKey(project, on_delete=models.SET_NULL, null=True, related_name='tasks', db_column='project_id')
    due_date = models.DateField(null=True, blank=True, db_column='due_date')
    created = models.DateTimeField(null=True, blank=True, db_column='created')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks', db_column='parent_id')

    class Meta:
        db_table = 'FDK_tasks'



class attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True, db_column='attachment_id')
    task = models.ForeignKey(task, on_delete=models.CASCADE, related_name='attachments', db_column='task_id')
    file_name = models.CharField(max_length=255, db_column='file_name')
    file_path = models.CharField(max_length=255, db_column='file_path')
    uploaded_by = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, related_name='uploaded_attachments', db_column='uploaded_by')
    uploaded_date = models.DateTimeField(null=True, blank=True, db_column='uploaded_date')

    class Meta:
        db_table = 'FDK_attachments'

class comment(models.Model):
    comment_id = models.AutoField(primary_key=True, db_column='comment_id')
    task = models.ForeignKey(task, on_delete=models.CASCADE, related_name='comments', db_column='task_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments', db_column='user_id')
    project = models.ForeignKey(project, on_delete=models.SET_NULL, null=True, related_name='comments', db_column='project_id')
    comment = models.TextField(null=True, blank=True, db_column='comment')
    posted = models.DateTimeField(null=True, blank=True, db_column='posted')

    class Meta:
        db_table = 'FDK_comments'

class activity_log(models.Model):
    log_id = models.AutoField(primary_key=True, db_column='log_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs', db_column='user_id')
    user_action = models.CharField(max_length=100, db_column='user_action')
    description = models.TextField(null=True, blank=True, db_column='description')
    date_time = models.DateTimeField(null=True, blank=True, db_column='date_time')

    class Meta:
        db_table = 'FDK_activity_log'

class document(models.Model):
    document_id = models.AutoField(primary_key=True, db_column='document_id')
    project = models.ForeignKey(project, on_delete=models.CASCADE, related_name='documents', db_column='project_id')
    document_type = models.CharField(max_length=255, db_column='document_type')
    title = models.CharField(max_length=255, db_column='title')
    url = models.CharField(max_length=255, db_column='url')
    description = models.TextField(null=True, blank=True, db_column='description')
    file_path = models.CharField(max_length=255, db_column='file_path')
    uploaded_by = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents', db_column='uploaded_by')
    uploaded_at = models.DateTimeField(auto_now_add=True, db_column='uploaded_at')

    class Meta:
        db_table = 'FDK_documents'

class flist(models.Model):
    list_id = models.AutoField(primary_key=True, db_column='list_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    project = models.ForeignKey(project, on_delete=models.SET_NULL, null=True, blank=True, related_name='lists', db_column='project_id')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_lists', db_column='owner_id')
    is_private = models.BooleanField(default=True, db_column='is_private')
    created = models.DateTimeField(default=timezone.now, db_column='created')  # Přidáme výchozí hodnotu
    modified = models.DateTimeField(auto_now=True, db_column='modified', null=True, blank=True)

    class Meta:
        db_table = 'FDK_lists'

class list_item(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='item_id')
    flist = models.ForeignKey(flist, on_delete=models.CASCADE, related_name='items', db_column='list_id')
    content = models.TextField(db_column='content')
    item_order = models.IntegerField(db_column='item_order')
    created = models.DateTimeField(default=timezone.now, db_column='created') 
    modified = models.DateTimeField(auto_now=True, db_column='modified')


    class Meta:
        db_table = 'FDK_list_items'


class list_permission(models.Model):
    list_permission_id = models.AutoField(primary_key=True, db_column='list_permission_id')
    flist = models.ForeignKey(flist, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_permissions')
    can_edit = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)

    class Meta:
        unique_together = ('flist', 'user')
    class Meta:
        db_table = 'FDK_list_permissions'








class contact(models.Model):
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
    project = models.ForeignKey(project, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts', db_column='project_id')
    account = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts', db_column='account_id')

    # Určení, zda je kontakt soukromý nebo sdílený s projektem
    is_private = models.BooleanField(default=True, db_column='is_private')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        db_table = 'FDK_contacts'


### MANAGEMENT SYSTEMS ###
# # # WAREHOUSE # # #
class warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True, db_column='warehouse_id')
    name = models.CharField(max_length=255, db_column='name')
    location = models.CharField(max_length=255, db_column='location')
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    class Meta:
        db_table = 'FDK_warehouse'

class item(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='item_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    quantity = models.PositiveIntegerField(default=0, db_column='quantity')
    warehouse = models.ForeignKey(warehouse, on_delete=models.CASCADE, related_name='items', db_column='warehouse_id')
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    class Meta:
        db_table = 'FDK_warehouse_item'

class transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, db_column='transaction_id')
    item = models.ForeignKey(item, on_delete=models.CASCADE, related_name='transactions', db_column='item_id')
    transaction_type = models.CharField(max_length=10, choices=[('IN', 'Příjem'), ('OUT', 'Výdej')], db_column='transaction_type')
    quantity = models.PositiveIntegerField(db_column='quantity')
    date = models.DateTimeField(auto_now_add=True, db_column='date')

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity})"
    class Meta:
        db_table = 'FDK_warehouse_transaction'


# # # # # # # # #
class contract(models.Model):
    contract_id = models.AutoField(primary_key=True, db_column='contract_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    start_date = models.DateField(null=True, blank=True, db_column='start_date')
    end_date = models.DateField(null=True, blank=True, db_column='end_date')
    project = models.ForeignKey(project, on_delete=models.CASCADE, related_name='contracts', db_column='project_id')
    document = models.FileField(upload_to='contracts/', null=True, blank=True)
    class Meta:
        db_table = 'FDK_contract'
# # # # # # # # #


### TEST MANAGEMENT ###

class test_type(models.Model):
    test_type_id = models.AutoField(primary_key=True, db_column='test_type_id')
    project = models.ForeignKey('project', on_delete=models.CASCADE, related_name='test_types', db_column='project_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    class Meta:
        db_table = 'FDK_test_types'

    def __str__(self):
        return self.name


class test(models.Model):
    test_id = models.AutoField(primary_key=True, db_column='test_id')
    project = models.ForeignKey('project', on_delete=models.CASCADE, related_name='tests', db_column='project_id')
    test_type = models.ForeignKey(test_type, on_delete=models.CASCADE, related_name='tests', db_column='test_type_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    grid_location = models.CharField(max_length=2, null=True, blank=True, db_column='grid_location')  # A1, B2, etc.
    date_created = models.DateTimeField(auto_now_add=True, db_column='date_created')

    class Meta:
        db_table = 'FDK_tests'

    def __str__(self):
        return self.name


class test_result(models.Model):
    test_result_id = models.AutoField(primary_key=True, db_column='test_result_id')
    project = models.ForeignKey('project', on_delete=models.CASCADE, related_name='test_results', db_column='project_id') 
    test = models.ForeignKey(test, on_delete=models.CASCADE, related_name='results', db_column='test_id')
    executed_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='executed_tests', db_column='executed_by')
    result = models.CharField(max_length=50, db_column='result')  # Pass, Fail, Blocked, etc.
    execution_date = models.DateTimeField(auto_now_add=True, db_column='execution_date')

    class Meta:
        db_table = 'FDK_test_results'

    def __str__(self):
        return f"{self.test.name} - {self.result}"


class test_error(models.Model):
    STATUS_CHOICES = [
        ('open', 'Otevřená'),
        ('closed', 'Uzavřená'),
        ('in_progress', 'V procesu'),
    ]
    test_error_id = models.AutoField(primary_key=True, db_column='test_error_id')
    test_result = models.ForeignKey(test_result, on_delete=models.CASCADE, related_name='errors', db_column='test_result_id')
    project = models.ForeignKey('project', on_delete=models.CASCADE, related_name='test_errors', db_column='project_id') 
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
class company(models.Model):
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


class invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True, db_column='invoice_id')
    company = models.ForeignKey(company, on_delete=models.CASCADE, related_name='invoices', db_column='company_id')
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




class invoice_item(models.Model):
    invoice_item_id = models.AutoField(primary_key=True, db_column='invoice_item_id')
    invoice = models.ForeignKey(invoice, on_delete=models.CASCADE, related_name='items', db_column='invoice_id')
    description = models.CharField(max_length=255, db_column='description')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, db_column='quantity')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='unit_price')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_price')
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=21, db_column='vat_rate')  

    class Meta:
        db_table = 'FDK_invoice_item'

    def __str__(self):
        return self.description








