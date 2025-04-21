from django.urls import path
from . import views
from .views import substituicoes_view


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('questionario/', views.questionario_view, name='questionario'),
    path('perfil/', views.perfil_nutricional_view, name='perfil_nutricional'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('excluir-perfil/', views.excluir_perfil, name='excluir_perfil'),
    path('logout/', views.logout_view, name='logout'),
    path('substituicoes/', views.substituicoes_view, name='substituicoes')

]
