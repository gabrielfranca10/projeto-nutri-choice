from django.db import models
from django.contrib.auth.models import User

# Perfil Nutricional do Usuário
class PerfilNutricional(models.Model):
    OBJETIVOS = [
        ('ganhar', 'Ganho de massa'),
        ('perder', 'Perda de peso'),
        ('manter', 'Manutenção'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    objetivo = models.CharField(max_length=10, choices=OBJETIVOS)

    def __str__(self):
        return f'Perfil de {self.user.username}'


# Questionário de hábitos e preferências
class Questionario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gosta_de_legumes = models.BooleanField(default=True)
    come_carne = models.BooleanField(default=True)
    tem_restricao = models.TextField(blank=True, null=True)
    preferencias = models.TextField(blank=True, null=True)
    refeicoes_por_dia = models.IntegerField(default=3)
    atividade_fisica = models.CharField(max_length=100)
    sono = models.IntegerField(help_text="Horas de sono por noite")
    agua = models.IntegerField(help_text="Copos de água por dia")

    def __str__(self):
        return f'Questionário de {self.user.username}'
