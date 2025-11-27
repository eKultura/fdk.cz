# Data migration for OrganizationMembership role conversion

from django.db import migrations


def migrate_organization_roles(apps, schema_editor):
    """
    Migrate existing OrganizationMembership roles from CharField to ForeignKey.
    Maps old role values to new OrganizationRole objects.
    """
    OrganizationMembership = apps.get_model('fdk_cz', 'OrganizationMembership')
    OrganizationRole = apps.get_model('fdk_cz', 'OrganizationRole')

    # Mapping from old CharField values to new role names
    role_mapping = {
        'admin': 'organization_admin',
        'member': 'organization_member',
        'viewer': 'organization_viewer',
    }

    # Get or create roles if they don't exist (should be created by init_roles)
    for old_value, new_name in role_mapping.items():
        role, created = OrganizationRole.objects.get_or_create(
            role_name=new_name,
            defaults={'description': f'Migrated from {old_value}'}
        )

        # Update all memberships with this old role value
        memberships = OrganizationMembership.objects.filter(role_old=old_value)
        for membership in memberships:
            membership.role = role
            membership.save()

    # Handle any memberships that might have unexpected role values
    unmatched = OrganizationMembership.objects.filter(role__isnull=True)
    if unmatched.exists():
        # Default to organization_member for any unmatched roles
        default_role = OrganizationRole.objects.get(role_name='organization_member')
        for membership in unmatched:
            membership.role = default_role
            membership.save()


def reverse_migration(apps, schema_editor):
    """
    Reverse migration: copy role back to role_old
    """
    OrganizationMembership = apps.get_model('fdk_cz', 'OrganizationMembership')

    role_reverse_mapping = {
        'organization_admin': 'admin',
        'organization_member': 'member',
        'organization_viewer': 'viewer',
        'organization_owner': 'admin',  # Map owner back to admin
    }

    for membership in OrganizationMembership.objects.all():
        if membership.role:
            role_name = membership.role.role_name
            old_value = role_reverse_mapping.get(role_name, 'member')
            membership.role_old = old_value
            membership.save()


class Migration(migrations.Migration):
    """
    Data migration to convert OrganizationMembership.role from CharField to ForeignKey.
    This should be run AFTER init_roles command has been executed.
    """

    dependencies = [
        ('fdk_cz', '0017_comprehensive_roles_permissions'),
    ]

    operations = [
        migrations.RunPython(
            migrate_organization_roles,
            reverse_code=reverse_migration
        ),
    ]
