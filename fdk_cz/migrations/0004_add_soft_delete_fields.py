# Generated migration for soft delete functionality

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0003_alter_testerror_test_result'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Add soft delete fields to TestError
        migrations.AddField(
            model_name='testerror',
            name='deleted',
            field=models.BooleanField(default=False, db_column='deleted'),
        ),
        migrations.AddField(
            model_name='testerror',
            name='deleted_at',
            field=models.DateTimeField(null=True, blank=True, db_column='deleted_at'),
        ),
        migrations.AddField(
            model_name='testerror',
            name='deleted_by',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='deleted_test_errors',
                to=settings.AUTH_USER_MODEL,
                db_column='deleted_by_id'
            ),
        ),

        # Add soft delete fields to ProjectTask
        migrations.AddField(
            model_name='projecttask',
            name='deleted',
            field=models.BooleanField(default=False, db_column='deleted'),
        ),
        migrations.AddField(
            model_name='projecttask',
            name='deleted_at',
            field=models.DateTimeField(null=True, blank=True, db_column='deleted_at'),
        ),
        migrations.AddField(
            model_name='projecttask',
            name='deleted_by',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='deleted_tasks',
                to=settings.AUTH_USER_MODEL,
                db_column='deleted_by_id'
            ),
        ),
    ]
