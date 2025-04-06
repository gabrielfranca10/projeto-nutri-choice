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
