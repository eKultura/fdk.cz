# Generated manually on 2025-11-09 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0001_initial'),
    ]

    operations = [
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
