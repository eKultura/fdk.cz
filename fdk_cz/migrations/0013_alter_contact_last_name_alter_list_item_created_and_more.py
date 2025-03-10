# Generated by Django 5.1.1 on 2024-09-14 16:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0012_alter_project_user_project_alter_project_user_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, db_column='last_name', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='list_item',
            name='created',
            field=models.DateTimeField(db_column='created', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='list_item',
            name='modified',
            field=models.DateTimeField(auto_now=True, db_column='modified'),
        ),
    ]
