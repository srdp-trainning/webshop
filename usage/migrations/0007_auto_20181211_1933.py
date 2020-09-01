# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-11 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0006_auto_20181211_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(default='9cfb6289efea416e8814f61685bda0a6', max_length=50, verbose_name='单号'),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(default=1, verbose_name='购买个数'),
        ),
    ]