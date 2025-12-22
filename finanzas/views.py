from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

from .services import (
    balance_general,
    balance_mensual,
    balance_anual
)


@login_required
def dashboard(request):
    hoy = date.today()

    contexto = {
        'balance_general': balance_general(),
        'balance_mensual': balance_mensual(hoy.year, hoy.month),
        'balance_anual': balance_anual(hoy.year),
        'mes': hoy.month,
        'anio': hoy.year,
    }

    return render(request, 'finanzas/dashboard.html', contexto)
