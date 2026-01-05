from django import forms
from .models import Ingreso
from .models import Gasto

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = [
            "fecha", 
            "monto_bruto", 
            "comision", 
            "descripcion", 
            "plataforma",
            "propiedad", 
            ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.TextInput(attrs={"placeholder": "Ej: Reserva Airbnb"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        monto = cleaned_data.get("monto_bruto")
        comision = cleaned_data.get("comision")

        if monto is not None and comision is not None:
            if comision > monto:
                raise forms.ValidationError(
                    "La comisión no puede ser mayor al monto bruto."
                )

        return cleaned_data


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = [
            "fecha",
            "propiedad", 
            "monto", 
            "categoria",
            "descripcion",
            ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),            
        }