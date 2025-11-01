# GRANTS MODULE ENHANCEMENT DESIGN
## Vylepšení modulu Granty a dotace pro FDK.cz

**Verze:** 1.0
**Datum:** 2025-11-01
**Status:** Design dokumentace

---

## 1. SOUČASNÝ STAV

### 1.1 Co funguje
✅ **GrantProgram** - Grantové programy s providery
✅ **GrantCall** - Výzvy/dotace s datumy, rozpočty, statusy
✅ **GrantApplication** - Žádosti uživatelů na výzvy
✅ **GrantRequirement** - Požadavky výzev
✅ **GrantApplicationDocument** - Dokumenty k žádostem
✅ **Grant calendar** - Kalendářní view výzev

### 1.2 Co chybí (požadavky uživatele)
❌ **Seznam aktivních dotačních příležitostí** - Dynamický dashboard s otevřenými výzvami
❌ **Průvodce generováním dokumentů** - Wizard pro poloautomatické vytváření dokumentů
❌ **Integrace s externími DB** - Napojení na dotaceEU, MŠMT + ruční přidání
❌ **Ověření jedinečnosti** - Kontrola duplicit v databázi
❌ **Kompletní životní cyklus** - Reporting, monitoring, ukončení

---

## 2. DATABÁZOVÉ ROZŠÍŘENÍ

### 2.1 Rozšíření GrantCall modelu

```python
class GrantCall(models.Model):
    # ... existující pole ...

    # ✅ NOVÉ: Zdroj dotace
    source = models.CharField(
        max_length=50,
        choices=[
            ('manual', 'Manuální'),
            ('dotaceeu', 'DotaceEU'),
            ('msmt', 'MŠMT'),
            ('other_api', 'Jiné API')
        ],
        default='manual',
        db_column='source'
    )

    # ✅ NOVÉ: Externí ID pro integraci
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_column='external_id',
        help_text='ID z externí databáze (dotaceEU, MŠMT)'
    )

    # ✅ NOVÉ: URL na původní zdroj
    source_url = models.URLField(
        null=True,
        blank=True,
        db_column='source_url',
        help_text='Odkaz na dotaci v původním systému'
    )

    # ✅ NOVÉ: Metadata z externího zdroje
    external_metadata = models.JSONField(
        default=dict,
        db_column='external_metadata',
        help_text='Dodatečná data z externího API'
    )

    # ✅ NOVÉ: Datum poslední synchronizace
    last_synced = models.DateTimeField(
        null=True,
        blank=True,
        db_column='last_synced'
    )

    # ✅ NOVÉ: Hashtag pro lepší vyhledávání
    tags = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column='tags',
        help_text='Tagy oddělené čárkami: startup,inovace,kultura'
    )

    # ✅ NOVÉ: Minimální/maximální částka
    min_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='min_amount'
    )
    max_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='max_amount'
    )

    # ✅ NOVÉ: Priorita pro zobrazení
    priority = models.IntegerField(
        default=0,
        db_column='priority',
        help_text='Vyšší číslo = vyšší priorita zobrazení'
    )

    class Meta:
        db_table = 'FDK_grant_call'
        indexes = [
            models.Index(fields=['external_id']),
            models.Index(fields=['source', 'is_active']),
            models.Index(fields=['-priority', '-published_at']),
            models.Index(fields=['status', 'end_date']),
        ]

    def is_open_for_applications(self):
        """Kontrola, zda je výzva otevřená"""
        today = timezone.now().date()
        if not self.is_active or self.status != 'open':
            return False
        if self.start_date and self.start_date > today:
            return False
        if self.end_date and self.end_date < today:
            return False
        return True

    def days_until_deadline(self):
        """Počet dní do uzávěrky"""
        if not self.end_date:
            return None
        delta = self.end_date - timezone.now().date()
        return delta.days if delta.days >= 0 else 0
```

### 2.2 Nový model: GrantOpportunityBookmark

```python
class GrantOpportunityBookmark(models.Model):
    """Uživatelé si mohou označit zajímavé příležitosti"""
    bookmark_id = models.AutoField(primary_key=True, db_column='bookmark_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grant_bookmarks', db_column='user_id')
    call = models.ForeignKey(GrantCall, on_delete=models.CASCADE, related_name='bookmarks', db_column='call_id')

    notes = models.TextField(null=True, blank=True, db_column='notes')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_grant_opportunity_bookmark'
        unique_together = ('user', 'call')

    def __str__(self):
        return f"{self.user.username} - {self.call.title}"
```

### 2.3 Nový model: GrantDocumentTemplate

