# -------------------------------------------------------------------
#                    VIEWS.FLIST.PY
# -------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from fdk_cz.forms.flist import list_form, list_item_form
from fdk_cz.models import Flist, ListItem, Project

import logging

# -------------------------------------------------------------------
#                    POZNÁMKY A TODO
# -------------------------------------------------------------------
# a
# b
# c
# -------------------------------------------------------------------



@login_required
def index_list(request):
    try:
        # Načteme uživatele explicitně podle jeho primárního klíče
        current_user = User.objects.get(pk=request.user.pk)
        lists = flist.objects.filter(owner=current_user)
    except User.DoesNotExist:
        lists = []
    
    return render(request, 'list/index_list.html', {'lists': lists})



@login_required
def create_list(request):
    if request.method == 'POST':
        form = list_form(request.POST, user=request.user)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.owner = request.user
            if not new_list.created:  # Pokud není nastaveno datum vytvoření
                new_list.created = timezone.now()
            new_list.save()
            return redirect('index_list')
    else:
        form = list_form(user=request.user)
    
    return render(request, 'list/create_list.html', {'form': form})




@login_required
def edit_list(request, list_id):
    flist_instance = get_object_or_404(flist, pk=list_id)

    if flist_instance.owner != request.user:
        return redirect('detail_list', list_id=list_id)

    if request.method == 'POST':
        form = list_form(request.POST, instance=flist_instance, user=request.user)
        if form.is_valid():
            form.save()  # Zde se nyní správně uloží projekt, pokud je vyplněn
            return redirect('detail_list', list_id=list_id)
    else:
        form = list_form(instance=flist_instance, user=request.user)

    return render(request, 'list/edit_list.html', {'form': form, 'list_id': list_id})





@login_required
def detail_list(request, list_id):
    flist_instance = get_object_or_404(flist, pk=list_id)
    items = flist_instance.items.all()

    if request.method == 'POST':
        item_form = list_item_form(request.POST)
        if item_form.is_valid():
            new_item = item_form.save(commit=False)
            new_item.flist = flist_instance
            new_item.created = timezone.now()  # Použití timezone pro nastavení data vytvoření
            new_item.save()
            return redirect('detail_list', list_id=new_item.flist.list_id)
    else:
        item_form = list_item_form()

    return render(request, 'list/detail_list.html', {'list': flist_instance, 'items': items, 'item_form': item_form})





@login_required
def add_item(request, list_id):
    flist_instance = get_object_or_404(flist, pk=list_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            flist_instance.items.create(content=content, created=timezone.now(), modified=timezone.now())
            return redirect('detail_list', list_id=list_id)

    return render(request, 'list/add_item.html', {'flist': flist_instance})



def edit_item(request, item_id):
    item = get_object_or_404(list_item, pk=item_id)
    if request.method == 'POST':
        form = list_item_form(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('detail_list', args=[item.flist.list_id]))
    else:
        form = list_item_form(instance=item)
    return render(request, 'list/edit_item.html', {'form': form, 'item': item})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(list_item, pk=item_id)
    flist_id = item.flist.list_id
    item.delete()
    return redirect('detail_list', list_id=flist_id)



