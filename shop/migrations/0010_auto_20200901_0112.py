# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-01 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20190226_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='stock',
            field=models.PositiveIntegerField(),
        ),
    ]