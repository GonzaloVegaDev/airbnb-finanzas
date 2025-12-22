from django.contrib import admin
from .models import Propiedad, Ingreso, Gasto


@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'activa', 'creada_por', 'fecha_creacion')
    list_filter = ('activa',)
    search_fields = ('nombre', 'direccion')


@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'concepto', 'monto', 'propiedad', 'creado_por')
    list_filter = ('propiedad', 'fecha')
    search_fields = ('concepto',)


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'concepto', 'monto', 'propiedad', 'creado_por')
    list_filter = ('propiedad', 'fecha')
    search_fields = ('concepto',)
