from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from .models import Propiedad, Ingreso, Gasto


@login_required
def dashboard(request):
    propiedades = Propiedad.objects.all()

    # Obtener propiedad seleccionada
    propiedad_id = request.GET.get('propiedad')

    if propiedad_id:
        propiedad = Propiedad.objects.get(id=propiedad_id)
    else:
        propiedad = propiedades.first()

    # Balance general
    ingresos_total = Ingreso.objects.filter(propiedad=propiedad).aggregate(
        total=Sum('monto_bruto') - Sum('comision')
    )['total'] or 0

    gastos_total = Gasto.objects.filter(propiedad=propiedad).aggregate(
        total=Sum('monto')
    )['total'] or 0

    # Balance mensual
    ingresos_mensuales = (
        Ingreso.objects
        .filter(propiedad=propiedad)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=Sum('monto_bruto') - Sum('comision'))
        .order_by('mes')
    )

    gastos_mensuales = (
        Gasto.objects
        .filter(propiedad=propiedad)
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=Sum('monto'))
    )

    gastos_por_mes = {g['mes']: g['total'] for g in gastos_mensuales}

    balance_mensual = []
    for i in ingresos_mensuales:
        gastos_mes = gastos_por_mes.get(i['mes'], 0)
        balance_mensual.append({
            'mes': i['mes'],
            'ingresos': i['total'],
            'gastos': gastos_mes,
            'utilidad': i['total'] - gastos_mes
        })

    # Balance anual
    ingresos_anuales = (
        Ingreso.objects
        .filter(propiedad=propiedad)
        .annotate(anio=TruncYear('fecha'))
        .values('anio')
        .annotate(total=Sum('monto_bruto') - Sum('comision'))
        .order_by('anio')
    )

    gastos_anuales = (
        Gasto.objects
        .filter(propiedad=propiedad)
        .annotate(anio=TruncYear('fecha'))
        .values('anio')
        .annotate(total=Sum('monto'))
    )

    gastos_por_anio = {g['anio']: g['total'] for g in gastos_anuales}

    balance_anual = []
    for i in ingresos_anuales:
        gastos_anio = gastos_por_anio.get(i['anio'], 0)
        balance_anual.append({
            'anio': i['anio'].year,
            'ingresos': i['total'],
            'gastos': gastos_anio,
            'utilidad': i['total'] - gastos_anio
        })

    contexto = {
        'propiedades': propiedades,
        'propiedad_actual': propiedad.id if propiedad else None,
        'propiedad': propiedad,
        'ingresos': ingresos_total,
        'gastos': gastos_total,
        'utilidad': ingresos_total - gastos_total,
        'balance_mensual': balance_mensual,
        'balance_anual': balance_anual
    }

    return render(request, 'core/dashboard.html', contexto)
