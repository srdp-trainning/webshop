# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-10 00:11
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20181210_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='fake_id',
            field=models.CharField(default=uuid.UUID('052b7a64-fbcd-11e8-ad5c-54e1adb1338e'), max_length=100),
        ),
    ]