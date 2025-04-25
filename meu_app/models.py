from django.db import models
from django.contrib.auth.models import User

# Modelo Questionário
class Questionario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questionarios", verbose_name="Usuário")
    nome = models.CharField(max_length=100, blank=True, null=True)
    idade = models.IntegerField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)  # em kg
    altura = models.FloatField(null=True, blank=True)  # em metros
    genero = models.CharField(max_length=20, blank=True)
    objetivo = models.CharField(max_length=100)
    restricoes = models.TextField(blank=True)
    preferencia = models.TextField(blank=True)
    fome = models.CharField(max_length=50, blank=True)
    refeicoes_por_dia = models.IntegerField(null=True, blank=True)
    come_carne = models.BooleanField(default=True)
    gosta_de_legumes = models.BooleanField(default=True)
    agua_bebida = models.FloatField(default=0, null=True, blank=True)  # ml de água por dia
    agua = models.CharField(max_length=50, blank=True)
    sono = models.CharField(max_length=10, blank=True)
    atividade_fisica = models.CharField(max_length=100, blank=True)
    usa_suplementos = models.BooleanField(default=False)
    estresse = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nome if self.nome else f"Questionário de {self.usuario.username}"

    class Meta:
        verbose_name = "Questionário"
        verbose_name_plural = "Questionários"



# Modelo Alimento
class Alimento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=100)
    valor_nutricional = models.TextField(blank=True)
    vegetariano = models.BooleanField(default=False)
    sem_lactose = models.BooleanField(default=False)
    sem_gluten = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Alimento"
        verbose_name_plural = "Alimentos"


# Modelo Substituição
class Substituicao(models.Model):
    alimento_original = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='alternativas_para')
    alternativa = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='substitui')
    justificativa = models.TextField(blank=True)

    def __str__(self):
        return f"{self.alternativa.nome} como substituto de {self.alimento_original.nome}"

    class Meta:
        verbose_name = "Substituição"
        verbose_name_plural = "Substituições"


# Modelo Cardapio
class Cardapio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    itens = models.ManyToManyField(Alimento, blank=True)

    def __str__(self):
        return f"Cardápio de {self.usuario.username} em {self.data_criacao.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Cardápio"
        verbose_name_plural = "Cardápios"


# Modelo Perfil
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    peso = models.FloatField()
    altura = models.FloatField()
    objetivo = models.CharField(max_length=100)
    restricoes = models.TextField(blank=True)
    preferencia = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"