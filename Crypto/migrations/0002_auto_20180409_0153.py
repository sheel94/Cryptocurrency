# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-09 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crypto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptonews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
                ('timestamp', models.DateTimeField()),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'cryptonews',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CurrencyNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=500)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('incontent', models.CharField(db_column='inContent', max_length=10)),
                ('intitle', models.CharField(db_column='inTitle', max_length=10)),
                ('date', models.DateTimeField()),
            ],
            options={
                'db_table': 'currency_news',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DummyCryptonews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
                ('timestamp', models.DateTimeField()),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'dummy_cryptonews',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('quote', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Value',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Visit',
        ),
    ]
