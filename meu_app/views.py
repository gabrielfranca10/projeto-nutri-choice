from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Questionario


# Redireciona a raiz do site para a tela de login
def redirecionar_para_login(request):
    return redirect('login')


# === TELA DE LOGIN ===
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'meu_app/login.html', {
                'erro': 'Preencha todos os campos'
            })

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('perfil_nutricional')
        else:
            return render(request, 'meu_app/login.html', {
                'erro': 'Credenciais inválidas'
            })

    return render(request, 'meu_app/login.html')


# === TELA DE CADASTRO ===
def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'meu_app/cadastro.html', {
                'erro': 'Preencha todos os campos'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'meu_app/cadastro.html', {
                'erro': 'Usuário já existe'
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # Login automático
        return redirect('questionario')

    return render(request, 'meu_app/cadastro.html')


# === QUESTIONÁRIO NUTRICIONAL ===
def questionario_view(request):
    if request.method == 'POST':
        dados = {
            'objetivo': request.POST.get('objetivo'),
            'restricoes': request.POST.get('restricoes') or '',
            'preferencia': request.POST.get('preferencia') or '',
            'refeicoes_por_dia': request.POST.get('refeicoes_por_dia'),
            'come_carne': request.POST.get('come_carne') == 'on',
            'gosta_de_legumes': request.POST.get('gosta_de_legumes') == 'on',
            'agua': request.POST.get('agua') or '0',
            'sono': request.POST.get('sono') or '0',
            'atividade_fisica': request.POST.get('atividade_fisica'),
            'usa_suplementos': request.POST.get('usa_suplementos') == 'on',
            'estresse': request.POST.get('estresse'),
        }

        campos_obrigatorios = ['objetivo', 'refeicoes_por_dia', 'atividade_fisica', 'estresse']
        for campo in campos_obrigatorios:
            if not dados[campo]:
                return render(request, 'meu_app/questionario.html', {
                    'erro': 'Preencha todos os campos obrigatórios'
                })

        Questionario.objects.create(**dados)
        cardapio = gerar_cardapio_personalizado(dados)
        return render(request, 'meu_app/cardapio.html', {'cardapio': cardapio, 'dados': dados})

    return render(request, 'meu_app/questionario.html')


# === GERADOR DE CARDÁPIO ===
def gerar_cardapio_personalizado(dados):
    cardapio = {
        'Café da Manhã': [],
        'Almoço': [],
        'Lanche da Tarde': [],
        'Jantar': [],
    }

    if dados['objetivo'] == 'ganhar':
        cardapio['Café da Manhã'].append("Ovos mexidos + pão integral + vitamina de banana com aveia")
        cardapio['Almoço'].append("Arroz integral + frango grelhado + legumes no vapor")
        cardapio['Lanche da Tarde'].append("Iogurte natural com granola")
        cardapio['Jantar'].append("Omelete com batata doce e salada")
    elif dados['objetivo'] == 'perder':
        cardapio['Café da Manhã'].append("Iogurte desnatado + frutas vermelhas")
        cardapio['Almoço'].append("Peito de frango + salada verde com azeite e quinoa")
        cardapio['Lanche da Tarde'].append("Castanhas e uma fruta")
        cardapio['Jantar'].append("Sopa de legumes com frango desfiado")
    elif dados['objetivo'] == 'manter':
        cardapio['Café da Manhã'].append("Pão integral com queijo branco + café sem açúcar")
        cardapio['Almoço'].append("Arroz + feijão + carne magra + salada")
        cardapio['Lanche da Tarde'].append("Fruta + iogurte")
        cardapio['Jantar'].append("Sanduíche natural + suco de frutas")

    if 'atum' in dados['preferencia'].lower():
        for key in cardapio:
            cardapio[key] = [item.replace('atum', 'frango') for item in cardapio[key]]

    if not dados['come_carne']:
        for key in cardapio:
            cardapio[key] = [item.replace('frango', 'grão-de-bico') for item in cardapio[key]]

    if 'glúten' in dados['restricoes'].lower():
        for key in cardapio:
            cardapio[key] = [item.replace('pão', 'pão sem glúten') for item in cardapio[key]]

    return cardapio


# === PERFIL NUTRICIONAL FINAL ===
def perfil_nutricional_view(request):
    ultimo = Questionario.objects.last()
    return render(request, 'meu_app/perfil.html', {'dados': ultimo})


# === CARDÁPIO PERSONALIZADO ===
def cardapio_view(request):
    ultimo = Questionario.objects.last()
    cardapio = gerar_cardapio_personalizado(vars(ultimo))
    return render(request, 'meu_app/cardapio.html', {'cardapio': cardapio, 'dados': ultimo})
