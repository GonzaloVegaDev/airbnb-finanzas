from django import forms
from .models import Ingreso
from .models import Gasto

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = [
            "propiedad",
            "plataforma",
            "monto_bruto",
            "comision",
            "fecha",
        ]

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ["propiedad", "monto", "categoria", "fecha"]