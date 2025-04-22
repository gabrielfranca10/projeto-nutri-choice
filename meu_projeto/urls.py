from django.contrib import admin
from django.urls import path
from meu_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirecionar_para_login),  # URL raiz, redireciona para o login
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('questionario/', views.questionario_view, name='questionario'),
    path('perfil/', views.perfil_nutricional_view, name='perfil_nutricional'),
    path('logout/', views.logout_view, name='logout'),  # Adicionando a URL para o logout
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('excluir-perfil/', views.excluir_perfil, name='excluir_perfil'),
    path('substituicoes/', views.substituicoes_view, name='substituicoes'),
    path('adicionar_cardapio/', views.adicionar_cardapio, name='adicionar_cardapio'),

]