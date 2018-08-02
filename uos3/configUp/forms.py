from django import forms
from .models import config


class configCreateForm(forms.ModelForm):
    class Meta:
        model = config
        exclude = [
            'date_submitted',
            'date_modified',
            'user_submitted',
            'confirmed_uplink',
            'date_uplink',
        ]


class configModForm(forms.ModelForm):
    class Meta:
        model = config
        exclude = [
            'date_submitted',
            'date_modified',
            'user_submitted',
            'confirmed_uplink',
            'date_uplink',
        ]
