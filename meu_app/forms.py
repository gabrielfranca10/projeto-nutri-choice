from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilNutricional, Questionario

# Formulário de Cadastro
class CadastroForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'seu@email.com',
        'class': 'input'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Formulário de Perfil Nutricional
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilNutricional
        fields = ['idade', 'peso', 'altura', 'objetivo']
        widgets = {
            'idade': forms.NumberInput(attrs={'placeholder': 'Idade', 'class': 'input'}),
            'peso': forms.NumberInput(attrs={'placeholder': 'Peso em kg', 'class': 'input'}),
            'altura': forms.NumberInput(attrs={'placeholder': 'Altura em cm', 'class': 'input'}),
            'objetivo': forms.Select(attrs={'class': 'input'}),
        }

# Formulário de Questionário Nutricional
class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        exclude = ['user']  # user será definido na view

        widgets = {
            'gosta_de_legumes': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'come_carne': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'tem_restricao': forms.Textarea(attrs={'placeholder': 'Ex: lactose, glúten, etc.', 'class': 'input'}),
            'preferencias': forms.Textarea(attrs={'placeholder': 'Ex: Gosto de frutas cítricas, evito doces...', 'class': 'input'}),
            'refeicoes_por_dia': forms.NumberInput(attrs={'class': 'input'}),
            'atividade_fisica': forms.TextInput(attrs={'placeholder': 'Ex: Caminhada 3x por semana', 'class': 'input'}),
            'sono': forms.NumberInput(attrs={'placeholder': 'Horas de sono', 'class': 'input'}),
            'agua': forms.NumberInput(attrs={'placeholder': 'Copos por dia', 'class': 'input'}),
        }

        labels = {
            'gosta_de_legumes': 'Você gosta de legumes?',
            'come_carne': 'Você consome carne?',
            'tem_restricao': 'Possui alguma restrição alimentar?',
            'preferencias': 'Preferências alimentares',
            'refeicoes_por_dia': 'Quantas refeições faz por dia?',
            'atividade_fisica': 'Nível de atividade física',
            'sono': 'Quantas horas de sono por noite?',
            'agua': 'Quantos copos de água por dia?',
        }
