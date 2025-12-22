from django.db import models
from django.contrib.auth.models import User


class Propiedad(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    activa = models.BooleanField(default=True)
    creada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='propiedades_creadas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Ingreso(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    fecha = models.DateField()
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    creado_por = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name='ingresos_finanzas'
)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.concepto} - {self.monto}"


class Gasto(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    fecha = models.DateField()
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    creado_por = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name='gastos_finanzas'
)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.concepto} - {self.monto}"
