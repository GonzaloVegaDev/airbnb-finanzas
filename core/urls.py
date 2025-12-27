from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # INGRESOS
    path("ingresos/nuevo/", views.crear_ingreso, name="crear_ingreso"),
    path("ingresos/", views.lista_ingresos, name="lista_ingresos"),
    path("ingresos/<int:pk>/editar/", views.editar_ingreso, name="editar_ingreso"),
    path("ingresos/<int:pk>/eliminar/", views.eliminar_ingreso, name="eliminar_ingreso"),
   
    # GASTOS
    path("gastos/nuevo/", views.crear_gasto, name="crear_gasto"),
    path("gastos/", views.lista_gastos, name="lista_gastos"),
    path("gastos/<int:pk>/editar/", views.editar_gasto, name="editar_gasto"),
    path("gastos/<int:pk>/eliminar/", views.eliminar_gasto, name="eliminar_gasto"),
]
