# Generated manually for comprehensive roles and permissions system

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Comprehensive roles and permissions system:
    - Adds description fields to ProjectRole and ProjectPermission
    - Creates OrganizationRole, OrganizationPermission, OrganizationRolePermission
    - Migrates OrganizationMembership from CharField to ForeignKey for role
    - Creates ModuleRole, ModulePermission, ModuleRolePermission, ModuleAccess
    """

    dependencies = [
        ('fdk_cz', '0016_merge_20251123_1324'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ================================================================
        # 1. Add description fields to existing Project tables
        # ================================================================
        migrations.AddField(
            model_name='projectrole',
            name='description',
            field=models.TextField(blank=True, help_text='Stručný popis role', null=True),
        ),
        migrations.AddField(
            model_name='projectpermission',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),

        # ================================================================
        # 2. Create Organization Role tables
        # ================================================================
        migrations.CreateModel(
            name='OrganizationRole',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='Stručný popis role', null=True)),
            ],
            options={
                'db_table': 'FDK_organization_roles',
                'verbose_name': 'Organizační role',
                'verbose_name_plural': 'Organizační role',
            },
        ),
        migrations.CreateModel(
            name='OrganizationPermission',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, serialize=False)),
                ('permission_name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FDK_organization_permissions',
                'verbose_name': 'Organizační oprávnění',
                'verbose_name_plural': 'Organizační oprávnění',
            },
        ),
        migrations.CreateModel(
            name='OrganizationRolePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fdk_cz.organizationpermission')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='fdk_cz.organizationrole')),
            ],
            options={
                'db_table': 'FDK_organization_role_permissions',
                'unique_together': {('role', 'permission')},
            },
        ),

        # ================================================================
        # 3. Create Module Role tables
        # ================================================================
        migrations.CreateModel(
            name='ModuleRole',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='Stručný popis role', null=True)),
            ],
            options={
                'db_table': 'FDK_module_roles',
                'verbose_name': 'Modulová role',
                'verbose_name_plural': 'Modulové role',
            },
        ),
        migrations.CreateModel(
            name='ModulePermission',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, serialize=False)),
                ('permission_name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FDK_module_permissions',
                'verbose_name': 'Modulové oprávnění',
                'verbose_name_plural': 'Modulová oprávnění',
            },
        ),
        migrations.CreateModel(
            name='ModuleRolePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fdk_cz.modulepermission')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='fdk_cz.modulerole')),
            ],
            options={
                'db_table': 'FDK_module_role_permissions',
                'unique_together': {('role', 'permission')},
            },
        ),
        migrations.CreateModel(
            name='ModuleAccess',
            fields=[
                ('access_id', models.AutoField(primary_key=True, serialize=False)),
                ('module_name', models.CharField(
                    choices=[
                        ('warehouse', 'Sklad'),
                        ('contact', 'Kontakty'),
                        ('invoice', 'Faktury'),
                        ('task', 'Úkoly'),
                        ('document', 'Dokumenty'),
                        ('milestone', 'Milníky'),
                    ],
                    max_length=50
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='module_accesses',
                    to='fdk_cz.organization'
                )),
                ('project', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='module_accesses',
                    to='fdk_cz.project'
                )),
                ('role', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='accesses',
                    to='fdk_cz.modulerole'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='module_accesses',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'db_table': 'FDK_module_access',
                'verbose_name': 'Modulový přístup',
                'verbose_name_plural': 'Modulové přístupy',
                'unique_together': {('user', 'module_name', 'project', 'organization')},
            },
        ),

        # ================================================================
        # 4. Migrate OrganizationMembership.role from CharField to ForeignKey
        # ================================================================
        # This is a complex migration that requires:
        # 1. Create temporary default role
        # 2. Rename old role field
        # 3. Add new role field as ForeignKey
        # 4. Migrate data
        # 5. Remove old field

        # Step 1: Rename the old role field
        migrations.RenameField(
            model_name='organizationmembership',
            old_name='role',
            new_name='role_old',
        ),

        # Step 2: Add new role field as ForeignKey (nullable for now)
        migrations.AddField(
            model_name='organizationmembership',
            name='role',
            field=models.ForeignKey(
                null=True,  # Temporarily nullable
                on_delete=django.db.models.deletion.CASCADE,
                related_name='memberships',
                to='fdk_cz.organizationrole'
            ),
        ),

        # Step 3: Data migration will be handled separately or in production
        # The init_roles command should be run first to create the roles

        # Note: After running init_roles, you'll need to manually update existing memberships:
        # UPDATE FDK_organization_membership SET role_id = (
        #   SELECT role_id FROM FDK_organization_roles WHERE role_name = 'organization_' || role_old
        # );

        # Step 4: After data migration, make role non-nullable and remove role_old
        # This will be done in a follow-up migration after data is migrated
    ]
