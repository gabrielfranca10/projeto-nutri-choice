# Generated by Django 5.2 on 2025-04-23 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_app', '0011_alter_questionario_agua_bebida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardapio',
            name='itens',
        ),
        migrations.AddField(
            model_name='cardapio',
            name='itens',
            field=models.ManyToManyField(blank=True, to='meu_app.alimento'),
        ),
    ]
