# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-13 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20181211_1418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AlterModelOptions(
            name='seller',
            options={'verbose_name': '商家', 'verbose_name_plural': '商家'},
        ),
        migrations.AlterModelOptions(
            name='userall',
            options={'verbose_name': '所有用户', 'verbose_name_plural': '所有用户'},
        ),
        migrations.AlterField(
            model_name='customer',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.UserAll', verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.UserAll', verbose_name='商家'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='store_status',
            field=models.BooleanField(default=True, verbose_name='商店状态'),
        ),
    ]
