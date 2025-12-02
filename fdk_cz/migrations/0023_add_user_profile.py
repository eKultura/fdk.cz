# Add UserProfile model for VIP status and project limits

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Add UserProfile model:
    - OneToOne relationship with User
    - is_vip field for VIP status
    - get_max_active_projects() method in model
    """

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fdk_cz', '0022_finalize_organization_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_vip', models.BooleanField(default=False, db_column='is_vip', help_text='VIP uživatelé mají vyšší limity projektů')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='profile',
                    to=settings.AUTH_USER_MODEL,
                    db_column='user_id'
                )),
            ],
            options={
                'db_table': 'FDK_user_profile',
                'verbose_name': 'Profil uživatele',
                'verbose_name_plural': 'Profily uživatelů',
            },
        ),
    ]
