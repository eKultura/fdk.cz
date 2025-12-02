# -------------------------------------------------------------------
#                    MODELS.RISK
# -------------------------------------------------------------------
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Risk(models.Model):
    """Identifikované riziko"""
    risk_id = models.AutoField(primary_key=True, db_column='risk_id')

    # Základní údaje
    title = models.CharField(max_length=255, db_column='title')
    description = models.TextField(db_column='description')

    # Vztahy
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='risks', db_column='project_id')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='risks', db_column='organization_id')

    # Kategorizace
    CATEGORY_CHOICES = [
        ('technical', 'Technické'),
        ('financial', 'Finanční'),
        ('operational', 'Provozní'),
        ('strategic', 'Strategické'),
        ('legal', 'Právní'),
        ('security', 'Bezpečnostní'),
        ('other', 'Jiné')
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_column='category')

    # Hodnocení
    PROBABILITY_CHOICES = [
        (1, 'Velmi nízká'),
        (2, 'Nízká'),
        (3, 'Střední'),
        (4, 'Vysoká'),
        (5, 'Velmi vysoká')
    ]
    probability = models.IntegerField(choices=PROBABILITY_CHOICES, default=3, db_column='probability')

    IMPACT_CHOICES = [
        (1, 'Zanedbatelný'),
        (2, 'Malý'),
        (3, 'Střední'),
        (4, 'Velký'),
        (5, 'Kritický')
    ]
    impact = models.IntegerField(choices=IMPACT_CHOICES, default=3, db_column='impact')

    # Skóre rizika (probability * impact)
    risk_score = models.IntegerField(default=9, db_column='risk_score')

    # Opatření
    mitigation_strategy = models.TextField(null=True, blank=True, db_column='mitigation_strategy')
    contingency_plan = models.TextField(null=True, blank=True, db_column='contingency_plan')

    # Status
    STATUS_CHOICES = [
        ('identified', 'Identifikováno'),
        ('assessed', 'Vyhodnoceno'),
        ('mitigated', 'Zmírněno'),
        ('accepted', 'Akceptováno'),
        ('closed', 'Uzavřeno')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='identified', db_column='status')

    # Zodpovědnost
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='owned_risks', db_column='owner_id')

    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='created_risks', db_column='created_by_id')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'FDK_risk'
        ordering = ['-risk_score', '-created_at']

    def save(self, *args, **kwargs):
        # Auto-calculate risk score
        self.risk_score = self.probability * self.impact
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# -------------------------------------------------------------------
#                    IT MANAGEMENT
# -------------------------------------------------------------------

