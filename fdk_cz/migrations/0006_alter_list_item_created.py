# Generated by Django 5.1.1 on 2024-09-12 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0005_alter_list_item_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_item',
            name='created',
            field=models.DateTimeField(db_column='created'),
        ),
    ]
