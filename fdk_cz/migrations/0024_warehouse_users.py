# Generated by Django 5.1.2 on 2024-11-22 22:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0023_task_organization_alter_task_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='warehouses', to=settings.AUTH_USER_MODEL),
        ),
    ]