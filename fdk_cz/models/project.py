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
#                    SWOT ANALYSIS
# -------------------------------------------------------------------

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

