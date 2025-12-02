# -------------------------------------------------------------------
#                    MODELS.USER
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """Rozšíření Django User modelu o další atributy"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_column='user_id')
    is_vip = models.BooleanField(default=False, db_column='is_vip', help_text='VIP uživatelé mají vyšší limity projektů')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_user_profile'
        verbose_name = 'Profil uživatele'
        verbose_name_plural = 'Profily uživatelů'

    def __str__(self):
        return f"Profil: {self.user.username}"

    def get_max_active_projects(self):
        """Vrátí max. počet aktivních projektů pro uživatele"""
        return 3 if self.is_vip else 1


class ActivityLog(models.Model):
    log_id = models.AutoField(primary_key=True, db_column='log_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs', db_column='user_id')
    user_action = models.CharField(max_length=100, db_column='user_action')
    description = models.TextField(null=True, blank=True, db_column='description')
    date_time = models.DateTimeField(null=True, blank=True, db_column='date_time')

    class Meta:
        db_table = 'FDK_activity_log'

class Users2(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=100, unique=True, db_column='username')
    password_hash = models.CharField(max_length=255, db_column='password_hash')
    email = models.EmailField(max_length=255, unique=True, db_column='email')
    description = models.CharField(max_length=512, null=True, blank=True, db_column='description')
    created = models.DateTimeField(null=True, blank=True, db_column='created')
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')

    class Meta:
        db_table = 'FDK_users'


