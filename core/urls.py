from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("gastos/nuevo/", views.crear_gasto, name="crear_gasto"),
    path("ingresos/nuevo/", views.crear_ingreso, name="crear_ingreso"),
]
