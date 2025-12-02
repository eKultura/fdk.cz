# -------------------------------------------------------------------
#                    MODELS.HR
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

