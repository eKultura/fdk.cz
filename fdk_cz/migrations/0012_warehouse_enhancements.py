from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0011_remove_projecttask_deleted_and_more'),
    ]

    operations = [
        # NOTE: project_id and organization_id columns already exist in database
        # Skipping AddField operations for these fields to avoid duplicate column error

        # Alter location field
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
