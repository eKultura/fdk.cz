"""
Module landing pages for anonymous users
Shows attractive landing pages with features, pricing, and CTAs
"""

from django.shortcuts import render


def project_management_landing(request):
    """Landing page for Project Management module"""
    return render(request, 'modules/project_management_landing.html')


def grants_landing(request):
    """Landing page for Grants & Subsidies module"""
    return render(request, 'modules/grants_landing.html')


def accounting_landing(request):
    """Landing page for Accounting module"""
    return render(request, 'modules/accounting_landing.html')


def law_ai_landing(request):
    """Landing page for AI Lawyer module"""
    return render(request, 'modules/law_ai_landing.html')
