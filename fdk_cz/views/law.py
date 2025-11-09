# -------------------------------------------------------------------
#                    VIEWS.LAW.PY
# -------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from functools import wraps
import json


def law_module_required(view_func):
    """
    Decorator pro kontrolu přístupu k modulu AI Právo
    Přístup mají:
    - Superadmini
    - Uživatelé s aktivním předplatným modulu AI Právo
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Pro přístup k modulu AI Právo se musíte přihlásit.')
            return redirect('login_cs')

        # Superadmin má vždy přístup
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Kontrola aktivního předplatného modulu AI Právo
        from fdk_cz.models import UserModuleSubscription, Module
        try:
            law_module = Module.objects.get(name='ai_law')
            has_subscription = UserModuleSubscription.objects.filter(
                user=request.user,
                module=law_module,
                is_active=True
            ).exists()

            if has_subscription:
                return view_func(request, *args, **kwargs)
        except Module.DoesNotExist:
            pass

        # Uživatel nemá přístup
        messages.warning(request, 'Modul AI Právo je v testovacím režimu. Přístup mají pouze superadmini a uživatelé s aktivním předplatným.')
        return redirect('index')

    return wrapper


# Dummy models pro demonstraci - nahraďte skutečnými modely
class law_query(models.Model):
    """AI právní dotaz"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    question = models.TextField()
    ai_response = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Čeká na zpracování'),
        ('processing', 'Zpracovává se'),
        ('completed', 'Dokončeno'),
        ('failed', 'Chyba')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class law_detail(models.Model):
    """Zákon/Právní předpis"""
    title = models.CharField(max_length=300)
    number = models.CharField(max_length=50)  # číslo zákona
    year = models.IntegerField()
    content = models.TextField()
    category = models.CharField(max_length=100)
    effective_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class law_document(models.Model):
    """Právní dokument"""
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=50, choices=[
        ('contract', 'Smlouva'),
        ('agreement', 'Dohoda'),
        ('template', 'Šablona'),
        ('analysis', 'Analýza'),
        ('opinion', 'Stanovisko')
    ])
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


def law_dashboard(request):
    """Hlavní dashboard AI Práva"""
    context = {
        'page_title': 'AI Právo Dashboard',
        'testing_mode': True,  # Indikátor testovacího režimu
    }

    # Kontrola přístupu
    has_access = False
    if request.user.is_authenticated:
        if request.user.is_superuser:
            has_access = True
            context['access_reason'] = 'superadmin'
        else:
            # Kontrola předplatného
            from fdk_cz.models import UserModuleSubscription, Module
            try:
                law_module = Module.objects.get(name='ai_law')
                has_subscription = UserModuleSubscription.objects.filter(
                    user=request.user,
                    module=law_module,
                    is_active=True
                ).exists()
                if has_subscription:
                    has_access = True
                    context['access_reason'] = 'subscription'
            except Module.DoesNotExist:
                pass

    context['has_access'] = has_access

    if request.user.is_authenticated and has_access:
        # Statistiky pro přihlášené uživatele s přístupem
        context.update({
            'total_queries': 47,  # LawQuery.objects.filter(user=request.user).count()
            'pending_queries': 3,  # LawQuery.objects.filter(user=request.user, status='pending').count()
            'completed_queries': 44,  # LawQuery.objects.filter(user=request.user, status='completed').count()
            'total_documents': 12,  # LawDocument.objects.filter(user=request.user).count()

            # Nejnovější aktivity
            'recent_queries': [
                {'id': 1, 'title': 'Analýza kupní smlouvy', 'status': 'completed', 'created_at': timezone.now()},
                {'id': 2, 'title': 'Právní precedent - pracovní právo', 'status': 'processing', 'created_at': timezone.now()},
                {'id': 3, 'title': 'Generování žaloby', 'status': 'completed', 'created_at': timezone.now()},
            ],

            'recent_documents': [
                {'id': 1, 'title': 'Smlouva o dílo - IT služby', 'document_type': 'contract', 'created_at': timezone.now()},
                {'id': 2, 'title': 'Analýza obchodních podmínek', 'document_type': 'analysis', 'created_at': timezone.now()},
            ]
        })
    else:
        # Demo data pro nepřihlášené nebo bez přístupu
        context.update({
            'demo_mode': True,
            'total_queries': 15632,
            'pending_queries': 247,
            'completed_queries': 15385,
            'total_documents': 3456,
        })

    return render(request, 'law/dashboard.html', context)


