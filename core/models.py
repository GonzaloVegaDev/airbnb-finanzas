from django.db import models
from django.contrib.auth.models import User


class Propiedad(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='activa')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Ingreso(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    monto_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha = models.DateField()
    plataforma = models.CharField(max_length=50)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def monto_neto(self):
        return self.monto_bruto - self.comision


class Gasto(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100)
    fecha = models.DateField()
    creado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="gastos"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.propiedad} - {self.categoria}"
