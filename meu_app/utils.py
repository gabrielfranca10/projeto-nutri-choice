def calcular_perfil(idade, peso, altura, objetivo, atividade):
    tmb = 10 * peso + 6.25 * altura - 5 * idade + 5

    fatores = {
        'sedentario': 1.2,
        'moderado': 1.55,
        'intenso': 1.9
    }
    calorias = tmb * fatores.get(atividade, 1.2)

    if objetivo == 'perder_peso':
        calorias -= 500
    elif objetivo == 'ganhar_massa':
        calorias += 500

    proteinas = peso * 2
    gorduras = peso * 1
    carboidratos = (calorias - (proteinas * 4 + gorduras * 9)) / 4

    return calorias, proteinas, carboidratos, gorduras

from .models import Cardapio, Questionario

def gerar_cardapio(usuario):
    questionario = Questionario.objects.filter(usuario=usuario).last()
    if not questionario:
        return None

    objetivo = questionario.objetivo
    if objetivo == 'perder_peso':
        cafe = "Iogurte com granola e frutas"
        almoco = "Peito de frango grelhado com salada"
        jantar = "Sopa de legumes"
    elif objetivo == 'ganhar_massa':
        cafe = "Ovos mexidos com aveia e banana"
        almoco = "Arroz, feijão, carne moída e batata-doce"
        jantar = "Panqueca de frango e vitamina"
    else:
        cafe = "Pão integral com queijo branco"
        almoco = "Arroz, feijão, frango grelhado e salada"
        jantar = "Macarrão integral com legumes"

    return Cardapio.objects.create(
        usuario=usuario,
        cafe_da_manha=cafe,
        almoco=almoco,
        jantar=jantar
    )

def gerar_cardapio(questionario):
    # Simulação simples de cardápio com base no objetivo
    if questionario.objetivo == 'perder_peso':
        return [
            "Café da manhã: Omelete de claras + chá verde",
            "Almoço: Frango grelhado + salada de folhas + abobrinha cozida",
            "Jantar: Sopa de legumes + 1 fatia de pão integral"
        ]
    elif questionario.objetivo == 'ganhar_massa':
        return [
            "Café da manhã: Vitamina de banana com aveia e whey",
            "Almoço: Arroz, feijão, bife e batata doce",
            "Jantar: Macarrão integral com frango desfiado"
        ]
    else:  # manter peso ou objetivo indefinido
        return [
            "Café da manhã: Iogurte natural com frutas",
            "Almoço: Arroz integral, lentilha e frango grelhado",
            "Jantar: Salada com atum e grão de bico"
        ]