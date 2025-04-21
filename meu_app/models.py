from django.db import models
from django.contrib.auth.models import User

class Questionario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionamento com o User
    nome = models.CharField(max_length=100, blank=True, null=True)  # Permitindo nome em branco ou nulo
    idade = models.IntegerField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)   
    altura = models.FloatField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    objetivo = models.CharField(max_length=100)
    restricoes = models.TextField(blank=True)
    preferencia = models.TextField(blank=True)
    fome = models.CharField(max_length=50, blank=True)
    refeicoes_por_dia = models.CharField(max_length=10, blank=True)
    come_carne = models.BooleanField(default=True)
    gosta_de_legumes = models.BooleanField(default=True)
    agua = models.CharField(max_length=10, blank=True)  
    agua_bebida = models.FloatField(default=0)  # Novo campo para quantidade de água consumida em ml
    sono = models.CharField(max_length=10, blank=True)
    atividade_fisica = models.CharField(max_length=100, blank=True)
    usa_suplementos = models.BooleanField(default=False)
    estresse = models.CharField(max_length=100, blank=True)

    def __str__(self):
        # Retorna o nome ou "Questionário Anônimo" se o nome estiver em branco
        return self.nome if self.nome else "Questionário Anônimo"