```python
class GrantDocumentTemplate(models.Model):
    """Šablony dokumentů pro průvodce"""
    template_id = models.AutoField(primary_key=True, db_column='template_id')

    name = models.CharField(max_length=255, db_column='name')
    description = models.TextField(null=True, blank=True, db_column='description')

    document_type = models.CharField(
        max_length=100,
        choices=[
            ('project_description', 'Popis projektu'),
            ('budget', 'Rozpočet'),
            ('timeline', 'Časový harmonogram'),
            ('team', 'Složení týmu'),
            ('motivation', 'Motivační dopis'),
            ('references', 'Reference'),
            ('other', 'Jiné')
        ],
        db_column='document_type'
    )

    # JSON schéma pro dynamické pole formuláře
    fields_schema = models.JSONField(default=list, db_column='fields_schema')
    # Příklad: [{"name": "project_name", "type": "text", "label": "Název projektu", "required": true}, ...]

    # Markdown šablona s placeholdery
    template_content = models.TextField(db_column='template_content')
    # Příklad: "# {{project_name}}\n\nPopis: {{description}}"

    is_active = models.BooleanField(default=True, db_column='is_active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'FDK_grant_document_template'

    def __str__(self):
        return f"{self.name} ({self.document_type})"
```

### 2.4 Rozšíření GrantApplication

```python
class GrantApplication(models.Model):
    # ... existující pole ...

    # ✅ NOVÉ: Fáze životního cyklu
    lifecycle_stage = models.CharField(
        max_length=50,
        choices=[
            ('preparation', 'Příprava žádosti'),
            ('submitted', 'Odesláno'),
            ('under_review', 'Probíhá hodnocení'),
            ('approved', 'Schváleno'),
            ('rejected', 'Zamítnuto'),
            ('in_progress', 'V realizaci'),
            ('reporting', 'Reporting'),
            ('completed', 'Ukončeno'),
            ('archived', 'Archivováno')
        ],
        default='preparation',
        db_column='lifecycle_stage'
    )

    # ✅ NOVÉ: Reporting
    report_deadline = models.DateField(null=True, blank=True, db_column='report_deadline')
    last_report_submitted = models.DateTimeField(null=True, blank=True, db_column='last_report_submitted')

    # ✅ NOVÉ: Skutečně získaná částka (může se lišit od granted_amount)
    actual_received_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        db_column='actual_received_amount'
    )

    # ✅ NOVÉ: Průběh realizace v %
    completion_percentage = models.IntegerField(
        default=0,
        db_column='completion_percentage',
        help_text='0-100%'
    )
```

---

## 3. IMPLEMENTACE FUNKCI

### 3.1 Seznam aktivních dotačních příležitostí

#### 3.1.1 View: grant_opportunities_dashboard

```python
# fdk_cz/views/grants.py

@login_required
def grant_opportunities_dashboard(request):
    """
    Dashboard aktivních dotačních příležitostí
    - Otevřené výzvy seřazené podle priority a deadline
    - Filtry: provider, typ, tags
    - Bookmarked opportunities
    """
    today = timezone.now().date()

    # Aktivní výzvy (otevřené pro podání)
    open_calls = GrantCall.objects.filter(
        is_active=True,
        status='open',
        end_date__gte=today
    ).select_related('program').order_by('-priority', 'end_date')

    # Nadcházející výzvy
    upcoming_calls = GrantCall.objects.filter(
        is_active=True,
        status='upcoming',
        start_date__gte=today
    ).select_related('program').order_by('start_date')[:5]

    # Brzy končící (deadline < 14 dní)
    urgent_calls = open_calls.filter(end_date__lte=today + timedelta(days=14))

    # Filtry
    provider_filter = request.GET.get('provider')
    type_filter = request.GET.get('type')
    tag_filter = request.GET.get('tag')

    if provider_filter:
        open_calls = open_calls.filter(provider=provider_filter)
    if type_filter:
        open_calls = open_calls.filter(type=type_filter)
    if tag_filter:
        open_calls = open_calls.filter(tags__icontains=tag_filter)

    # Bookmarked opportunities
    bookmarked_ids = GrantOpportunityBookmark.objects.filter(
        user=request.user
    ).values_list('call_id', flat=True)

    context = {
        'open_calls': open_calls,
        'upcoming_calls': upcoming_calls,
        'urgent_calls': urgent_calls,
        'bookmarked_ids': list(bookmarked_ids),
        'today': today,
        'providers': GrantCall.objects.values_list('provider', flat=True).distinct(),
        'types': GrantCall._meta.get_field('type').choices,
    }

    return render(request, 'grants/opportunities_dashboard.html', context)
```

#### 3.1.2 View: bookmark_opportunity

