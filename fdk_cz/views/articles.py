# -------------------------------------------------------------------
#                    ARTICLES.PY
# -------------------------------------------------------------------

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from fdk_cz.models import Article
from fdk_cz.forms.articles import ArticleForm


# Přehled článků – BLOG
def article_blog_index(request):
    articles = Article.objects.filter(category='Blog', is_published=True).order_by('-created_at')
    return render(request, 'articles/blog_index.html', {'articles': articles})


# Nápověda / dokumentace
def article_help_index(request):
    articles = Article.objects.filter(category='Help', is_published=True).order_by('title')
    return render(request, 'articles/help_index.html', {'articles': articles})


# Stránky webu (např. O nás, GDPR, Kontakt)
def article_page_index(request):
    articles = Article.objects.filter(category='Page', is_published=True)
    return render(request, 'articles/page_index.html', {'articles': articles})


# Detail článku
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'articles/article_detail.html', {'article': article})


# Přidání článku
@login_required
def article_add(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Článek byl úspěšně vytvořen.")
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form, 'title': 'Nový článek'})


# Úprava článku
@login_required
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.user != article.author and not request.user.is_staff:
        messages.error(request, "Nemáte oprávnění upravovat tento článek.")
        return redirect('article_detail', slug=slug)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Článek byl aktualizován.")
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form, 'title': 'Upravit článek'})
