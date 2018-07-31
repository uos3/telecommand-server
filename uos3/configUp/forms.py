from django import forms
from .models import config


class configForm(forms.ModelForm):
    class Meta:
        model = config
        exclude = [
            'date_submitted',
            'user_submitted',
            'confirmed_uplink',
            'date_uplink',
        ]
