from django import forms
from .models import RegistroPeso

class RegistroPesoForm(forms.ModelForm):
    class Meta:
        model = RegistroPeso
        fields = ['peso_atual', 'meta_peso', 'observacoes']
        widgets = {
            'peso_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Digite seu peso atual'
            }),
            'meta_peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Digite sua meta de peso'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações (opcional)'
            }),
        }
        labels = {
            'peso_atual': 'Peso Atual (kg)',
            'meta_peso': 'Meta de Peso (kg)',
            'observacoes': 'Observações'
        }
