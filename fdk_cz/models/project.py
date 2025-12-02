# -------------------------------------------------------------------
#                    MODELS.PROJECT
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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



# ============================================================================
# PROJECT ROLES & PERMISSIONS
# ============================================================================


class ProjectRole(models.Model):
    """
    Role v projektu:
    - project_owner: vlastník projektu
    - project_admin: administrátor projektu
    - project_manager: projektový manažer
    - project_editor: editor projektu
    - project_contributor: přispěvatel
    - project_viewer: pozorovatel
    - project_stakeholder: stakeholder
    - project_controller: kontrolor
    """
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True, help_text="Stručný popis role")

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'FDK_roles'
        verbose_name = 'Projektová role'
        verbose_name_plural = 'Projektové role'



class ProjectPermission(models.Model):
    """Oprávnění v rámci projektu"""
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.permission_name

    class Meta:
        db_table = 'FDK_permissions'
        verbose_name = 'Projektové oprávnění'
        verbose_name_plural = 'Projektová oprávnění'




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


# ============================================================================
# MODULE ROLES & PERMISSIONS
# ============================================================================

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
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, null=True, related_name='tasks', db_column='category_id')
    priority = models.CharField(max_length=16, null=True, blank=True, db_column='priority')
    status = models.CharField(max_length=50, null=True, blank=True, db_column='status')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', db_column='creator_id')
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', db_column='assigned_id')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='tasks', db_column='project_id')
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

