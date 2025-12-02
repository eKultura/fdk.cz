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

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('Page', 'Webová stránka'),          # O nás, GDPR, Kontakt
        ('Help', 'Nápověda / Dokumentace'),  # Interní nebo uživatelská nápověda
        ('Announcement', 'Oznámení / Novinka'),  # Např. "Nová verze modulu", "Výpadek"
        ('Blog', 'Blogový příspěvek'),       # Dlouhodobé texty, inspirace
        ('Internal', 'Interní poznámka'),    # Jen pro interní uživatele (role admin/editor)
    ]

    title = models.CharField(max_length=255, db_column='title')
    slug = models.SlugField(max_length=255, unique=True, db_column='slug')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Page', db_column='category')
    
    content = models.TextField(db_column='content')
    summary = models.TextField(null=True, blank=True, db_column='summary', help_text="Krátký perex nebo popis")

    meta_header = models.TextField(blank=True, help_text="HTML kód do <head> (např. knihovny, meta tagy)", db_column='meta_header')
    meta_footer = models.TextField(blank=True, help_text="HTML/JS kód před </body>", db_column='meta_footer')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', db_column='author_id')
    is_published = models.BooleanField(default=True, db_column='is_published')
    is_featured = models.BooleanField(default=False, db_column='is_featured', help_text="Zobrazit v hlavních oznámeních nebo na dashboardu")

    created_at = models.DateTimeField(default=timezone.now, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = "FDK_articles"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.slug}"


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


