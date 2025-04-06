from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('meu_app.urls')),  # redireciona para as URLs do app principal
]
