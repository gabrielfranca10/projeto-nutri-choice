# Generated by Django 5.2 on 2025-04-27 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meu_app', '0023_questionario_atividade_fisica_questionario_fome_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionario',
            old_name='agua_bebida',
            new_name='agua',
        ),
    ]
