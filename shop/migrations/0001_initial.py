# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-10 00:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import shop.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fake_id', models.CharField(default=uuid.UUID('3aa7d7e8-fbcc-11e8-bfb8-54e1adb1338e'), max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('tags', models.CharField(choices=[('clothes', '上衣'), ('shoes', '鞋子'), ('hat', '帽子'), ('trouser', '裤子'), ('underwear', '内衣')], max_length=12, null=True)),
                ('view', models.ImageField(blank=True, upload_to=shop.models.good_dictionary_path)),
                ('price', models.CharField(max_length=100)),
                ('stock', models.PositiveIntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('on_sale', models.BooleanField(default=False)),
                ('detail_information', models.TextField()),
                ('version_number', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good_owner', to='account.Seller')),
            ],
        ),
        migrations.CreateModel(
            name='NewestGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fake_id', models.CharField(max_length=100, verbose_name='商品编号')),
                ('name', models.CharField(max_length=50, verbose_name='商品名')),
                ('tags', models.CharField(choices=[('clothes', '上衣'), ('shoes', '鞋子'), ('hat', '帽子'), ('trouser', '裤子'), ('underwear', '内衣')], max_length=12, null=True, verbose_name='标签')),
                ('view', models.ImageField(blank=True, null=True, upload_to=shop.models.good_dictionary_path)),
                ('price', models.CharField(max_length=100, verbose_name='价格')),
                ('stock', models.PositiveIntegerField(verbose_name='库存')),
                ('on_sale', models.BooleanField(default=False, verbose_name='是否上架?')),
                ('detail_information', models.TextField(verbose_name='详细消息')),
                ('newest_version', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='account.Seller')),
                ('praise', models.ManyToManyField(related_name='good_praise', to='account.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='account.Customer')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good_cart', to='shop.Goods')),
            ],
        ),
    ]
