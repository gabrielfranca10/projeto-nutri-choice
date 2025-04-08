from django.contrib import admin
from django.urls import path
from meu_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirecionar_para_login),  # 👈 URL raiz
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('questionario/', views.questionario_view, name='questionario'),
    path('perfil/', views.perfil_nutricional_view, name='perfil_nutricional'),
]
