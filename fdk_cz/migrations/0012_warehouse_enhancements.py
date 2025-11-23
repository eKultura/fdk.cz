from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fdk_cz', '0003_alter_testerror_test_result'),
    ]

    operations = [
        # NOTE: All operations already applied to database in previous migration attempt
        # Database already contains:
        # - FDK_warehouse_category table
        # - category_id column in FDK_warehouse_item
        # - project_id and organization_id in FDK_warehouse
        # Emptying operations to prevent duplicate table/column errors
    ]
