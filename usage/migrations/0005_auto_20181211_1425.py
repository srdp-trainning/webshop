# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-11 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0004_auto_20181211_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(default='9b9ef7f0fd0d11e8a02954e1adb1338e', max_length=50, verbose_name='单号'),
        ),
    ]
