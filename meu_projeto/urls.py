from django.contrib import admin
from django.urls import path, include
from meu_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('meu_app.urls', 'meu_app'), namespace='meu_app')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirecionar_para_login),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('questionario/', views.questionario_view, name='questionario'),
    path('perfil/', views.perfil_nutricional_view, name='perfil_nutricional'),
    path('logout/', views.logout_view, name='logout'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('excluir-perfil/', views.excluir_perfil, name='excluir_perfil'),
    path('receitas/', views.receitas_view, name='receitas'),  # <-- esta linha resolve o erro
    path('agua/', views.agua_view, name='agua'),
    path('cardapio/', views.cardapio_view, name='cardapio'),
    path('dicas-nutricionais/', views.dicas_nutricionais, name='dicas_nutricionais'),
    path('dados/', views.dadoscadastrais, name='dados'),
    path('admin/', admin.site.urls),
    path('', include(('meu_app.urls', 'meu_app'), namespace='meu_app')),
]