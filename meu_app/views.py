from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CadastroForm, PerfilForm, QuestionarioForm
from .models import PerfilNutricional, Questionario
from django.contrib import messages

# Cadastro + Perfil
def register(request):
    if request.method == 'POST':
        form_user = CadastroForm(request.POST)
        form_perfil = PerfilForm(request.POST)
        if form_user.is_valid() and form_perfil.is_valid():
            user = form_user.save()
            perfil = form_perfil.save(commit=False)
            perfil.user = user
            perfil.save()
            login(request, user)
            return redirect('questionario')
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form_user = CadastroForm()
        form_perfil = PerfilForm()

    return render(request, 'meu_app/cadastro.html', {
        'form_user': form_user,
        'form_perfil': form_perfil,
    })

# Visualizar Perfil
@login_required
def perfil_view(request):
    try:
        perfil = PerfilNutricional.objects.get(user=request.user)
    except PerfilNutricional.DoesNotExist:
        messages.warning(request, "Você ainda não criou seu perfil nutricional.")
        return redirect('register')
    
    return render(request, 'meu_app/perfil.html', {'perfil': perfil})

# Preenchimento do Questionário
@login_required
def questionario_view(request):
    if request.method == 'POST':
        form = QuestionarioForm(request.POST)
        if form.is_valid():
            questionario = form.save(commit=False)
            questionario.user = request.user
            questionario.save()
            return redirect('confirmacao_questionario')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = QuestionarioForm()
    
    return render(request, 'meu_app/questionario.html', {'form': form})

# Confirmação após envio do questionário
@login_required
def confirmacao_questionario(request):
    return render(request, 'meu_app/confirmacao.html')

# Exibir cardápio personalizado
@login_required
def cardapio_view(request):
    perfil = get_object_or_404(PerfilNutricional, user=request.user)
    questionario = get_object_or_404(Questionario, user=request.user)

    # Lógica básica personalizada
    sugestoes = []

    if perfil.objetivo == 'ganhar':
        sugestoes.append("Café da manhã: Omelete com aveia e banana")
        sugestoes.append("Almoço: Arroz integral, frango grelhado, legumes")
        sugestoes.append("Lanche: Shake de proteína com pasta de amendoim")
        sugestoes.append("Jantar: Macarrão integral com carne moída e salada")
    elif perfil.objetivo == 'perder':
        sugestoes.append("Café da manhã: Iogurte natural com frutas")
        sugestoes.append("Almoço: Salada com frango grelhado e batata doce")
        sugestoes.append("Lanche: Mix de castanhas")
        sugestoes.append("Jantar: Sopa de legumes")
    else:
        sugestoes.append("Café da manhã: Pão integral com ovo")
        sugestoes.append("Almoço: Arroz, feijão, carne magra e salada")
        sugestoes.append("Lanche: Frutas")
        sugestoes.append("Jantar: Omelete leve com legumes")

    if not questionario.come_carne:
        sugestoes = [s.replace("frango", "tofu").replace("carne", "lentilha") for s in sugestoes]

    if not questionario.gosta_de_legumes:
        sugestoes = [s.replace("legumes", "outros vegetais") for s in sugestoes]

    # Preparar para exibição no template
    cardapio_formatado = []
    for s in sugestoes:
        if ":" in s:
            tipo, descricao = s.split(":", 1)
            cardapio_formatado.append({
                'refeicao': tipo.strip(),
                'descricao': descricao.strip()
            })
        else:
            cardapio_formatado.append({
                'refeicao': 'Refeição',
                'descricao': s
            })

    return render(request, 'meu_app/cardapio.html', {
        'cardapio': cardapio_formatado
    })
