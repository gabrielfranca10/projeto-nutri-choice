from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Alimento, Substituicao, Questionario, Perfil, RegistroPeso
from .forms import RegistroPesoForm
from datetime import datetime, timedelta
from django.http import HttpResponse

# === DEBUG HOST ===
def debug_host(request):
    return HttpResponse(f"Host recebido: {request.get_host()}")

# === LOGIN ===
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
            return redirect('perfil_nutricional')
        else:
            messages.error(request, 'Credenciais inválidas')
            return render(request, 'meu_app/login.html')

    return render(request, 'meu_app/login.html')

# === CADASTRO ===
def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('perfil_nutricional')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        password2 = request.POST.get('confirmar_senha')

        if not all([nome, username, email, password, password2]):
            messages.error(request, 'Preencha todos os campos')
            return render(request, 'meu_app/cadastro.html')

        if password != password2:
            messages.error(request, 'As senhas não coincidem')
            return render(request, 'meu_app/cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe')
            return render(request, 'meu_app/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return render(request, 'meu_app/cadastro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        Perfil.objects.create(user=user, nome=nome)
        login(request, user)
        messages.success(request, 'Cadastro concluído! Agora você pode fazer login para começar.')
    return render(request, 'meu_app/cadastro.html')

# === QUESTIONÁRIO NUTRICIONAL ===
@login_required
def questionario_view(request):
    if request.method == 'POST':
        def parse_int(valor):
            try:
                return int(valor)
            except (TypeError, ValueError):
                return None

        dados = {
            'objetivo': request.POST.get('objetivo'),
            'restricoes': request.POST.get('restricoes') or '',
            'preferencia': request.POST.get('preferencia') or '',
            'refeicoes_por_dia': parse_int(request.POST.get('refeicoes_por_dia')),
            'sono': parse_int(request.POST.get('sono')),
            'atividade_fisica': request.POST.get('atividade_fisica'),
            'estresse': request.POST.get('estresse'),
            'come_carne': request.POST.get('come_carne'),
            'gosta_de_legumes': request.POST.get('gosta_de_legumes'),
            'usa_suplementos': request.POST.get('usa_suplementos'),
        }

        erros = {}
        campos_obrigatorios = [
            ('objetivo', 'O campo "Objetivo" é obrigatório.'),
            ('restricoes', 'O campo "Restrições" é obrigatório.'),
            ('preferencia', 'O campo "Preferências alimentares" é obrigatório.'),
            ('refeicoes_por_dia', 'O campo "Refeições por dia" é obrigatório.'),
            ('sono', 'O campo "Horas de sono" é obrigatório.'),
            ('atividade_fisica', 'O campo "Atividade física" é obrigatório.'),
            ('estresse', 'O campo "Nível de estresse" é obrigatório.'),
            ('come_carne', 'O campo "Consome carne" é obrigatório.'),
            ('gosta_de_legumes', 'O campo "Gosta de legumes" é obrigatório.'),
            ('usa_suplementos', 'O campo "Usa suplementos" é obrigatório.')
        ]
        for campo, mensagem in campos_obrigatorios:
            if not dados.get(campo):
                erros[campo] = mensagem

        if erros:
            return render(request, 'meu_app/questionario.html', {'erros': erros, 'dados': dados})

        # Conversão booleana após validação
        dados['come_carne'] = dados['come_carne'].lower() == 'sim'
        dados['gosta_de_legumes'] = dados['gosta_de_legumes'].lower() == 'sim'
        dados['usa_suplementos'] = dados['usa_suplementos'].lower() == 'sim'

        hoje = datetime.now().date()
        dados['ultima_modificacao'] = hoje
        dados['ultima_atualizacao'] = hoje

        Questionario.objects.update_or_create(
            usuario=request.user,
            defaults=dados
        )

        messages.success(request, 'Questionário enviado, verifique no seu perfil a aba Dieta/Cardápio.')
        return render(request, 'meu_app/questionario.html', {'dados': {}, 'erros': {}})

    # GET: sempre envie dados e erros vazios
    return render(request, 'meu_app/questionario.html', {'dados': {}, 'erros': {}})

# === AJUSTE DE SUBSTITUIÇÕES ===
def ajustar_substituicoes(cardapio, substituicoes):
    novo_cardapio = {}
    for refeicao, itens in cardapio.items():
        novos_itens = []
        for item in itens:
            for original, substituto in substituicoes.items():
                item = item.replace(original, substituto)
            novos_itens.append(item)
        novo_cardapio[refeicao] = novos_itens
    return novo_cardapio

# === GERADOR DE CARDÁPIO PERSONALIZADO ===
def gerar_cardapio_personalizado(dados):
    cardapio = {
        'Café da Manhã': [],
        'Almoço': [],
        'Lanche da Tarde': [],
        'Jantar': [],
    }

    objetivo = str(dados.get('objetivo', '')).lower()

    if 'ganhar' in objetivo:
        cardapio['Café da Manhã'].append("Ovos mexidos + pão integral + vitamina de banana com aveia")
        cardapio['Almoço'].append("Arroz integral + frango grelhado + legumes no vapor")
        cardapio['Lanche da Tarde'].append("Iogurte natural com granola")
        cardapio['Jantar'].append("Omelete com batata doce e salada")
    elif 'perder' in objetivo:
        cardapio['Café da Manhã'].append("Iogurte desnatado com frutas vermelhas")
        cardapio['Almoço'].append("Peito de frango + salada verde com azeite e quinoa")
        cardapio['Lanche da Tarde'].append("Castanhas e uma fruta")
        cardapio['Jantar'].append("Sopa de legumes com frango desfiado")
    elif 'saúde' in objetivo or 'saude' in objetivo:
        cardapio['Café da Manhã'].append("Pão integral com queijo branco + café sem açúcar")
        cardapio['Almoço'].append("Arroz + feijão + carne magra + salada")
        cardapio['Lanche da Tarde'].append("Fruta + iogurte")
        cardapio['Jantar'].append("Sanduíche natural + suco de frutas")
    else:
        for key in cardapio:
            cardapio[key].append("Sem cardápio definido para o objetivo informado.")

    preferencia = str(dados.get('preferencia', '')).lower()
    restricoes = str(dados.get('restricoes', '')).lower()
    come_carne = dados.get('come_carne', True)

    substituicoes = {}
    if 'atum' in preferencia:
        substituicoes['atum'] = 'frango'
    if 'gluten' in restricoes or 'glúten' in restricoes:
        substituicoes['pão integral'] = 'pão sem glúten integral'
        substituicoes['pão'] = 'pão sem glúten'
    if not come_carne:
        substituicoes['frango'] = 'seitan'
        substituicoes['carne'] = 'proteína vegetal'

    cardapio = ajustar_substituicoes(cardapio, substituicoes)

    perfil_desatualizado = False
    perfil_atualizado = False

    hoje = datetime.now().date()
    try:
        ultima_atualizacao_str = dados.get('ultima_atualizacao')
        ultima_modificacao_str = dados.get('ultima_modificacao')

        if ultima_atualizacao_str:
            if isinstance(ultima_atualizacao_str, datetime):
                ultima_atualizacao = ultima_atualizacao_str.date()
            else:
                ultima_atualizacao = datetime.strptime(str(ultima_atualizacao_str), '%Y-%m-%d').date()
            if (hoje - ultima_atualizacao) > timedelta(days=90):
                perfil_desatualizado = True

        if ultima_modificacao_str:
            if isinstance(ultima_modificacao_str, datetime):
                ultima_modificacao = ultima_modificacao_str.date()
            else:
                ultima_modificacao = datetime.strptime(str(ultima_modificacao_str), '%Y-%m-%d').date()
            if (hoje - ultima_modificacao) <= timedelta(days=2):
                perfil_atualizado = True

    except Exception:
        pass

    return {
        'cardapio': cardapio,
        'perfil_desatualizado': perfil_desatualizado,
        'perfil_atualizado': perfil_atualizado,
    }

# === CARDÁPIO PERSONALIZADO ===
@login_required
def cardapio_view(request):
    questionario = Questionario.objects.filter(usuario=request.user).last()
    if questionario:
        dados = {
            'objetivo': questionario.objetivo,
            'preferencia': questionario.preferencia,
            'restricoes': questionario.restricoes,
            'come_carne': questionario.come_carne,
            'ultima_atualizacao': questionario.ultima_atualizacao.strftime('%Y-%m-%d') if questionario.ultima_atualizacao else None,
            'ultima_modificacao': questionario.ultima_modificacao.strftime('%Y-%m-%d') if questionario.ultima_modificacao else None,
        }
        resultado = gerar_cardapio_personalizado(dados)
        return render(request, 'meu_app/cardapio.html', {
            'cardapio': resultado['cardapio'],
            'perfil_desatualizado': resultado['perfil_desatualizado'],
            'perfil_atualizado': resultado['perfil_atualizado'],
        })
    else:
        messages.error(request, '⚠️ Complete o questionário para ver seu cardápio.')
        return redirect('questionario')

# === PERFIL NUTRICIONAL ===
@login_required
def perfil_nutricional_view(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    questionario = Questionario.objects.filter(usuario=request.user).last()
    nome = perfil.nome if perfil and perfil.nome else request.user.username

    if questionario:
        dados = {
            'objetivo': questionario.objetivo,
            'preferencia': questionario.preferencia,
            'restricoes': questionario.restricoes,
            'come_carne': questionario.come_carne,
            'ultima_atualizacao': questionario.ultima_atualizacao.strftime('%Y-%m-%d') if questionario.ultima_atualizacao else None,
            'ultima_modificacao': questionario.ultima_modificacao.strftime('%Y-%m-%d') if questionario.ultima_modificacao else None,
        }
        cardapio = gerar_cardapio_personalizado(dados)
        return render(request, 'meu_app/perfil.html', {
            'questionario': questionario,
            'cardapio': cardapio,
            'usuario': request.user,
            'idade': getattr(questionario, 'idade', None),
            'nome': nome,
        })
    else:
        messages.error(request, 'Complete o questionário para ver seu perfil nutricional!')
        return render(request, 'meu_app/perfil.html', {
            'questionario': None,
            'usuario': request.user,
            'nome': nome,
        })

# === EDITAR PERFIL ===
@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    questionario = Questionario.objects.filter(usuario=request.user).last()

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        idade_str = request.POST.get('idade', '').strip()

        if not nome:
            messages.error(request, "O campo nome é obrigatório.")
            return render(request, 'meu_app/editar_perfil.html', {
                'perfil': perfil,
                'questionario': questionario,
                'dados': {},
                'erros': {},
            })

        if not idade_str:
            messages.error(request, "O campo idade é obrigatório.")
            return render(request, 'meu_app/editar_perfil.html', {
                'perfil': perfil,
                'questionario': questionario,
                'dados': {},
                'erros': {},
            })

        try:
            idade = int(idade_str)
            if idade <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Informe uma idade válida.")
            return render(request, 'meu_app/editar_perfil.html', {
                'perfil': perfil,
                'questionario': questionario,
                'dados': {},
                'erros': {},
            })

        perfil.nome = nome
        perfil.idade = idade
        perfil.save()

        if questionario:
            questionario.nome = nome
            questionario.idade = idade
            questionario.save()

        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil_nutricional')

    # GET: sempre envie dados e erros vazios
    return render(request, 'meu_app/editar_perfil.html', {
        'perfil': perfil,
        'questionario': questionario,
        'dados': {},
        'erros': {},
    })

# === EXCLUIR PERFIL ===
@login_required
def excluir_perfil(request):
    if request.method == 'POST':
        try:
            perfil = Perfil.objects.get(user=request.user)
            perfil.delete()
        except Perfil.DoesNotExist:
            pass
        try:
            questionario = Questionario.objects.get(usuario=request.user)
            questionario.delete()
        except Questionario.DoesNotExist:
            pass
        user = request.user
        user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('login')
    return render(request, 'meu_app/excluir_conta.html', {'dados': {}, 'erros': {}})

# === OUTRAS VIEWS ===
def receitas_view(request):
    return render(request, 'meu_app/receitas.html', {'dados': {}, 'erros': {}})

def agua_view(request):
    return render(request, 'meu_app/agua.html', {'dados': {}, 'erros': {}})

def dicas_nutricionais(request):
    return render(request, 'meu_app/dicas_nutricionais.html', {'dados': {}, 'erros': {}})

@login_required
def dadoscadastrais(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    questionario = Questionario.objects.filter(usuario=request.user).first()
    return render(request, 'meu_app/dados_cadastrais.html', {
        'perfil': perfil,
        'questionario': questionario,
        'dados': {},
        'erros': {},
    })

@login_required
def registrar_peso(request):
    if request.method == 'POST':
        form = RegistroPesoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user
            registro.save()
            messages.success(request, 'Peso registrado com sucesso!')
            return redirect('meu_app:registrar_peso')
    else:
        form = RegistroPesoForm()
    registros = RegistroPeso.objects.filter(usuario=request.user).order_by('-data')[:5]
    return render(request, 'meu_app/registrar_peso.html', {
        'form': form,
        'registros': registros,
        'dados': {},
        'erros': {},
    })

def ingestao_calorias(request):
    return render(request, 'meu_app/calorias.html', {'dados': {}, 'erros': {}})

# === LOGOUT ===
def logout_view(request):
    logout(request)
    return redirect('login')

# === REDIRECIONAMENTO PARA LOGIN ===
def redirecionar_para_login(request):
    return redirect('login')