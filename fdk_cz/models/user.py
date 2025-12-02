# -------------------------------------------------------------------
#                    MODELS.USER
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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