```python
@login_required
def bookmark_opportunity(request, call_id):
    """Toggle bookmark for a grant opportunity"""
    call = get_object_or_404(GrantCall, call_id=call_id)

    bookmark, created = GrantOpportunityBookmark.objects.get_or_create(
        user=request.user,
        call=call
    )

    if not created:
        # Už existuje -> odebereme
        bookmark.delete()
        messages.success(request, f'Dotace "{call.title}" byla odebrána ze záložek.')
    else:
        messages.success(request, f'Dotace "{call.title}" byla přidána do záložek.')

    return redirect(request.META.get('HTTP_REFERER', 'grant_opportunities_dashboard'))
```

### 3.2 Průvodce generováním dokumentů

#### 3.2.1 View: document_wizard_start

```python
@login_required
def document_wizard_start(request, application_id):
    """
    Spustit průvodce generováním dokumentů
    """
    application = get_object_or_404(
        GrantApplication,
        application_id=application_id,
        applicant=request.user
    )

    # Dostupné šablony
    templates = GrantDocumentTemplate.objects.filter(is_active=True)

    context = {
        'application': application,
        'templates': templates
    }

    return render(request, 'grants/wizard/document_wizard_start.html', context)


@login_required
def document_wizard_generate(request, application_id, template_id):
    """
    Krok 2: Vyplnit formulář podle šablony
    """
    application = get_object_or_404(
        GrantApplication,
        application_id=application_id,
        applicant=request.user
    )
    template = get_object_or_404(GrantDocumentTemplate, template_id=template_id)

    if request.method == 'POST':
        # Získat data z formuláře
        form_data = {}
        for field in template.fields_schema:
            field_name = field['name']
            form_data[field_name] = request.POST.get(field_name, '')

        # Generovat dokument z šablony
        import re
        generated_content = template.template_content

        for key, value in form_data.items():
            generated_content = re.sub(
                r'\{\{' + key + r'\}\}',
                value,
                generated_content
            )

        # Uložit jako GrantApplicationDocument
        from fdk_cz.models import GrantApplicationDocument

        # Vytvořit dočasný soubor
        import io
        from django.core.files.base import ContentFile

        file_content = ContentFile(generated_content.encode('utf-8'))
        filename = f"{template.name}_{application.application_id}.md"

        doc = GrantApplicationDocument.objects.create(
            application=application,
            file=file_content
        )
        doc.file.save(filename, file_content)

        messages.success(request, f'Dokument "{template.name}" byl vygenerován.')
        return redirect('application_detail', application_id=application.application_id)

    context = {
        'application': application,
        'template': template,
        'fields': template.fields_schema
    }

    return render(request, 'grants/wizard/document_wizard_generate.html', context)
```

### 3.3 Integrace s externími databázemi dotací

#### 3.3.1 DotaceEU Integration

```python
# fdk_cz/integrations/dotaceeu.py

import requests
from django.conf import settings

class DotaceEUIntegration:
    """
    Integrace s API DotaceEU
    Pozn: DotaceEU nemá veřejné API, takže můžeme použít web scraping nebo RSS feed
    """

    BASE_URL = 'https://dotaceeu.cz/cs/evropske-fondy-v-cr'
    RSS_URL = 'https://dotaceeu.cz/rss'

    def fetch_opportunities(self, limit=50):
        """
        Stáhnout aktuální výzvy z DotaceEU
        """
        try:
            # Použití RSS feedu
            import feedparser
            feed = feedparser.parse(self.RSS_URL)

            opportunities = []
            for entry in feed.entries[:limit]:
                opportunity = {
                    'title': entry.title,
                    'description': entry.summary,
                    'url': entry.link,
                    'published': entry.published_parsed,
                    'provider': 'DotaceEU',
                    'external_id': entry.id or entry.link,
                }
                opportunities.append(opportunity)

            return opportunities
        except Exception as e:
            print(f"Chyba při stahování z DotaceEU: {e}")
            return []

    def import_to_database(self):
        """
        Importovat příležitosti do databáze
        """
        from fdk_cz.models import GrantCall, GrantProgram
        from datetime import datetime

        opportunities = self.fetch_opportunities()
        imported_count = 0

        for opp in opportunities:
            # Zkontrolovat duplicity podle external_id
            if GrantCall.objects.filter(external_id=opp['external_id']).exists():
                continue

            # Získat nebo vytvořit program
            program, _ = GrantProgram.objects.get_or_create(
                name='DotaceEU',
                defaults={
                    'provider': 'DotaceEU',
                    'description': 'Automaticky importované výzvy z DotaceEU',
                    'is_active': True
                }
            )

            # Vytvořit GrantCall
            call = GrantCall.objects.create(
                program=program,
                title=opp['title'],
                description=opp['description'],
                provider=opp['provider'],
                source='dotaceeu',
                external_id=opp['external_id'],
                source_url=opp['url'],
                status='open',
                is_active=True,
                last_synced=timezone.now()
            )

            imported_count += 1

        return imported_count
```

