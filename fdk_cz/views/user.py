### views.user.py

#from django.shortcuts import render

# views.user.py

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from fdk_cz.forms.user import user_registration_form

from django.shortcuts import render, redirect




def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')  # redirect to dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required
def user_profile(request):
    return render(request, 'user/profile.html', {'user': request.user})

@login_required
def user_settings(request):
    return render(request, 'user/settings.html', {'user': request.user})


def registration(request):
    if request.method == 'POST':
        form = user_registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # automatické přihlášení po registraci
            return redirect('dashboard')  # Přesměrování po úspěšné registraci
    else:
        form = user_registration_form()
    return render(request, 'user/registration.html', {'form': form})






"""

def login(request):
    return render(request, 'user/login.html')

def logout(request):
    return render(request, 'user/logout.html')

def registration(request):
    return render(request, 'user/registration.html')

"""