@login_required
@law_module_required
def create_query(request):
    """Vytvoření nového AI dotazu"""
    if request.method == 'POST':
        title = request.POST.get('title')
        question = request.POST.get('question')
        query_type = request.POST.get('query_type', 'general')

        if title and question:
            # Zde by se vytvořil skutečný dotaz a poslal do AI
            # query = LawQuery.objects.create(
            #     user=request.user,
            #     title=title,
            #     question=question,
            #     status='pending'
            # )

            messages.success(request, f'Dotaz "{title}" byl úspěšně vytvořen a je zpracováván AI.')
            return redirect('law_query_detail', query_id=1)  # Dummy ID
        else:
            messages.error(request, 'Vyplňte prosím všechna povinná pole.')

    # Pre-fill law if law_id is provided
    selected_law = None
    law_id = request.GET.get('law_id')
    if law_id:
        try:
            from fdk_cz.models import Law
            selected_law = Law.objects.get(id=law_id)
        except (Law.DoesNotExist, ValueError, UnicodeDecodeError):
            # Ignore if law doesn't exist or has encoding issues
            pass

    context = {
        'page_title': 'Nový AI dotaz',
        'selected_law': selected_law,
        'query_types': [
            ('contract_analysis', 'Analýza smlouvy'),
            ('legal_research', 'Právní rešerše'),
            ('document_generation', 'Generování dokumentu'),
            ('precedent_search', 'Hledání precedentů'),
            ('legal_advice', 'Právní poradenství'),
            ('compliance_check', 'Kontrola souladu'),
        ]
    }

    return render(request, 'law/create_query.html', context)


@login_required
@law_module_required
def query_detail(request, query_id):
    """Detail AI dotazu"""
    try:
        # query = get_object_or_404(LawQuery, id=query_id, user=request.user)

        # Demo data - použití UTF-8 safe stringu
        ai_response_text = (
            "**Analýza kupní smlouvy dokončena**\n\n"
            "Identifikoval jsem následující rizikové klauzule:\n\n"
            "1. **Výhrada vlastnictví (čl. 4.2)** - Prodávající si vyhrazuje vlastnictví až do úplného zaplacení\n"
            "2. **Omezení záruky (čl. 7.1)** - Záruka pouze 6 měsíců, což je pod zákonným minimem\n"
            "3. **Jednostranné změny cen (čl. 3.4)** - Prodávající může změnit cenu bez souhlasu kupujícího\n\n"
            "**Doporučené úpravy:**\n"
            "- Prodloužit záruční dobu na 24 měsíců\n"
            "- Omezit možnosti změny ceny\n"
            "- Přidat sankce za prodlení s dodáním"
        )

        query_data = {
            'id': query_id,
            'title': 'Analýza kupní smlouvy - rizikové klauzule',
            'question': 'Prosím analyzujte přiloženou kupní smlouvu a identifikujte potenciální rizika pro kupujícího.',
            'status': 'completed',
            'ai_response': ai_response_text,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
        }

        context = {
            'page_title': 'Detail AI dotazu',
            'query': query_data,
        }

        return render(request, 'law/detail_query.html', context)
    except UnicodeDecodeError:
        from django.contrib import messages
        messages.error(request, 'Chyba při načítání dotazu. Data mohou obsahovat neplatné znaky.')
        from django.shortcuts import redirect
        return redirect('law_dashboard')


def law_list(request):
    """Seznam zákonů a právních předpisů"""
    # laws = Law.objects.all().order_by('-year', 'number')
    
    # Demo data
    laws_data = [
        {'id': 1, 'title': 'Občanský zákoník', 'number': '89/2012', 'year': 2012, 'category': 'Občanské právo'},
        {'id': 2, 'title': 'Zákoník práce', 'number': '262/2006', 'year': 2006, 'category': 'Pracovní právo'},
        {'id': 3, 'title': 'Obchodní zákoník', 'number': '513/1991', 'year': 1991, 'category': 'Obchodní právo'},
        {'id': 4, 'title': 'Trestní zákoník', 'number': '40/2009', 'year': 2009, 'category': 'Trestní právo'},
        {'id': 5, 'title': 'Správní řád', 'number': '500/2004', 'year': 2004, 'category': 'Správní právo'},
    ]
    
    # Filtrace podle kategorie
    category_filter = request.GET.get('category')
    if category_filter:
        laws_data = [law for law in laws_data if law['category'] == category_filter]
    
    context = {
        'page_title': 'Zákony a předpisy',
        'laws': laws_data,
        'categories': ['Občanské právo', 'Pracovní právo', 'Obchodní právo', 'Trestní právo', 'Správní právo'],
        'selected_category': category_filter,
    }
    
    return render(request, 'law/list_law.html', context)


