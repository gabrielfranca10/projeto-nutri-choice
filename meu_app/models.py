from django.db import models
from django.contrib.auth.models import User

# === MODELO QUESTIONÁRIO ===
class Questionario(models.Model):
    USUARIO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    ATIVIDADE_FISICA_CHOICES = [
        ('Sedentario', 'Sedentário'),
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Intensa', 'Intensa'),
    ]
    FOME_CHOICES = [
        ('Baixa', 'Baixa'),
        ('Moderada', 'Moderada'),
        ('Alta', 'Alta'),
    ]
    SONO_CHOICES = [
        ('Ruim', 'Ruim'),
        ('Moderado', 'Moderado'),
        ('Bom', 'Bom'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questionarios", verbose_name="Usuário")
    nome = models.CharField(max_length=100, blank=True, null=True)  # Pode ser usado, mas prefira o Perfil
    idade = models.IntegerField(null=True, blank=True)
    objetivo = models.CharField(max_length=100)
    restricoes = models.TextField(blank=True)
    preferencia = models.TextField(blank=True)
    refeicoes_por_dia = models.IntegerField(null=True, blank=True)
    come_carne = models.BooleanField(default=True)
    gosta_de_legumes = models.BooleanField(default=True)
    usa_suplementos = models.BooleanField(default=False)
    estresse = models.CharField(max_length=100, blank=True)
    atividade_fisica = models.CharField(max_length=100, choices=ATIVIDADE_FISICA_CHOICES, blank=True)
    fome = models.CharField(max_length=100, choices=FOME_CHOICES, blank=True)
    sono = models.CharField(max_length=100, choices=SONO_CHOICES, blank=True)
    # Campos para controle de atualização do perfil
    ultima_atualizacao = models.DateField(null=True, blank=True, verbose_name="Última atualização do perfil")
    ultima_modificacao = models.DateField(null=True, blank=True, verbose_name="Última modificação relevante")

    def __str__(self):
        return self.nome if self.nome else f"Questionário de {self.usuario.username}"

    class Meta:
        verbose_name = "Questionário"
        verbose_name_plural = "Questionários"

# === MODELO ALIMENTO ===
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

# === MODELO SUBSTITUIÇÃO ===
class Substituicao(models.Model):
    alimento_original = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='alternativas_para')
    alternativa = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='substitui')
    justificativa = models.TextField(blank=True)

    def __str__(self):
        return f"{self.alternativa.nome} como substituto de {self.alimento_original.nome}"

    class Meta:
        verbose_name = "Substituição"
        verbose_name_plural = "Substituições"

# === MODELO CARDÁPIO ===
class Cardapio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    itens = models.ManyToManyField(Alimento, blank=True)
    descricao = models.TextField(blank=True)  # Texto do cardápio gerado

    def __str__(self):
        return f"Cardápio de {self.usuario.username} em {self.data_criacao.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Cardápio"
        verbose_name_plural = "Cardápios"

# === MODELO PERFIL ===
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)  # Nome do usuário para exibir no perfil
    idade = models.IntegerField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    objetivo = models.CharField(max_length=100, blank=True)
    restricoes = models.TextField(blank=True)
    preferencia = models.TextField(blank=True)
    questionario = models.OneToOneField(Questionario, on_delete=models.CASCADE, null=True, blank=True, related_name="perfil")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

# === MODELO REGISTRO DE PESO ===
class RegistroPeso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    peso_atual = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso Atual (kg)")
    meta_peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Meta de Peso (kg)")
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Registro de Peso"
        verbose_name_plural = "Registros de Peso"
        ordering = ['-data']

    def __str__(self):
        return f"{self.usuario.username} - {self.data}: {self.peso_atual}kg (Meta: {self.meta_peso}kg)"