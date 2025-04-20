from django.db import models
from django.contrib.auth.models import User

class Questionario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=True)
    idade = models.IntegerField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)   # Novo campo
    altura = models.FloatField(null=True, blank=True) # Novo campo
    genero = models.CharField(max_length=20, blank=True)
    objetivo = models.CharField(max_length=100)
    restricoes = models.TextField(blank=True)
    preferencia = models.TextField(blank=True)
    fome = models.CharField(max_length=50, blank=True)
    refeicoes_por_dia = models.CharField(max_length=10, blank=True)
    come_carne = models.BooleanField(default=True)
    gosta_de_legumes = models.BooleanField(default=True)
    agua = models.CharField(max_length=10, blank=True)
    sono = models.CharField(max_length=10, blank=True)
    atividade_fisica = models.CharField(max_length=100, blank=True)
    usa_suplementos = models.BooleanField(default=False)
    estresse = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome or "Questionário Anônimo"
