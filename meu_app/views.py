from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Alimento, Substituicao, Questionario
from django.http import HttpResponse
from .models import Perfil, Questionario

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

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return render(request, 'meu_app/cadastro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Login automático (opcional: remova se quiser que o usuário vá para login primeiro)
        login(request, user)

        messages.success(request, 'Cadastro concluído! Faça login para começar.')
        return redirect('login')

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
            'idade': parse_int(request.POST.get('idade')) or '',
            'objetivo': request.POST.get('objetivo'),
            'restricoes': request.POST.get('restricoes') or '',
            'preferencia': request.POST.get('preferencia') or '',
            'fome': request.POST.get('fome') or '',
            'refeicoes_por_dia': request.POST.get('refeicoes_por_dia'),
            'come_carne': request.POST.get('come_carne') == 'on',
            'gosta_de_legumes': request.POST.get('gosta_de_legumes') == 'on',
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
        return render(request, 'meu_app/perfil.html', {'cardapio': cardapio, 'dados': dados})

    return render(request, 'meu_app/questionario.html')

# === GERADOR DE CARDÁPIO ===
def ajustar_substituicoes(cardapio, substituicoes):
    for key in cardapio:
        for original, novo in substituicoes.items():
            cardapio[key] = [item.replace(original, novo) for item in cardapio[key]]
    return cardapio

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
        # Se objetivo não for reconhecido, preenche algo básico para não quebrar o site
        for key in cardapio:
            cardapio[key].append("Sem cardápio definido para o objetivo informado.")

    # Ajustes conforme preferências e restrições
    preferencia = str(dados.get('preferencia', '')).lower()
    restricoes = str(dados.get('restricoes', '')).lower()
    come_carne = dados.get('come_carne', True)

    # Dicionários de substituições
    substituicoes = {}
    if 'atum' in preferencia:
        substituicoes['atum'] = 'frango'
    if 'gluten' in restricoes or 'glúten' in restricoes:
        substituicoes['pão integral'] = 'pão sem glúten integral'
        substituicoes['pão'] = 'pão sem glúten'
    if not come_carne:
        substituicoes['frango'] = 'seitan'

    # Aplicando as substituições
    cardapio = ajustar_substituicoes(cardapio, substituicoes)

    return cardapio

def exibir_cardapio(cardapio):
    # Gerar o conteúdo HTML para exibir o cardápio
    cardapio_html = ""
    for refeicao, itens in cardapio.items():
        cardapio_html += f"<h3>{refeicao}:</h3>"
        cardapio_html += "<ul>"
        for item in itens:
            cardapio_html += f"<li>{item}</li>"
        cardapio_html += "</ul>"
    return cardapio_html

def questionario(request):
    if request.method == 'POST':
        dados = {
            'objetivo': request.POST.get('objetivo', '').strip(),
            'refeicoes_por_dia': request.POST.get('refeicoes_por_dia', '').strip(),
            'atividade_fisica': request.POST.get('atividade_fisica', '').strip(),
            'estresse': request.POST.get('estresse', '').strip(),
        }

        # Verificar campos obrigatórios
        campos_obrigatorios = ['objetivo', 'refeicoes_por_dia', 'atividade_fisica', 'estresse']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                messages.error(request, 'Preencha todos os campos obrigatórios.')
                return render(request, 'meu_app/questionario.html')

        # Validar objetivo
        objetivo = dados['objetivo'].lower()
        if objetivo not in ['ganhar massa', 'perder peso', 'melhorar saúde', 'saúde']:
            messages.error(request, 'Selecione um objetivo válido para gerar seu cardápio.')
            return render(request, 'meu_app/questionario.html')

        # Agora sim gerar o cardápio
        cardapio = gerar_cardapio_personalizado(dados)

        # Verifica se o cardápio gerado tem conteúdo
        if not cardapio:
            messages.error(request, 'Não conseguimos montar seu cardápio. Tente preencher novamente.')
            return render(request, 'meu_app/questionario.html')

        return render(request, 'meu_app/perfil.html', {'cardapio': cardapio})

    return render(request, 'meu_app/questionario.html')

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
            'cardapio': cardapio,
            'usuario': request.user,
            'idade': ultimo.idade,
            'nome': ultimo.nome,
        })
    else:
        messages.error(request, 'Complete o questionário para ver seu perfil nutricional!')
        return render(request, 'meu_app/perfil.html')

# === CARDÁPIO PERSONALIZADO ===
@login_required
def cardapio_view(request):
    questionario = Questionario.objects.filter(usuario=request.user).last()
    if questionario:
        dados = vars(questionario)
        cardapio = gerar_cardapio_personalizado(dados)
        return render(request, 'meu_app/cardapio.html', {'cardapio': cardapio})
    else:
        messages.error(request, 'Complete o questionário para ver seu cardápio.')
        return redirect('cardapio')  # ou onde preferir


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
    try:
        # Obtém o questionário do usuário logado
        questionario = Questionario.objects.get(usuario=request.user)
    except Questionario.DoesNotExist:
        messages.error(request, "Questionário não encontrado. Tente novamente.")
        return redirect('perfil_nutricional')  # Redireciona caso não exista o questionário

    if request.method == 'POST':
        # Converte os valores do POST para os tipos apropriados, com tratamento de exceção para float e int
        questionario.nome = request.POST.get('nome', questionario.nome)
        questionario.idade = int(request.POST.get('idade', questionario.idade) or questionario.idade)
        questionario.objetivo = request.POST.get('objetivo', questionario.objetivo)
        questionario.restricoes = request.POST.get('restricoes', questionario.restricoes)
        questionario.preferencia = request.POST.get('preferencia', questionario.preferencia)
        questionario.fome = request.POST.get('fome', questionario.fome)
        questionario.refeicoes_por_dia = int(request.POST.get('refeicoes_por_dia', questionario.refeicoes_por_dia) or questionario.refeicoes_por_dia)

        # Conversão para booleano
        questionario.come_carne = request.POST.get('come_carne') == 'on'
        questionario.gosta_de_legumes = request.POST.get('gosta_de_legumes') == 'on'
        
        # Tratamento do valor de 'agua_bebida' para float
        questionario.sono = request.POST.get('sono', questionario.sono)
        questionario.atividade_fisica = request.POST.get('atividade_fisica', questionario.atividade_fisica)
        
        # Conversão para booleano
        questionario.usa_suplementos = request.POST.get('usa_suplementos') == 'on'
        questionario.estresse = request.POST.get('estresse', questionario.estresse)

        # Salva as alterações no questionário
        questionario.save()

        # Mensagem de sucesso
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil_nutricional')

    # Caso o método seja GET, renderiza a página de edição com os dados do questionário
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

def receitas_view(request):
    return render(request, 'meu_app/receitas.html')
# views.py
def agua_view(request):
    return render(request, 'meu_app/agua.html')  # Ajuste conforme necessário

def dicas_nutricionais(request):
    return render(request, 'meu_app/dicas_nutricionais.html')

@login_required
def dadoscadastrais(request):
    questionario = Questionario.objects.filter(usuario=request.user).first()

    if not questionario:
        messages.error(request, 'Complete o questionário para visualizar os dados cadastrais.')
        return redirect('perfil_nutricional')

    return render(request, 'meu_app/dados_cadastrais.html', {'questionario': questionario})
