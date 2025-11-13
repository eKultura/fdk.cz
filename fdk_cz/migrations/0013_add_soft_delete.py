from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0012_warehouse_enhancements'),
    ]

    operations = [
        # Add deleted field to TestError
        migrations.AddField(
            model_name='testerror',
            name='deleted',
            field=models.BooleanField(default=False, db_column='deleted'),
        ),

        # Add deleted field to ProjectTask
        migrations.AddField(
            model_name='projecttask',
            name='deleted',
            field=models.BooleanField(default=False, db_column='deleted'),
        ),
    ]
