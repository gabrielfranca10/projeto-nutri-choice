from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Alimento, Substituicao, Questionario, Cardapio
from django.http import HttpResponse
from .models import Perfil, Questionario
from datetime import datetime
from .services import gerar_cardapio_personalizado


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

def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        password2 = request.POST.get('confirmar_senha')
        data_nascimento = request.POST.get('data_nascimento')
        genero = request.POST.get('genero')
        endereco = request.POST.get('endereco')

        if not all([username, email, password, password2, data_nascimento, genero, endereco]):
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

        try:
            nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
            hoje = datetime.today()
            idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        except ValueError:
            messages.error(request, 'Data de nascimento inválida.')
            return render(request, 'meu_app/cadastro.html')

        # Criação do usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Criação do perfil completo
        Perfil.objects.create(
            user=user,
            nome=username,
            idade=idade,
            data_nascimento=nascimento,
            genero=genero,
            endereco=endereco,
            peso=None,
            altura=None,
            objetivo='',
            restricoes='',
            preferencia='',
        )

        messages.success(request, 'Cadastro concluído! Faça login para começar.')
        return redirect('login')

    return render(request, 'meu_app/cadastro.html')


# === QUESTIONÁRIO NUTRICIONAL ===
@login_required
def questionario_view(request):
    if request.method == 'POST':
        # Funções auxiliares para parse de valores
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

        # Coletando dados do formulário
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
            'refeicoes_por_dia': parse_int(request.POST.get('refeicoes_por_dia')),
            'come_carne': request.POST.get('come_carne') == 'on',
            'gosta_de_legumes': request.POST.get('gosta_de_legumes') == 'on',
            'agua_bebida': parse_float(request.POST.get('agua_bebida')),  
            'sono': request.POST.get('sono') or '',
            'atividade_fisica': request.POST.get('atividade_fisica'),
            'usa_suplementos': request.POST.get('usa_suplementos') == 'on',
            'estresse': request.POST.get('estresse'),
        }

        # Campos obrigatórios
        campos_obrigatorios = ['objetivo', 'refeicoes_por_dia', 'atividade_fisica', 'estresse']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                messages.error(request, 'Preencha todos os campos obrigatórios')
                return render(request, 'meu_app/questionario.html')

        # Atualizando ou criando o Questionário
        questionario, created = Questionario.objects.update_or_create(
            usuario=request.user,
            defaults=dados
        )

        # Atualizando ou criando o Perfil
        perfil_data = {
            'nome': dados['nome'] or request.user.username,
            'idade': dados['idade'],
            'peso': dados['peso'],
            'altura': dados['altura'],
            'objetivo': dados['objetivo'],
            'restricoes': dados['restricoes'],
            'preferencia': dados['preferencia']
        }
        perfil, perfil_created = Perfil.objects.update_or_create(
            user=request.user,
            defaults=perfil_data
        )

        # Gerar cardápio personalizado (função que você já tem)
        descricao_cardapio = gerar_cardapio_personalizado(dados)

        # Salvar o cardápio no banco
        Cardapio.objects.create(
            usuario=request.user,
            descricao=descricao_cardapio
        )

        # Mensagem de sucesso
        messages.success(request, "Questionário respondido com sucesso! ✅ Seu cardápio já está disponível na aba Dieta/Cardápio.")

        # Redirecionar para o perfil
        return redirect('perfil_nutricional')  # ajuste o nome da URL se necessário

    return render(request, 'meu_app/questionario.html') 

