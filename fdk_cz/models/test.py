# -------------------------------------------------------------------
#                    MODELS.TEST
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

