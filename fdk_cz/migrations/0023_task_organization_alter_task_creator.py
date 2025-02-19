# Generated by Django 5.1.2 on 2024-11-17 19:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0022_document_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='organization',
            field=models.ForeignKey(blank=True, db_column='organization_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='fdk_cz.company'),
        ),
        migrations.AlterField(
            model_name='task',
            name='creator',
            field=models.ForeignKey(db_column='creator_id', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_tasks', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
