# -------------------------------------------------------------------
#                    MODELS.COMPANY
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Company(models.Model):
    company_id = models.AutoField(primary_key=True, db_column='company_id')
    name = models.CharField(max_length=255, db_column='name')
    # struktura pro adresu
    street = models.CharField(max_length=128, db_column='street')  # Ulice
    street_number = models.CharField(max_length=10, db_column='street_number')  # Číslo ulice
    city = models.CharField(max_length=128, db_column='city')  # Město
    postal_code = models.CharField(max_length=20, db_column='postal_code')  # PSČ
    state = models.CharField(max_length=128, db_column='state')  # Stát
  
    ico = models.CharField(max_length=20, unique=True, db_column='ico')  # IČO
    dic = models.CharField(max_length=20, blank=True, null=True, db_column='dic')  # DIČ (volitelně)
    phone = models.CharField(max_length=15, blank=True, null=True, db_column='phone')
    email = models.EmailField(blank=True, null=True, db_column='email')
    is_vat_payer = models.BooleanField(default=False, db_column='is_vat_payer')  # Plátce DPH
    users = models.ManyToManyField(User, related_name='companies', db_column='users')  # Uživatelé propojení s firmou
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_company'

    def __str__(self):
        return self.name


