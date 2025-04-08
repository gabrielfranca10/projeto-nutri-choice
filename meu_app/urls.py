from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirecionar_para_login, name='home'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('questionario/', views.questionario_view, name='questionario'),
    path('perfil/', views.perfil_nutricional_view, name='perfil_nutricional'),
    path('cardapio/', views.cardapio_view, name='cardapio_personalizado'),  # nova rota para cardápio
]
