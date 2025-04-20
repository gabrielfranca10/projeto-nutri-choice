from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),  # Tela de cadastro
    path('questionario/', views.questionario_view, name='questionario'),  # Tela do questionário
    path('perfil/', views.perfil_nutricional_view, name='perfil_nutricional'),  # Tela de perfil
    path('cardapio/', views.cardapio_view, name='cardapio'),  # Tela de cardápio
    path('redirecionar-login/', views.redirecionar_para_login, name='redirecionar_login'),  # Página de login
]
