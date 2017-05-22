# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 22:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('description', models.CharField(max_length=100)),
                ('achievement_type', models.PositiveIntegerField(choices=[(1, 'Exercício Correto'), (2, 'Resposta no Fórum'), (3, 'Pontuação do Usuário'), (4, 'Submissão de Exercícios')])),
                ('quantity', models.PositiveIntegerField()),
                ('achievement_icon', models.ImageField(default='Trophy-96.png', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='achievement.Achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userachievement',
            unique_together=set([('user', 'achievement')]),
        ),
    ]
