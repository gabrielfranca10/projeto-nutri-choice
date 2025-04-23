from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Alimento, Substituicao, Questionario
from django.http import HttpResponse

def debug_host(request):
    return HttpResponse(f"Host recebido: {request.get_host()}")

# === TELA DE LOGIN ===
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Preencha todos os campos')
            return render(request, 'meu_app/login.html')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('perfil_nutricional')  # Redireciona para o perfil nutricional
        else:
            messages.error(request, 'Credenciais inválidas')
            return render(request, 'meu_app/login.html')

    return render(request, 'meu_app/login.html')

# === TELA DE CADASTRO ===
def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        password2 = request.POST.get('confirmar_senha')

        if not all([username, email, password, password2]):
            messages.error(request, 'Preencha todos os campos')
            return render(request, 'meu_app/cadastro.html')

        if password != password2:
            messages.error(request, 'As senhas não coincidem')
            return render(request, 'meu_app/cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe')
            return render(request, 'meu_app/cadastro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('questionario')  # Redireciona para o questionário

    return render(request, 'meu_app/cadastro.html')

# === QUESTIONÁRIO NUTRICIONAL ===
@login_required
def questionario_view(request):
    if request.method == 'POST':
        def parse_float(valor):
            try:
                return float(valor)
            except (TypeError, ValueError):
                return None

        def parse_int(valor):
            try:
                return int(valor)
            except (TypeError, ValueError):
                return None

        dados = {
            'nome': request.POST.get('nome') or '',
            'idade': parse_int(request.POST.get('idade')),
            'peso': parse_float(request.POST.get('peso')),
            'altura': parse_float(request.POST.get('altura')),
            'genero': request.POST.get('genero') or '',
            'objetivo': request.POST.get('objetivo'),
            'restricoes': request.POST.get('restricoes') or '',
            'preferencia': request.POST.get('preferencia') or '',
            'fome': request.POST.get('fome') or '',
            'refeicoes_por_dia': request.POST.get('refeicoes_por_dia'),
            'come_carne': request.POST.get('come_carne') == 'on',
            'gosta_de_legumes': request.POST.get('gosta_de_legumes') == 'on',
            'agua': request.POST.get('agua') or '',
            'agua_bebida': parse_float(request.POST.get('agua_bebida')),
            'sono': request.POST.get('sono') or '',
            'atividade_fisica': request.POST.get('atividade_fisica'),
            'usa_suplementos': request.POST.get('usa_suplementos') == 'on',
            'estresse': request.POST.get('estresse'),
        }

        campos_obrigatorios = ['objetivo', 'refeicoes_por_dia', 'atividade_fisica', 'estresse']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                messages.error(request, 'Preencha todos os campos obrigatórios')
                return render(request, 'meu_app/questionario.html')

        Questionario.objects.update_or_create(
            usuario=request.user,
            defaults=dados
        )

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

    objetivo = dados.get('objetivo', '').lower()

    if 'ganhar' in objetivo:
        cardapio['Café da Manhã'].append("Ovos mexidos + pão integral + vitamina de banana com aveia")
        cardapio['Almoço'].append("Arroz integral + frango grelhado + legumes no vapor")
        cardapio['Lanche da Tarde'].append("Iogurte natural com granola")
        cardapio['Jantar'].append("Omelete com batata doce e salada")
    elif 'perder' in objetivo:
        cardapio['Café da Manhã'].append("Iogurte desnatado + frutas vermelhas")
        cardapio['Almoço'].append("Peito de frango + salada verde com azeite e quinoa")
        cardapio['Lanche da Tarde'].append("Castanhas e uma fruta")
        cardapio['Jantar'].append("Sopa de legumes com frango desfiado")
    elif 'saúde' in objetivo or 'saude' in objetivo:
        cardapio['Café da Manhã'].append("Pão integral com queijo branco + café sem açúcar")
        cardapio['Almoço'].append("Arroz + feijão + carne magra + salada")
        cardapio['Lanche da Tarde'].append("Fruta + iogurte")
        cardapio['Jantar'].append("Sanduíche natural + suco de frutas")

    if 'atum' in dados.get('preferencia', '').lower():
        for key in cardapio:
            cardapio[key] = [item.replace('atum', 'frango') for item in cardapio[key]]

    if not dados.get('come_carne', False):
        for key in cardapio:
            cardapio[key] = [item.replace('frango', 'grão-de-bico') for item in cardapio[key]]

    if 'glúten' in dados.get('restricoes', '').lower() or 'gluten' in dados.get('restricoes', '').lower():
        for key in cardapio:
            cardapio[key] = [item.replace('pão', 'pão sem glúten') for item in cardapio[key]]

    return cardapio

# === PERFIL NUTRICIONAL FINAL ===
@login_required
def perfil_nutricional_view(request):
    ultimo = Questionario.objects.filter(usuario=request.user).last()

    if ultimo:
        agua_bebida = ultimo.agua_bebida or 0
        meta_agua = 2000
        agua_faltante = max(meta_agua - agua_bebida, 0)
        porcentagem_agua = min((agua_bebida / meta_agua) * 100, 100)

        cardapio = gerar_cardapio_personalizado(vars(ultimo))

        return render(request, 'meu_app/perfil.html', {
            'questionario': ultimo,
            'agua_faltante': agua_faltante,
            'porcentagem_agua': round(porcentagem_agua, 2),
            'cardapio': cardapio,
            'usuario': request.user,
            'idade': ultimo.idade,
            'peso': ultimo.peso,
            'altura': ultimo.altura,
            'nome': ultimo.nome,
        })
    else:
        messages.error(request, 'Complete o questionário para ver seu perfil nutricional!')
        return render(request, 'meu_app/perfil.html')

# === CARDÁPIO PERSONALIZADO ===
@login_required
def cardapio_view(request):
    ultimo = Questionario.objects.filter(usuario=request.user).last()
    if ultimo:
        cardapio = gerar_cardapio_personalizado(vars(ultimo))
        return render(request, 'meu_app/cardapio.html', {'cardapio': cardapio, 'dados': ultimo})
    else:
        messages.error(request, 'Complete o questionário para ver seu cardápio personalizado!')
        return render(request, 'meu_app/cardapio.html')

# === LOGOUT ===
def logout_view(request):
    logout(request)
    return redirect('login')

# REDIRECIONAMENTO PARA LOGIN
def redirecionar_para_login(request):
    return redirect('login')

# === EDITAR PERFIL ===
@login_required
def editar_perfil(request):
    questionario = Questionario.objects.get(usuario=request.user)

    if request.method == 'POST':
        questionario.nome = request.POST.get('nome', questionario.nome)
        questionario.idade = request.POST.get('idade', questionario.idade)
        questionario.peso = request.POST.get('peso', questionario.peso)
        questionario.altura = request.POST.get('altura', questionario.altura)
        questionario.genero = request.POST.get('genero', questionario.genero)
        questionario.objetivo = request.POST.get('objetivo', questionario.objetivo)
        questionario.restricoes = request.POST.get('restricoes', questionario.restricoes)
        questionario.preferencia = request.POST.get('preferencia', questionario.preferencia)
        questionario.fome = request.POST.get('fome', questionario.fome)
        questionario.refeicoes_por_dia = request.POST.get('refeicoes_por_dia', questionario.refeicoes_por_dia)
        questionario.come_carne = request.POST.get('come_carne') == 'on'
        questionario.gosta_de_legumes = request.POST.get('gosta_de_legumes') == 'on'
        questionario.agua = request.POST.get('agua', questionario.agua)
        questionario.agua_bebida = request.POST.get('agua_bebida', questionario.agua_bebida)
        questionario.sono = request.POST.get('sono', questionario.sono)
        questionario.atividade_fisica = request.POST.get('atividade_fisica', questionario.atividade_fisica)
        questionario.usa_suplementos = request.POST.get('usa_suplementos') == 'on'
        questionario.estresse = request.POST.get('estresse', questionario.estresse)
        questionario.save()

        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil_nutricional')

    return render(request, 'meu_app/editar_perfil.html', {'questionario': questionario})

# === EXCLUIR PERFIL ===
@login_required
def excluir_perfil(request):
    if request.method == 'POST':
        # Exclui o questionário do usuário antes de excluir o usuário
        try:
            questionario = Questionario.objects.get(usuario=request.user)
            questionario.delete()  # Exclui os dados do questionário
        except Questionario.DoesNotExist:
            pass  # Caso o questionário não exista, nada será feito

        # Exclui o usuário
        user = request.user
        user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('login')  # Redireciona para a página inicial ou outra página

    return render(request, 'meu_app/excluir_conta.html')

# === SUBSTITUIÇÕES ALIMENTARES ===
@login_required
def substituicoes_view(request):
    termo = request.GET.get('busca')
    substituicoes = []
    erro = ''

    if termo:
        try:
            # Tenta encontrar o alimento
            alimento = Alimento.objects.get(nome__icontains=termo)

            # Pega preferências do usuário (se tiver questionário preenchido)
            questionario = Questionario.objects.filter(usuario=request.user).last()
            preferencias = {
                'vegetariano': not questionario.come_carne if questionario else False,
                'sem_lactose': 'lactose' in (questionario.restricoes.lower() if questionario else ''),
                'sem_gluten': 'gluten' in (questionario.restricoes.lower() if questionario else ''),
            }

            # Filtra substituições compatíveis
            substituicoes = Substituicao.objects.filter(alimento_original=alimento)
            substituicoes = [
                s for s in substituicoes
                if (not preferencias['vegetariano'] or s.alternativa.vegetariano)
                and (not preferencias['sem_lactose'] or s.alternativa.sem_lactose)
                and (not preferencias['sem_gluten'] or s.alternativa.sem_gluten)
            ]

        except Alimento.DoesNotExist:
            erro = "Alimento não encontrado. Tente outro nome ou veja sugestões abaixo."
            sugestoes = Alimento.objects.filter(nome__icontains=termo[:3])
            return render(request, 'meu_app/substituicoes.html', {'erro': erro, 'sugestoes': sugestoes})

    return render(request, 'meu_app/substituicoes.html', {
        'substituicoes': substituicoes,
        'termo': termo
    })