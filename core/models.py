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
    fecha = models.DateField()
    plataforma = models.CharField(max_length=50, blank=True)
    monto_bruto = models.DecimalField(max_digits=12, decimal_places=2)
    comision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.propiedad} - {self.fecha}"


class Gasto(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    fecha = models.DateField()
    categoria = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.propiedad} - {self.categoria}"
