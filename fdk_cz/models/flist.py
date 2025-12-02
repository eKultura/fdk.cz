# -------------------------------------------------------------------
#                    MODELS.FLIST
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Flist(models.Model):
    list_id = models.AutoField(primary_key=True, db_column='list_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='lists', db_column='project_id')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_lists', db_column='owner_id')
    is_private = models.BooleanField(default=True, db_column='is_private')
    created = models.DateTimeField(default=timezone.now, db_column='created')  # Přidáme výchozí hodnotu
    modified = models.DateTimeField(auto_now=True, db_column='modified', null=True, blank=True)

    class Meta:
        db_table = 'FDK_lists'


class ListItem(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='item_id')
    flist = models.ForeignKey(Flist, on_delete=models.CASCADE, related_name='items', db_column='list_id')
    content = models.TextField(db_column='content')
    item_order = models.IntegerField(db_column='item_order')
    created = models.DateTimeField(default=timezone.now, db_column='created') 
    modified = models.DateTimeField(auto_now=True, db_column='modified')

    class Meta:
        db_table = 'FDK_list_items'



class ListPermission(models.Model):
    list_permission_id = models.AutoField(primary_key=True, db_column='list_permission_id')
    flist = models.ForeignKey(Flist, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_permissions')
    can_edit = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)

    class Meta:
        db_table = 'FDK_list_permissions'
        unique_together = ('flist', 'user')


