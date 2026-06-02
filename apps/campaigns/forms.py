from django import forms

from .models import Campaign


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ["nombre", "descripcion", "meta_recaudacion", "activa", "imagen"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "meta_recaudacion": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "1", "placeholder": "Meta en MXN"}
            ),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "imagen": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean_meta_recaudacion(self):
        meta = self.cleaned_data["meta_recaudacion"]
        if meta <= 0:
            raise forms.ValidationError("La meta debe ser mayor a cero.")
        return meta
