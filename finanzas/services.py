from django.db.models import Sum
from datetime import date
from .models import Ingreso, Gasto


def balance_general(propiedad=None):
    ingresos = Ingreso.objects.all()
    gastos = Gasto.objects.all()

    if propiedad:
        ingresos = ingresos.filter(propiedad=propiedad)
        gastos = gastos.filter(propiedad=propiedad)

    total_ingresos = ingresos.aggregate(total=Sum('monto'))['total'] or 0
    total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0

    return {
        'ingresos': total_ingresos,
        'gastos': total_gastos,
        'utilidad': total_ingresos - total_gastos
    }


def balance_mensual(anio, mes, propiedad=None):
    ingresos = Ingreso.objects.filter(fecha__year=anio, fecha__month=mes)
    gastos = Gasto.objects.filter(fecha__year=anio, fecha__month=mes)

    if propiedad:
        ingresos = ingresos.filter(propiedad=propiedad)
        gastos = gastos.filter(propiedad=propiedad)

    total_ingresos = ingresos.aggregate(total=Sum('monto'))['total'] or 0
    total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0

    return {
        'anio': anio,
        'mes': mes,
        'ingresos': total_ingresos,
        'gastos': total_gastos,
        'utilidad': total_ingresos - total_gastos
    }


def balance_anual(anio, propiedad=None):
    ingresos = Ingreso.objects.filter(fecha__year=anio)
    gastos = Gasto.objects.filter(fecha__year=anio)

    if propiedad:
        ingresos = ingresos.filter(propiedad=propiedad)
        gastos = gastos.filter(propiedad=propiedad)

    total_ingresos = ingresos.aggregate(total=Sum('monto'))['total'] or 0
    total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0

    return {
        'anio': anio,
        'ingresos': total_ingresos,
        'gastos': total_gastos,
        'utilidad': total_ingresos - total_gastos
    }
