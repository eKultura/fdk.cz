# Generated by Django 5.1.1 on 2024-09-13 09:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0007_alter_flist_modified'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='item',
            fields=[
                ('item_id', models.AutoField(db_column='item_id', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=255)),
                ('description', models.TextField(blank=True, db_column='description', null=True)),
                ('quantity', models.PositiveIntegerField(db_column='quantity', default=0)),
                ('created', models.DateTimeField(auto_now_add=True, db_column='created')),
            ],
        ),
        migrations.CreateModel(
            name='warehouse',
            fields=[
                ('warehouse_id', models.AutoField(db_column='warehouse_id', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=255)),
                ('location', models.CharField(db_column='location', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, db_column='created')),
            ],
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('contact_id', models.AutoField(db_column='contact_id', primary_key=True, serialize=False)),
                ('first_name', models.CharField(db_column='first_name', max_length=100)),
                ('last_name', models.CharField(db_column='last_name', max_length=100)),
                ('phone', models.CharField(blank=True, db_column='phone', max_length=20, null=True)),
                ('email', models.EmailField(blank=True, db_column='email', max_length=255, null=True)),
                ('company', models.CharField(blank=True, db_column='company', max_length=255, null=True)),
                ('description', models.TextField(blank=True, db_column='description', null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, db_column='added_on')),
                ('last_contacted', models.DateTimeField(blank=True, db_column='last_contacted', null=True)),
                ('is_private', models.BooleanField(db_column='is_private', default=True)),
                ('account', models.ForeignKey(blank=True, db_column='account_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_column='project_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts', to='fdk_cz.project')),
            ],
            options={
                'db_table': 'FDK_contacts',
            },
        ),
        migrations.CreateModel(
            name='contract',
            fields=[
                ('contract_id', models.AutoField(db_column='contract_id', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=255)),
                ('description', models.TextField(blank=True, db_column='description', null=True)),
                ('start_date', models.DateField(blank=True, db_column='start_date', null=True)),
                ('end_date', models.DateField(blank=True, db_column='end_date', null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='contracts/')),
                ('project', models.ForeignKey(db_column='project_id', on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='fdk_cz.project')),
            ],
        ),
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('transaction_id', models.AutoField(db_column='transaction_id', primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('IN', 'Příjem'), ('OUT', 'Výdej')], db_column='transaction_type', max_length=10)),
                ('quantity', models.PositiveIntegerField(db_column='quantity')),
                ('date', models.DateTimeField(auto_now_add=True, db_column='date')),
                ('item', models.ForeignKey(db_column='item_id', on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='fdk_cz.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='warehouse',
            field=models.ForeignKey(db_column='warehouse_id', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='fdk_cz.warehouse'),
        ),
    ]
