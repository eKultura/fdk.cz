# Generated by Django 5.1.1 on 2024-09-16 15:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0015_test_error_date_created_test_error_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flist',
            name='created',
            field=models.DateTimeField(db_column='created', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='flist',
            name='modified',
            field=models.DateTimeField(auto_now=True, db_column='modified', null=True),
        ),
        migrations.AlterField(
            model_name='flist',
            name='project',
            field=models.ForeignKey(blank=True, db_column='project_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lists', to='fdk_cz.project'),
        ),
    ]
