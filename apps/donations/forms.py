from django import forms

from .models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["monto", "mensaje"]
        widgets = {
            "monto": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "1", "placeholder": "Monto"}
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Mensaje opcional de apoyo",
                }
            ),
        }

    def clean_monto(self):
        monto = self.cleaned_data["monto"]
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return monto
