# Generated by Django 5.2 on 2025-04-23 22:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_app', '0012_remove_cardapio_itens_cardapio_itens'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alimento',
            options={'verbose_name': 'Alimento', 'verbose_name_plural': 'Alimentos'},
        ),
        migrations.AlterModelOptions(
            name='cardapio',
            options={'verbose_name': 'Cardápio', 'verbose_name_plural': 'Cardápios'},
        ),
        migrations.AlterModelOptions(
            name='questionario',
            options={'verbose_name': 'Questionário', 'verbose_name_plural': 'Questionários'},
        ),
        migrations.AlterModelOptions(
            name='substituicao',
            options={'verbose_name': 'Substituição', 'verbose_name_plural': 'Substituições'},
        ),
        migrations.AlterField(
            model_name='questionario',
            name='refeicoes_por_dia',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
