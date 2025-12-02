# -------------------------------------------------------------------
#                    MODELS.ORGANIZATION
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

# ============================================================================
# ORGANIZATION ROLES & PERMISSIONS
# ============================================================================


class OrganizationRole(models.Model):
    """Role v organizaci (např. owner, admin, member, viewer)"""
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True, help_text="Stručný popis role")

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'FDK_organization_roles'
        verbose_name = 'Organizační role'
        verbose_name_plural = 'Organizační role'



class OrganizationPermission(models.Model):
    """Oprávnění v rámci organizace"""
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.permission_name

    class Meta:
        db_table = 'FDK_organization_permissions'
        verbose_name = 'Organizační oprávnění'
        verbose_name_plural = 'Organizační oprávnění'



class OrganizationRolePermission(models.Model):
    """Vazba mezi organizační rolí a oprávněními"""
    role = models.ForeignKey(OrganizationRole, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(OrganizationPermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')
        db_table = 'FDK_organization_role_permissions'



class OrganizationMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.ForeignKey(OrganizationRole, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FDK_organization_membership'
        unique_together = ('user', 'organization')

