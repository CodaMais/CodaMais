# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-01 00:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20170430_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='scored',
            field=models.IntegerField(default=0),
        ),
    ]