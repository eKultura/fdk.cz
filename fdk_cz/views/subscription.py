# fdk_cz/views/subscription.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from fdk_cz.models import Module, UserModuleSubscription, ModuleBundle


@login_required
def subscription_dashboard(request):
    """Dashboard předplatného - přehled aktivních modulů uživatele"""

    # Získat všechny aktivní subscriptions uživatele
    user_subscriptions = UserModuleSubscription.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('module').order_by('-created_at')

    # Moduly, které uživatel NEMÁ
    subscribed_module_ids = [sub.module_id for sub in user_subscriptions]
    available_modules = Module.objects.filter(
        is_active=True,
        is_free=False
    ).exclude(module_id__in=subscribed_module_ids).order_by('order')

    # Kontrola expirace - subscriptions končící do 7 dní
    expiring_soon = []
    for sub in user_subscriptions:
        days = sub.days_remaining()
        if days is not None and days <= 7:
            expiring_soon.append(sub)

    # Free moduly (pro info)
    free_modules = Module.objects.filter(is_free=True, is_active=True).order_by('order')

    context = {
        'active_subscriptions': user_subscriptions,
        'available_modules': available_modules,
        'expiring_soon': expiring_soon,
        'free_modules': free_modules,
    }

    return render(request, 'subscription/subscription_dashboard.html', context)


def subscription_pricing(request):
    """Stránka s cenami - veřejná pro všechny"""

    modules = Module.objects.filter(is_active=True).order_by('order')
    bundles = ModuleBundle.objects.filter(is_active=True).prefetch_related('modules').order_by('order')

    # Pokud je uživatel přihlášen, zjistit které moduly už má
    user_subscriptions = []
    if request.user.is_authenticated:
        user_subscriptions = UserModuleSubscription.objects.filter(
            user=request.user,
            is_active=True
        ).values_list('module_id', flat=True)

    context = {
        'modules': modules,
        'bundles': bundles,
        'user_subscriptions': list(user_subscriptions),
    }

    return render(request, 'subscription/subscription_pricing_page.html', context)


@login_required
def subscribe_to_module(request, module_id):
    """Zahájit nákup předplatného modulu"""

    module = get_object_or_404(Module, module_id=module_id, is_active=True)

    # Kontrola, zda už uživatel nemá aktivní subscription
    existing = UserModuleSubscription.objects.filter(
        user=request.user,
        module=module,
        is_active=True
    ).first()

    if existing:
        messages.info(request, f"Již máte aktivní předplatné modulu {module.display_name}.")
        return redirect('subscription_dashboard')

    if request.method == 'POST':
        subscription_type = request.POST.get('subscription_type')  # 'monthly' nebo 'yearly'

        # Vytvořit pending subscription
        if subscription_type == 'monthly':
            price = module.price_monthly
            end_date = timezone.now() + timedelta(days=30)
        elif subscription_type == 'yearly':
            price = module.price_yearly
            end_date = timezone.now() + timedelta(days=365)
        else:
            messages.error(request, "Neplatný typ předplatného.")
            return redirect('subscription_pricing')

        # Vytvořit subscription (zatím neaktivní - aktivujeme po platbě)
        subscription = UserModuleSubscription.objects.create(
            user=request.user,
            module=module,
            subscription_type=subscription_type,
            is_active=False,  # Aktivujeme po platbě
            end_date=end_date
        )

        # TODO: Přesměrovat na platební bránu
        # Pro teď rovnou aktivujeme (DEMO režim)
        subscription.is_active = True
        subscription.payment_method = 'demo'
        subscription.save()

        messages.success(request, f'Předplatné modulu "{module.display_name}" bylo aktivováno!')
        return redirect('subscription_dashboard')

    context = {
        'module': module
    }

    return render(request, 'subscription/subscribe_to_module.html', context)


@login_required
def cancel_subscription(request, subscription_id):
    """Zrušit předplatné"""

    subscription = get_object_or_404(
        UserModuleSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        cancellation_reason = request.POST.get('reason', '')

        subscription.is_active = False
        subscription.cancelled_at = timezone.now()
        subscription.cancellation_reason = cancellation_reason
        subscription.save()

        messages.success(request, f"Předplatné modulu {subscription.module.display_name} bylo zrušeno.")
        return redirect('subscription_dashboard')

    context = {
        'subscription': subscription
    }

    return render(request, 'subscription/cancel_subscription.html', context)


@login_required
def renew_subscription(request, subscription_id):
    """Obnovit předplatné"""

    subscription = get_object_or_404(
        UserModuleSubscription,
        subscription_id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        # Prodloužit end_date
        if subscription.subscription_type == 'monthly':
            new_end_date = timezone.now() + timedelta(days=30)
        elif subscription.subscription_type == 'yearly':
            new_end_date = timezone.now() + timedelta(days=365)
        else:
            new_end_date = timezone.now() + timedelta(days=30)

        subscription.end_date = new_end_date
        subscription.is_active = True
        subscription.save()

        # TODO: Vytvořit platbu

        messages.success(request, f"Předplatné modulu {subscription.module.display_name} bylo obnoveno!")
        return redirect('subscription_dashboard')

    context = {
        'subscription': subscription
    }

    return render(request, 'subscription/renew_subscription.html', context)
