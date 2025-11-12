# Generated manually on 2025-11-12 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0002_alter_projecttask_organization'),
    ]

    operations = [
        # Make test_result field nullable in TestError model
        migrations.AlterField(
            model_name='testerror',
            name='test_result',
            field=models.ForeignKey(
                blank=True,
                db_column='test_result_id',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='errors',
                to='fdk_cz.testresult'
            ),
        ),
    ]
