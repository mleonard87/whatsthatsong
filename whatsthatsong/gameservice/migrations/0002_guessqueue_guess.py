# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameservice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guessqueue',
            name='guess',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
