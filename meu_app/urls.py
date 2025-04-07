from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(template_name='meu_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('cadastro/', views.register, name='cadastro'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('questionario/', views.questionario_view, name='questionario'),
    path('cardapio/', views.cardapio_view, name='cardapio'),
]
