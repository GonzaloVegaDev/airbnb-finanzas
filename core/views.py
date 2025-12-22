from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from .models import Ingreso, Gasto
from .forms import IngresoForm, GastoForm

@login_required
def dashboard(request):
    ingresos_total = Ingreso.objects.aggregate(Sum('monto_bruto'))['monto_bruto__sum'] or 0
    gastos_total = Gasto.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    balance = ingresos_total - gastos_total
    return render(request, "core/dashboard.html", {
        "ingresos_total": ingresos_total,
        "gastos_total": gastos_total,
        "balance": balance
    })

    return render(
        request,
        "core/dashboard.html",
        {
            "ingresos_total": ingresos_total,
            "gastos_total": gastos_total,
            "balance": ingresos_total - gastos_total,
        },
    )


@login_required
def crear_ingreso(request):
    if request.method == "POST":
        form = IngresoForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.creado_por = request.user
            ingreso.save()
            return redirect("dashboard")
    else:
        form = IngresoForm()

    return render(request, "core/crear_ingreso.html", {"form": form})


@login_required
def crear_gasto(request):
    if request.method == "POST":
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.creado_por = request.user
            gasto.save()
            return redirect("dashboard")
    else:
        form = GastoForm()

    return render(request, "core/crear_gasto.html", {"form": form})

