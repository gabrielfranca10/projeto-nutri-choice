# meu_app/services.py

def gerar_cardapio_personalizado(dados):
    """
    Gera uma sugestão simples de cardápio baseado nos dados do questionário.
    Depois você pode deixar mais inteligente se quiser.
    """
    objetivo = dados.get('objetivo', '').lower()
    refeicoes = dados.get('refeicoes_por_dia', 3)

    if objetivo == 'emagrecimento':
        sugestao = "Inclua mais vegetais, proteínas magras e reduza carboidratos simples."
    elif objetivo == 'ganho de massa':
        sugestao = "Inclua mais proteínas, carboidratos complexos e boas fontes de gordura."
    else:
        sugestao = "Mantenha uma alimentação equilibrada com variedade de nutrientes."

    cardapio = f"""
Objetivo: {objetivo.title()}
Sugestão nutricional: {sugestao}

Quantidade de refeições por dia: {refeicoes}

Exemplo de refeições:
- Café da manhã: Ovos mexidos, pão integral, frutas
- Almoço: Arroz integral, peito de frango grelhado, salada variada
- Lanche: Iogurte natural e castanhas
- Jantar: Sopa de legumes com proteína
    """

    return cardapio.strip()