#### 3.3.2 Management Command: sync_external_grants

```python
# fdk_cz/management/commands/sync_external_grants.py

from django.core.management.base import BaseCommand
from fdk_cz.integrations.dotaceeu import DotaceEUIntegration

class Command(BaseCommand):
    help = 'Synchronizovat dotace z externích zdrojů'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='all',
            help='Zdroj: dotaceeu, msmt, all'
        )

    def handle(self, *args, **options):
        source = options['source']

        self.stdout.write(self.style.SUCCESS('🔄 Spouštím synchronizaci...'))

        if source in ['dotaceeu', 'all']:
            self.stdout.write('  📥 Stahuji z DotaceEU...')
            integration = DotaceEUIntegration()
            count = integration.import_to_database()
            self.stdout.write(self.style.SUCCESS(f'    ✅ Importováno: {count} výzev'))

        # Zde můžeme přidat další zdroje (MŠMT, ...)

        self.stdout.write(self.style.SUCCESS('✅ Synchronizace dokončena!'))
```

Spuštění cron job:
```bash
# Každý den v 6:00 ráno
0 6 * * * cd /path/to/fdk.cz && python manage.py sync_external_grants --source=all
```

### 3.4 Kontrola duplicit a jedinečnosti

#### 3.4.1 Utility funkce

```python
# fdk_cz/utils/grant_utils.py

from fdk_cz.models import GrantCall
from difflib import SequenceMatcher

def check_grant_duplicate(title, provider=None, external_id=None):
    """
    Zkontrolovat, zda dotace již existuje v databázi

    Returns:
        (is_duplicate, existing_call, similarity_score)
    """

    # 1. Kontrola podle external_id (nejpřesnější)
    if external_id:
        existing = GrantCall.objects.filter(external_id=external_id).first()
        if existing:
            return (True, existing, 1.0)

    # 2. Kontrola podle názvu a providera (přibližná)
    query = GrantCall.objects.all()
    if provider:
        query = query.filter(provider=provider)

    for call in query:
        similarity = SequenceMatcher(None, title.lower(), call.title.lower()).ratio()
        if similarity > 0.85:  # 85% shoda
            return (True, call, similarity)

    return (False, None, 0.0)


def get_duplicate_suggestions(title, provider=None, limit=5):
    """
    Vrátit potenciální duplicity
    """
    query = GrantCall.objects.all()
    if provider:
        query = query.filter(provider=provider)

    suggestions = []
    for call in query:
        similarity = SequenceMatcher(None, title.lower(), call.title.lower()).ratio()
        if similarity > 0.6:  # 60% shoda
            suggestions.append({
                'call': call,
                'similarity': similarity
            })

    # Seřadit podle similarity
    suggestions.sort(key=lambda x: x['similarity'], reverse=True)

    return suggestions[:limit]
```

#### 3.4.2 View s kontrolou duplicit

```python
@login_required
def grant_create_with_check(request, program_id=None):
    """
    Vytvoření nové výzvy s kontrolou duplicit
    """
    program = None
    if program_id:
        program = get_object_or_404(GrantProgram, pk=program_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        provider = request.POST.get('provider')

        # Kontrola duplicit
        from fdk_cz.utils.grant_utils import check_grant_duplicate, get_duplicate_suggestions

        is_duplicate, existing_call, similarity = check_grant_duplicate(
            title=title,
            provider=provider
        )

        if is_duplicate:
            suggestions = [{'call': existing_call, 'similarity': similarity}]
            messages.warning(
                request,
                f'Varování: Nalezena podobná dotace ({similarity*100:.0f}% shoda). '
                f'Zkontrolujte, zda se nejedná o duplicitu.'
            )

            context = {
                'program': program,
                'form_data': request.POST,
                'duplicate_suggestions': suggestions
            }
            return render(request, 'grants/grant_create_check_duplicates.html', context)

        # Pokračovat s vytvořením...
        description = request.POST.get('description')
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        budget = request.POST.get('budget') or None

        grant = GrantCall.objects.create(
            program=program,
            title=title,
            provider=provider,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            source='manual',
            status='open',
            is_active=True,
        )
        messages.success(request, f'Dotace "{grant.title}" byla vytvořena.')
        return redirect('grant_detail', grant_id=grant.call_id)

    return render(request, 'grants/grant_create.html', {'program': program})
```

