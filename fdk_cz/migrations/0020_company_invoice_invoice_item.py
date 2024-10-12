# Generated by Django 5.1.1 on 2024-10-05 18:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0019_task_parent_alter_test_error_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('company_id', models.AutoField(db_column='company_id', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=255)),
                ('street', models.CharField(db_column='street', max_length=128)),
                ('street_number', models.CharField(db_column='street_number', max_length=10)),
                ('city', models.CharField(db_column='city', max_length=128)),
                ('postal_code', models.CharField(db_column='postal_code', max_length=20)),
                ('state', models.CharField(db_column='state', max_length=128)),
                ('ico', models.CharField(db_column='ico', max_length=20, unique=True)),
                ('dic', models.CharField(blank=True, db_column='dic', max_length=20, null=True)),
                ('phone', models.CharField(blank=True, db_column='phone', max_length=15, null=True)),
                ('email', models.EmailField(blank=True, db_column='email', max_length=254, null=True)),
                ('is_vat_payer', models.BooleanField(db_column='is_vat_payer', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('users', models.ManyToManyField(db_column='users', related_name='companies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'FDK_company',
            },
        ),
        migrations.CreateModel(
            name='invoice',
            fields=[
                ('invoice_id', models.AutoField(db_column='invoice_id', primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(db_column='invoice_number', max_length=20, unique=True)),
                ('issue_date', models.DateField(db_column='issue_date')),
                ('due_date', models.DateField(db_column='due_date')),
                ('total_price', models.DecimalField(db_column='total_price', decimal_places=2, max_digits=10)),
                ('vat_amount', models.DecimalField(db_column='vat_amount', decimal_places=2, max_digits=10)),
                ('vat_rate', models.DecimalField(db_column='vat_rate', decimal_places=2, default=21, max_digits=5)),
                ('is_paid', models.BooleanField(db_column='is_paid', default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('company', models.ForeignKey(db_column='company_id', on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='fdk_cz.company')),
            ],
            options={
                'db_table': 'FDK_invoice',
            },
        ),
        migrations.CreateModel(
            name='invoice_item',
            fields=[
                ('invoice_item_id', models.AutoField(db_column='invoice_item_id', primary_key=True, serialize=False)),
                ('description', models.CharField(db_column='description', max_length=255)),
                ('quantity', models.DecimalField(db_column='quantity', decimal_places=2, max_digits=10)),
                ('unit_price', models.DecimalField(db_column='unit_price', decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(db_column='total_price', decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(db_column='invoice_id', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='fdk_cz.invoice')),
            ],
            options={
                'db_table': 'FDK_invoice_item',
            },
        ),
    ]