def law_detail(request, law_id):
    """Detail zákona"""
    # law = get_object_or_404(Law, id=law_id)
    
    # Demo data
    law_data = {
        'id': law_id,
        'title': 'Občanský zákoník',
        'number': '89/2012 Sb.',
        'year': 2012,
        'category': 'Občanské právo',
        'effective_date': '2014-01-01',
        'summary': 'Zákon upravuje soukromoprávní vztahy fyzických a právnických osob.',
        'key_sections': [
            {'section': '§ 1', 'title': 'Základní zásady', 'content': 'Soukromé právo chrání důstojnost a svobodu člověka...'},
            {'section': '§ 489', 'title': 'Kupní smlouva', 'content': 'Kupní smlouvou se prodávající zavazuje...'},
            {'section': '§ 1914', 'title': 'Záruka za vady', 'content': 'Prodávající odpovídá kupującímu...'},
        ]
    }
    
    context = {
        'page_title': f'{law_data["title"]} - {law_data["number"]}',
        'law': law_data,
    }
    
    return render(request, 'law/detail_law.html', context)


@login_required
def contract_templates(request):
    """Šablony smluv"""
    templates_data = [
        {
            'id': 1, 
            'title': 'Kupní smlouva - nemovitost', 
            'category': 'Nemovitosti',
            'description': 'Standardní šablona pro koupi nemovitosti',
            'usage_count': 156
        },
        {
            'id': 2, 
            'title': 'Smlouva o dílo - IT služby', 
            'category': 'IT',
            'description': 'Šablona pro vývoj software a IT služby',
            'usage_count': 89
        },
        {
            'id': 3, 
            'title': 'Pracovní smlouva', 
            'category': 'Práce',
            'description': 'Základní šablona pracovní smlouvy',
            'usage_count': 234
        },
        {
            'id': 4, 
            'title': 'Smlouva o nájmu bytu', 
            'category': 'Nemovitosti',
            'description': 'Nájemní smlouva pro bytové prostory',
            'usage_count': 178
        },
    ]
    
    context = {
        'page_title': 'Šablony smluv',
        'templates': templates_data,
        'categories': ['Nemovitosti', 'IT', 'Práce', 'Obchod', 'Služby'],
    }
    
    return render(request, 'law/list_contract.html', context)


@login_required
def documents(request):
    """Uživatelské právní dokumenty"""
    # documents = LawDocument.objects.filter(user=request.user).order_by('-created_at')
    
    documents_data = [
        {
            'id': 1,
            'title': 'Analýza obchodních podmínek - E-shop XYZ',
            'document_type': 'analysis',
            'created_at': timezone.now(),
            'status': 'completed'
        },
        {
            'id': 2,
            'title': 'Smlouva o poskytování služeb',
            'document_type': 'contract',
            'created_at': timezone.now(),
            'status': 'draft'
        },
        {
            'id': 3,
            'title': 'Právní stanovisko - GDPR compliance',
            'document_type': 'opinion',
            'created_at': timezone.now(),
            'status': 'completed'
        },
    ]
    
    context = {
        'page_title': 'Moje dokumenty',
        'documents': documents_data,
        'document_types': [
            ('contract', 'Smlouva'),
            ('agreement', 'Dohoda'),
            ('analysis', 'Analýza'),
            ('opinion', 'Stanovisko'),
            ('template', 'Šablona'),
        ]
    }
    
    return render(request, 'law/list_document.html', context)


@login_required
def ai_assistant(request):
    """AI Asistent pro právní poradenství"""
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX požadavek pro chat
            user_message = request.POST.get('message')
            
            # Simulace AI odpovědi
            ai_responses = [
                "Podle českého práva máte v této situaci několik možností...",
                "Doporučuji konzultovat tuto záležitost s právníkem, nicméně obecně platí...",
                "Podle § 123 občanského zákoníku je možné...",
                "Tato problematika spadá pod úpravu zákona č. 89/2012 Sb...",
            ]
            
            import random
            ai_response = random.choice(ai_responses)
            
            return JsonResponse({
                'response': ai_response,
                'timestamp': timezone.now().isoformat()
            })
    
    context = {
        'page_title': 'AI Právní asistent',
        'chat_history': [
            {
                'type': 'user',
                'message': 'Mohu vypovědět smlouvu před uplynutím lhůty?',
                'timestamp': timezone.now()
            },
            {
                'type': 'ai',
                'message': 'Výpověď smlouvy před uplynutím lhůty je možná v několika případech podle občanského zákoníku...',
                'timestamp': timezone.now()
            }
        ]
    }
    
    return render(request, 'law/ai_assistant.html', context)



law_documents = documents
