from .models import Cardapio, Questionario

# Função para calcular o perfil nutricional do usuário
def calcular_perfil(idade, peso, altura, objetivo, atividade):
    tmb = 10 * peso + 6.25 * altura - 5 * idade + 5  # Fórmula de TMB para homens

    # Fatores de atividade
    fatores = {
        'sedentario': 1.2,
        'moderado': 1.55,
        'intenso': 1.9
    }
    
    # Calorias com base na atividade
    calorias = tmb * fatores.get(atividade, 1.2)

    # Ajuste de calorias com base no objetivo
    if objetivo == 'perder_peso':
        calorias -= 500
    elif objetivo == 'ganhar_massa':
        calorias += 500

    # Macronutrientes
    proteinas = peso * 2  # Exemplo: 2g de proteína por kg de peso
    gorduras = peso * 1   # Exemplo: 1g de gordura por kg de peso
    carboidratos = (calorias - (proteinas * 4 + gorduras * 9)) / 4  # Restante das calorias para carboidratos

    return calorias, proteinas, carboidratos, gorduras

# Função para gerar o cardápio com base no objetivo do usuário
def gerar_cardapio_personalizado(usuario):
    questionario = Questionario.objects.filter(usuario=usuario).last()
    if not questionario:
        return None

    objetivo = questionario.objetivo
    
    # Lógica de cardápio baseado no objetivo
    if objetivo == 'perder_peso':
        cafe = "Omelete de claras + chá verde"
        almoco = "Frango grelhado + salada de folhas + abobrinha cozida"
        jantar = "Sopa de legumes + 1 fatia de pão integral"
    elif objetivo == 'ganhar_massa':
        cafe = "Vitamina de banana com aveia e whey"
        almoco = "Arroz, feijão, bife e batata doce"
        jantar = "Macarrão integral com frango desfiado"
    else:  # Para manter peso ou objetivos indefinidos
        cafe = "Iogurte natural com frutas"
        almoco = "Arroz integral, lentilha e frango grelhado"
        jantar = "Salada com atum e grão de bico"

    # Criar e retornar o cardápio no banco de dados
    cardapio = Cardapio.objects.create(
        usuario=usuario,
        cafe_da_manha=cafe,
        almoco=almoco,
        jantar=jantar
    )

    return cardapio
