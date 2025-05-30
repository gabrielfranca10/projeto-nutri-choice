# Generated by Django 5.2 on 2025-04-20 19:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meu_app', '0005_alter_questionario_agua_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='questionario',
            name='altura',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionario',
            name='peso',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionario',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]