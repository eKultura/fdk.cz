### views.user.py

#from django.shortcuts import render

# views.user.py

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from fdk_cz.forms.user import user_registration_form, profile_edit_form, password_renewal_form,reset_password_form

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage

from .utils import encrypt_email, decrypt_email
from django_ratelimit.decorators import ratelimit

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  # přesměrování na index nebo dashboard
        else:
            messages.error(request, "Nesprávné uživatelské jméno nebo heslo.")  # Zobrazit chybovou zprávu
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})
    


def logout(request):
    auth_logout(request)
    return redirect('index')

def renewal(request):
    if request.method == 'POST':
        form = password_renewal_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            send_renewal_password(request,email)
            return redirect('login_cs')
    else:
        return render(request, 'user/renewal.html')

def renewal_hash(request,gen_hash):
    dehashed_email = decrypt_email(gen_hash)
    user = User.objects.get(email=dehashed_email)

    if request.method == 'POST':
        form = reset_password_form(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('login_cs')
    else:
        form = user_registration_form()
    return render(request, 'user/renewal_hash.html', {'form': form})

@ratelimit(key='ip', rate='1/m', block=True) 
def send_renewal_password(request,email):
    host = request.get_host()
    hashed_email = encrypt_email(email)
    full_url = f"http://{host}/password_renewal/{hashed_email}"
    email = EmailMessage(
        subject="Password Reset",
        body=f"Link for reseting password {full_url}",
        from_email="juraj.michalik@ekultura.eu",
        to=[email],
    )
    email.send()

@login_required
def user_profile(request):
    return render(request, 'user/profile.html', {'user': request.user})

@login_required
def user_settings(request):
    if request.method == 'POST':
        form = profile_edit_form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = profile_edit_form(instance=request.user)
    return render(request, 'user/settings.html', {'user': request.user, 'form': form})


def registration(request):
    if request.method == 'POST':
        form = user_registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # automatické přihlášení po registraci
            return redirect('index')  # Přesměrování po úspěšné registraci
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


