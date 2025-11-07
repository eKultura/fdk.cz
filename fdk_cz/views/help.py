# -------------------------------------------------------------------
#                    VIEWS.HELP.PY
# -------------------------------------------------------------------
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from fdk_cz.models import HelpArticle, Module


def is_superuser(user):
    """Check if user is superuser"""
    return user.is_superuser


def help_index(request):
    """Index page for help/documentation"""
    user = request.user

    # Get all published articles
    articles = HelpArticle.objects.filter(is_published=True)

    # Filter technical articles for non-staff users
    if not (user.is_authenticated and (user.is_superuser or user.is_staff)):
        articles = articles.filter(is_technical=False)

    # Organize articles by category
    intro_articles = articles.filter(category='intro').order_by('order', 'title')
    module_articles = articles.filter(category='module').select_related('module').order_by('order', 'title')
    technical_articles = articles.filter(category='technical').order_by('order', 'title')
    faq_articles = articles.filter(category='faq').order_by('order', 'title')

    # Group module articles by module
    modules_with_articles = {}
    for article in module_articles:
        if article.module:
            if article.module not in modules_with_articles:
                modules_with_articles[article.module] = []
            modules_with_articles[article.module].append(article)

    context = {
        'intro_articles': intro_articles,
        'modules_with_articles': modules_with_articles,
        'technical_articles': technical_articles,
        'faq_articles': faq_articles,
        'can_edit': user.is_authenticated and user.is_superuser,
    }

    return render(request, 'help/index.html', context)


def help_detail(request, slug):
    """Detail page for a help article"""
    user = request.user

    # Get article
    article = get_object_or_404(HelpArticle, slug=slug, is_published=True)

    # Check if user can view technical articles
    if article.is_technical and not (user.is_authenticated and (user.is_superuser or user.is_staff)):
        messages.error(request, "Nemáte oprávnění k zobrazení této technické dokumentace.")
        return redirect('help_index')

    # Split keywords into list
    keywords_list = []
    if article.keywords:
        keywords_list = [k.strip() for k in article.keywords.split(',') if k.strip()]

    context = {
        'article': article,
        'keywords_list': keywords_list,
        'can_edit': user.is_authenticated and user.is_superuser,
    }

    return render(request, 'help/detail.html', context)


@user_passes_test(is_superuser)
def help_add(request):
    """Add a new help article (superuser only)"""
    if request.method == 'POST':
        # Create new article
        article = HelpArticle()
        article.title = request.POST.get('title')
        article.slug = slugify(request.POST.get('slug') or request.POST.get('title'))
        article.content = request.POST.get('content')
        article.category = request.POST.get('category')
        article.order = int(request.POST.get('order', 0))
        article.is_published = request.POST.get('is_published') == 'on'
        article.is_technical = request.POST.get('is_technical') == 'on'
        article.meta_description = request.POST.get('meta_description', '')
        article.keywords = request.POST.get('keywords', '')
        article.created_by = request.user

        # Module (optional)
        module_id = request.POST.get('module')
        if module_id:
            article.module = Module.objects.get(module_id=module_id)

        article.save()

        messages.success(request, f"Článek '{article.title}' byl úspěšně vytvořen.")
        return redirect('help_detail', slug=article.slug)

    # GET - show form
    modules = Module.objects.filter(is_active=True).order_by('display_name')

    context = {
        'modules': modules,
        'categories': HelpArticle.CATEGORY_CHOICES,
    }

    return render(request, 'help/add.html', context)


@user_passes_test(is_superuser)
def help_edit(request, slug):
    """Edit a help article (superuser only)"""
    article = get_object_or_404(HelpArticle, slug=slug)

    if request.method == 'POST':
        # Update article
        article.title = request.POST.get('title')
        new_slug = slugify(request.POST.get('slug') or request.POST.get('title'))
        if new_slug != article.slug:
            # Check if new slug is unique
            if HelpArticle.objects.filter(slug=new_slug).exclude(article_id=article.article_id).exists():
                messages.error(request, "Tento slug již existuje. Zvolte jiný.")
            else:
                article.slug = new_slug

        article.content = request.POST.get('content')
        article.category = request.POST.get('category')
        article.order = int(request.POST.get('order', 0))
        article.is_published = request.POST.get('is_published') == 'on'
        article.is_technical = request.POST.get('is_technical') == 'on'
        article.meta_description = request.POST.get('meta_description', '')
        article.keywords = request.POST.get('keywords', '')

        # Module (optional)
        module_id = request.POST.get('module')
        if module_id:
            article.module = Module.objects.get(module_id=module_id)
        else:
            article.module = None

        article.save()

        messages.success(request, f"Článek '{article.title}' byl úspěšně upraven.")
        return redirect('help_detail', slug=article.slug)

    # GET - show form
    modules = Module.objects.filter(is_active=True).order_by('display_name')

    context = {
        'article': article,
        'modules': modules,
        'categories': HelpArticle.CATEGORY_CHOICES,
    }

    return render(request, 'help/edit.html', context)


@user_passes_test(is_superuser)
def help_delete(request, slug):
    """Delete a help article (superuser only)"""
    article = get_object_or_404(HelpArticle, slug=slug)

    if request.method == 'POST':
        article_title = article.title
        article.delete()
        messages.success(request, f"Článek '{article_title}' byl úspěšně smazán.")
        return redirect('help_index')

    context = {
        'article': article,
    }

    return render(request, 'help/delete.html', context)
