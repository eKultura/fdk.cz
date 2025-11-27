# Final migration to clean up OrganizationMembership

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Finalize OrganizationMembership migration:
    - Make role field non-nullable
    - Remove old role_old field
    - Add unique_together constraint
    """

    dependencies = [
        ('fdk_cz', '0018_migrate_organization_membership_roles'),
    ]

    operations = [
        # Remove the old role_old field
        migrations.RemoveField(
            model_name='organizationmembership',
            name='role_old',
        ),

        # Alter role field to be non-nullable and add the proper constraint
        migrations.AlterField(
            model_name='organizationmembership',
            name='role',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='memberships',
                to='fdk_cz.organizationrole'
            ),
        ),

        # Add unique_together constraint (if not already present)
        migrations.AlterUniqueTogether(
            name='organizationmembership',
            unique_together={('user', 'organization')},
        ),
    ]
