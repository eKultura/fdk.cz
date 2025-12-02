# -------------------------------------------------------------------
#                    MODELS.LAW
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Law(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    title = models.CharField(max_length=300, db_column='title')
    number = models.CharField(max_length=50, db_column='number')
    year = models.IntegerField(db_column='year')
    content = models.TextField(db_column='content')
    category = models.CharField(max_length=100, db_column='category')
    effective_date = models.DateField(db_column='effective_date')
    created_at = models.DateTimeField(db_column='created_at')

    class Meta:
        db_table = 'FDK_law'

    def __str__(self):
        return f"{self.number}/{self.year} – {self.title}"


class LawDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FDK_law_document'



class LawQuery(models.Model):
    query_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    question = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FDK_law_query'

# -------------------------------------------------------------------
#                    SUBSCRIPTION SYSTEM
# -------------------------------------------------------------------

