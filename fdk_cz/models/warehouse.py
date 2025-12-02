# -------------------------------------------------------------------
#                    MODELS.WAREHOUSE
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True, db_column='warehouse_id')
    name = models.CharField(max_length=255, db_column='name')
    location = models.CharField(max_length=255, db_column='location', null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True, related_name='stores', db_column='project_id')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True, related_name='stores', db_column='organization_id')
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = 'FDK_warehouse'

    def __str__(self):
        return self.name


class WarehouseCategory(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='category_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    class Meta:
        db_table = 'FDK_warehouse_category'
        verbose_name_plural = 'Warehouse Categories'

    def __str__(self):
        return self.name


class WarehouseItem(models.Model):
    item_id = models.AutoField(primary_key=True, db_column='item_id')
    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')
    quantity = models.PositiveIntegerField(default=0, db_column='quantity')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items', db_column='warehouse_id')
    category = models.ForeignKey(WarehouseCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items', db_column='category_id')
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = 'FDK_warehouse_item'

    def __str__(self):
        return self.name


class WarehouseTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, db_column='transaction_id')
    item = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE, related_name='transactions', db_column='item_id')
    transaction_type = models.CharField(max_length=10, choices=[('IN', 'Příjem'), ('OUT', 'Výdej')], db_column='transaction_type')
    quantity = models.PositiveIntegerField(db_column='quantity')
    date = models.DateTimeField(auto_now_add=True, db_column='date')

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity})"
    class Meta:
        db_table = 'FDK_warehouse_transaction'

# kategorie - cena (historie)




# # # # # # # # #
