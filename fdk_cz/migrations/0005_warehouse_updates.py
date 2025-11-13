# Generated migration for warehouse enhancements

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0004_add_soft_delete_fields'),
    ]

    operations = [
        # Add project and organization fields to Warehouse
        migrations.AddField(
            model_name='warehouse',
            name='project',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='stores',
                to='fdk_cz.project',
                db_column='project_id'
            ),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='organization',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='stores',
                to='fdk_cz.organization',
                db_column='organization_id'
            ),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='location',
            field=models.CharField(max_length=255, db_column='location', null=True, blank=True),
        ),

        # Create WarehouseCategory model
        migrations.CreateModel(
            name='WarehouseCategory',
            fields=[
                ('category_id', models.AutoField(primary_key=True, db_column='category_id')),
                ('name', models.CharField(max_length=255, db_column='name')),
                ('description', models.TextField(null=True, blank=True, db_column='description')),
            ],
            options={
                'db_table': 'FDK_warehouse_category',
                'verbose_name_plural': 'Warehouse Categories',
            },
        ),

        # Add category field to WarehouseItem
        migrations.AddField(
            model_name='warehouseitem',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='items',
                to='fdk_cz.warehousecategory',
                db_column='category_id'
            ),
        ),
    ]
