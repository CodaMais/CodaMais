# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 13:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20170421_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recoverpasswordprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2017, 4, 23)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2017, 4, 23)),
        ),
    ]