---

## 4. TEMPLATES STRUKTURA

```
templates/grants/
├── opportunities_dashboard.html       # Dashboard aktivních příležitostí
├── opportunities_calendar.html        # Kalendářní view s deadlines
├── grant_detail_enhanced.html         # Rozšířený detail s lifecycle
├── wizard/
│   ├── document_wizard_start.html     # Krok 1: Výběr šablony
│   ├── document_wizard_generate.html  # Krok 2: Vyplnění formuláře
│   └── document_wizard_preview.html   # Krok 3: Náhled a stažení
├── application_lifecycle.html         # Tracking celého životního cyklu
└── grant_create_check_duplicates.html # Formulář s upozorněním na duplicity
```

---

## 5. URL ROUTING

```python
# fdk_cz/urls.py

urlpatterns = [
    # ... existující ...

    # Dashboard aktivních příležitostí
    path('granty/prilezitosti/', grants.grant_opportunities_dashboard, name='grant_opportunities_dashboard'),
    path('granty/prilezitost/<int:call_id>/bookmark/', grants.bookmark_opportunity, name='bookmark_opportunity'),

    # Průvodce dokumenty
    path('granty/zadost/<int:application_id>/pruvod ce/', grants.document_wizard_start, name='document_wizard_start'),
    path('granty/zadost/<int:application_id>/pruvodce/<int:template_id>/', grants.document_wizard_generate, name='document_wizard_generate'),

    # Kontrola duplicit
    path('granty/vytvorit-kontrola/', grants.grant_create_with_check, name='grant_create_with_check'),

    # Lifecycle tracking
    path('granty/zadost/<int:application_id>/lifecycle/', grants.application_lifecycle, name='application_lifecycle'),
]
```

---

## 6. IMPLEMENTAČNÍ FÁZE

### Fáze 1: Databázové rozšíření (0.5 dne)
- ✅ Rozšířit GrantCall model
- ✅ Vytvořit GrantOpportunityBookmark model
- ✅ Vytvořit GrantDocumentTemplate model
- ✅ Migrace

### Fáze 2: Dashboard příležitostí (1 den)
- ✅ View grant_opportunities_dashboard
- ✅ Template opportunities_dashboard.html
- ✅ Bookmark funkce

### Fáze 3: Průvodce dokumenty (1.5 dne)
- ✅ Vytvořit defaultní šablony
- ✅ View document_wizard (3 kroky)
- ✅ Templates pro wizard
- ✅ Generování dokumentů

### Fáze 4: Externí integrace (2 dny)
- ✅ DotaceEU integration class
- ✅ Management command sync_external_grants
- ✅ Testování importu

### Fáze 5: Kontrola duplicit (0.5 dne)
- ✅ Utility funkce check_grant_duplicate
- ✅ View s kontrolou
- ✅ Template s varováním

### Fáze 6: Lifecycle tracking (1 den)
- ✅ Rozšíření GrantApplication
- ✅ View application_lifecycle
- ✅ Template s timeline

**Celkový čas: 6.5 dne**

---

## 7. BEZPEČNOST & VALIDACE

1. **Duplicity**
   - Kontrola external_id (unique constraint)
   - Fuzzy matching pro titulky
   - Warning před vytvořením duplicity

2. **Extern í API**
   - Rate limiting
   - Caching responses (1 hodina)
   - Error handling

3. **Document wizard**
   - Sanitizace uživatelského inputu
   - Markdown preview (bez XSS)
   - Limity na velikost souboru

---

## 8. DALŠÍ ROZŠÍŘENÍ (budoucnost)

1. **AI asistent** - GPT pomoc s vyplňováním žádostí
2. **Auto-matching** - Doporučení dotací podle profilu organizace
3. **Email notifikace** - Upozornění na nové příležitosti a deadlines
4. **Reporting dashboards** - Statistiky úspěšnosti žádostí
5. **Export do PDF** - Generování PDF dokumentů
6. **Collaboration** - Týmová spolupráce na žádostech

---

## 9. ZÁVĚR

Tento design poskytuje kompletní vylepšení Grants modulu s:

- ✅ **Dashboard aktivních příležitostí** s bookmarks
- ✅ **Průvodce generováním dokumentů** (wizard)
- ✅ **Integrace s DotaceEU** (+ rozšiřitelné na MŠMT)
- ✅ **Kontrola duplicit** s fuzzy matching
- ✅ **Lifecycle tracking** pro celý proces dotace

**Další krok: Začít implementaci Fáze 1 - Databázové rozšíření**

---

**Konec dokumentu**
