# -------------------------------------------------------------------
#                    MODELS.HELP
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class HelpArticle(models.Model):
    """Dokumentace a nápověda pro systém FDK.cz"""
    article_id = models.AutoField(primary_key=True, db_column='article_id')

    # Základní údaje
    title = models.CharField(max_length=255, db_column='title')
    slug = models.SlugField(max_length=255, unique=True, db_column='slug')
    content = models.TextField(db_column='content', help_text='Markdown formátovaný text')

    # Kategorizace
    CATEGORY_CHOICES = [
        ('intro', 'Obecný úvod'),
        ('module', 'Dokumentace modulu'),
        ('technical', 'Technická dokumentace'),
        ('faq', 'Často kladené otázky')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_column='category')

    # Propojení s modulem (volitelné)
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='help_articles', db_column='module_id',
                               help_text='Modul, ke kterému se článek vztahuje')

    # Řazení a viditelnost
    order = models.IntegerField(default=0, db_column='order', help_text='Pořadí zobrazení (nižší = dříve)')
    is_published = models.BooleanField(default=True, db_column='is_published')
    is_technical = models.BooleanField(default=False, db_column='is_technical',
                                      help_text='Viditelné pouze pro administrátory a testery')

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_help_articles', db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    # SEO a vyhledávání
    meta_description = models.CharField(max_length=255, null=True, blank=True, db_column='meta_description')
    keywords = models.CharField(max_length=500, null=True, blank=True, db_column='keywords',
                                help_text='Klíčová slova oddělená čárkami')

    class Meta:
        db_table = 'FDK_help_article'
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['category', 'is_published']),
            models.Index(fields=['module', 'is_published']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def get_absolute_url(self):
        return f"/napoveda/{self.slug}/"


