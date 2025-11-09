# Generated manually on 2025-11-09 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0001_initial'),
    ]

    operations = [
        # First, drop the old foreign key constraint
        migrations.RunSQL(
            sql="""
                ALTER TABLE FDK_tasks
                DROP FOREIGN KEY FDK_tasks_organization_id_32c192f0_fk_FDK_company_company_id;
            """,
            reverse_sql="""
                ALTER TABLE FDK_tasks
                ADD CONSTRAINT FDK_tasks_organization_id_32c192f0_fk_FDK_company_company_id
                FOREIGN KEY (organization_id) REFERENCES FDK_company(company_id);
            """
        ),
        # Then alter the field to point to Organization
        migrations.AlterField(
            model_name='projecttask',
            name='organization',
            field=models.ForeignKey(
                blank=True,
                db_column='organization_id',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='tasks',
                to='fdk_cz.organization'
            ),
        ),
    ]
