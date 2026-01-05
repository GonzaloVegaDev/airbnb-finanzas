from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingreso, Gasto, Propiedad
from .forms import IngresoForm, GastoForm
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

@login_required
def dashboard(request):
    hoy = date.today()

    mes = int(request.GET.get("mes", hoy.month))
    anio = int(request.GET.get("anio", hoy.year))

    meses = list(range(1, 13))

    ingresos_qs = Ingreso.objects.filter(
        fecha__month=mes,
        fecha__year=anio
    )

    gastos_qs = Gasto.objects.filter(
        fecha__month=mes,
        fecha__year=anio
    )

    total_ingresos = ingresos_qs.aggregate(
        total=Sum("monto_bruto")
    )["total"] or 0

    total_comisiones = ingresos_qs.aggregate(
        total=Sum("comision")
    )["total"] or 0

    total_gastos = gastos_qs.aggregate(
        total=Sum("monto")
    )["total"] or 0

    balance = total_ingresos - total_comisiones - total_gastos
    ingresos = ingresos_qs.order_by("-fecha")
    gastos = gastos_qs.order_by("-fecha")


    context = {
        "mes": mes,
        "anio": anio,
        "total_ingresos": total_ingresos,
        "total_comisiones": total_comisiones,
        "total_gastos": total_gastos,
        "balance": balance,
        "meses": meses,
        "ingresos": ingresos,
        "gastos": gastos,
    }

    return render(request, "core/dashboard.html", context)

@login_required
def crear_ingreso(request):
    if request.method == "POST":
        form = IngresoForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)

            ingreso.creado_por = request.user
            ingreso.propiedad = Propiedad.objects.first()  # 👈 CLAVE
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
            gasto.propiedad = Propiedad.objects.first()
            gasto.save()
            return redirect("dashboard")
    else:
        form = GastoForm()

    return render(request, "core/crear_gasto.html", {
        "form": form,
        "editar": False,
        })

def lista_ingresos(request):
    ingresos = Ingreso.objects.all().order_by("-fecha")
    return render(request, "core/lista_ingresos.html", {
        "ingresos": ingresos
    })


def lista_gastos(request):
    gastos = Gasto.objects.all().order_by("-fecha")
    return render(request, "core/lista_gastos.html", {
        "gastos": gastos
    })

@login_required
def editar_ingreso(request, pk):
    ingreso = get_object_or_404(Ingreso, pk=pk)

    if request.method == "POST":
        form = IngresoForm(request.POST, instance=ingreso)
        if form.is_valid():
            ingreso_editado = form.save(commit=False)
            ingreso_editado.propiedad = ingreso.propiedad
            ingreso_editado.creado_por = ingreso.creado_por
            ingreso_editado.save()
            return redirect("lista_ingresos")
    else:
        form = IngresoForm(instance=ingreso)

    return render(request, "core/crear_ingreso.html", {
        "form": form,
        "editar": True,
    })

@login_required
def eliminar_ingreso(request, pk):
    ingreso = get_object_or_404(Ingreso, pk=pk)

    if request.method == "POST":
        ingreso.delete()
        return redirect("lista_ingresos")

    return render(request, "core/confirmar_eliminar.html", {
        "objeto": ingreso,
        "tipo": "ingreso",
    })



@login_required
def editar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)

    if request.method == "POST":
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect("lista_gastos")
    else:
        form = GastoForm(instance=gasto)

    return render(request, "core/crear_gasto.html", {
        "form": form,
        "editar": True,
    })

@login_required
def eliminar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)

    if request.method == "POST":
        gasto.delete()
        return redirect("dashboard")

    return render(request, "core/confirmar_eliminar.html", {
        "objeto": gasto,
        "tipo": "gasto",
    })