def gerar_cardapio_personalizado(dados):
    cardapio = {
        'Café da Manhã': [],
        'Almoço': [],
        'Lanche da Tarde': [],
        'Jantar': [],
    }

    objetivo = dados.get('objetivo', '').lower()
    preferencias = dados.get('preferencia', '').lower()
    restricoes = dados.get('restricoes', '').lower()

    gosta_de_carne = dados.get('gosta_de_carne', True)
    gosta_de_legumes = dados.get('gosta_de_legumes', True)
    come_carne = dados.get('come_carne', True)

    def substituir_almoco_e_jantar(almoco_opcao, jantar_opcao):
        if not gosta_de_carne or not come_carne:
            almoco_opcao = almoco_opcao.replace('frango', 'grão-de-bico').replace('carne', 'soja texturizada').replace('peito de frango', 'lentilhas').replace('carne magra', 'tofu grelhado')
            jantar_opcao = jantar_opcao.replace('frango', 'grão-de-bico').replace('carne', 'soja texturizada').replace('peito de frango', 'lentilhas').replace('carne magra', 'tofu grelhado')
        if not gosta_de_legumes:
            # Substituir legumes/salada por arroz, purê, ou outra alternativa viável
            almoco_opcao = almoco_opcao.replace('legumes no vapor', 'purê de batata').replace('salada verde', 'arroz integral').replace('salada', 'arroz e feijão')
            jantar_opcao = jantar_opcao.replace('salada', 'quinoa refogada').replace('sopa de legumes', 'creme de abóbora').replace('legumes', 'arroz com ovo')
        return almoco_opcao, jantar_opcao

    # CAFÉ DA MANHÃ E LANCHE
    if 'ganhar' in objetivo:
        cardapio['Café da Manhã'].append("Ovos mexidos + pão integral + vitamina de banana com aveia")
        cardapio['Lanche da Tarde'].append("Iogurte natural com granola")
        almoco, jantar = substituir_almoco_e_jantar(
            "Arroz integral + frango grelhado + legumes no vapor",
            "Omelete com batata doce e salada"
        )
    elif 'perder' in objetivo:
        cardapio['Café da Manhã'].append("Iogurte desnatado + frutas vermelhas")
        cardapio['Lanche da Tarde'].append("Castanhas e uma fruta")
        almoco, jantar = substituir_almoco_e_jantar(
            "Peito de frango + salada verde com azeite e quinoa",
            "Sopa de legumes com frango desfiado"
        )
    elif 'saúde' in objetivo or 'saude' in objetivo:
        cardapio['Café da Manhã'].append("Pão integral com queijo branco + café sem açúcar")
        cardapio['Lanche da Tarde'].append("Fruta + iogurte")
        almoco, jantar = substituir_almoco_e_jantar(
            "Arroz + feijão + carne magra + salada",
            "Sanduíche natural + suco de frutas"
        )
    else:
        almoco, jantar = "Arroz + feijão + ovo cozido", "Sopa de abóbora com torradas"

    cardapio['Almoço'].append(almoco)
    cardapio['Jantar'].append(jantar)

    # Preferência por atum
    if 'atum' in preferencias:
        for key in cardapio:
            cardapio[key] = [item.replace('atum', 'frango') for item in cardapio[key]]

    # Restrições ao glúten
    if 'glúten' in restricoes or 'gluten' in restricoes:
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
def cardapio_view(request):
    try:
        # Tenta pegar o último cardápio criado pelo usuário
        cardapio = Cardapio.objects.filter(usuario=request.user).latest('id')
    except Cardapio.DoesNotExist:
        cardapio = None

    return render(request, 'meu_app/cardapio.html', {'cardapio': cardapio})

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
        questionario.peso = float(request.POST.get('peso', questionario.peso) or questionario.peso)
        questionario.altura = float(request.POST.get('altura', questionario.altura) or questionario.altura)
        questionario.genero = request.POST.get('genero', questionario.genero)
        questionario.objetivo = request.POST.get('objetivo', questionario.objetivo)
        questionario.restricoes = request.POST.get('restricoes', questionario.restricoes)
        questionario.preferencia = request.POST.get('preferencia', questionario.preferencia)
        questionario.fome = request.POST.get('fome', questionario.fome)
        questionario.refeicoes_por_dia = int(request.POST.get('refeicoes_por_dia', questionario.refeicoes_por_dia) or questionario.refeicoes_por_dia)

        # Conversão para booleano
        questionario.come_carne = request.POST.get('come_carne') == 'on'
        questionario.gosta_de_legumes = request.POST.get('gosta_de_legumes') == 'on'
        
        # Tratamento do valor de 'agua_bebida' para float
        try:
            questionario.agua_bebida = float(request.POST.get('agua_bebida', 0))
        except ValueError:
            questionario.agua_bebida = 0  # Valor padrão caso a conversão falhe

        # Mantém os valores default caso não seja passado
        questionario.agua_bebida = request.POST.get('agua_bebida', questionario.agua_bebida)
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

def receitas_view(request):
    return render(request, 'meu_app/receitas.html')
# views.py
def agua_view(request):
    return render(request, 'meu_app/agua.html')  # Ajuste conforme necessário

def dicas_nutricionais(request):
    return render(request, 'meu_app/dicas_nutricionais.html')

@login_required
def dadoscadastrais(request):
    # Recupera o questionário do usuário logado, se existir
    questionario = Questionario.objects.filter(usuario=request.user).first()

    if questionario:
        dados = {
            'nome': questionario.nome,
            'idade': questionario.idade,
            'peso': questionario.peso,
            'altura': questionario.altura,
            'genero': questionario.genero,
            'objetivo': questionario.objetivo,
            'restricoes': questionario.restricoes,
            'preferencia': questionario.preferencia,
            'fome': questionario.fome,
            'refeicoes_por_dia': questionario.refeicoes_por_dia,
            'come_carne': questionario.come_carne,
            'gosta_de_legumes': questionario.gosta_de_legumes,
            'agua_bebida': questionario.agua_bebida,
            'sono': questionario.sono,
            'atividade_fisica': questionario.atividade_fisica,
            'usa_suplementos': questionario.usa_suplementos,
            'estresse': questionario.estresse,
        }
    else:
        dados = {}

    return render(request, 'meu_app/dados_cadastrais.html', {'dados': dados, 'questionario': questionario})