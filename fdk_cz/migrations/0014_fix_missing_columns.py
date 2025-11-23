from django.db import migrations


class Migration(migrations.Migration):
    """
    Fix missing columns that were added to 0001_initial after it was applied.
    Uses raw SQL with column existence checks to be safe for any database state.
    """

    dependencies = [
        ('fdk_cz', '0013_add_soft_delete'),
    ]

    operations = [
        # Add missing SWOT columns to FDK_tasks
        migrations.RunSQL(
            sql="""
                ALTER TABLE FDK_tasks
                ADD COLUMN IF NOT EXISTS swot_type VARCHAR(20) NULL;
            """,
            reverse_sql="ALTER TABLE FDK_tasks DROP COLUMN IF EXISTS swot_type;",
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE FDK_tasks
                ADD COLUMN IF NOT EXISTS swot_impact INT NULL;
            """,
            reverse_sql="ALTER TABLE FDK_tasks DROP COLUMN IF EXISTS swot_impact;",
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE FDK_tasks
                ADD COLUMN IF NOT EXISTS swot_confidence INT NULL;
            """,
            reverse_sql="ALTER TABLE FDK_tasks DROP COLUMN IF EXISTS swot_confidence;",
        ),

        # Add missing Gantt columns to FDK_milestones
        migrations.RunSQL(
            sql="""
                ALTER TABLE FDK_milestones
                ADD COLUMN IF NOT EXISTS start_date DATE NULL;
            """,
            reverse_sql="ALTER TABLE FDK_milestones DROP COLUMN IF EXISTS start_date;",
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE FDK_milestones
                ADD COLUMN IF NOT EXISTS progress INT DEFAULT 0;
            """,
            reverse_sql="ALTER TABLE FDK_milestones DROP COLUMN IF EXISTS progress;",
        ),
    ]
