# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Value(models.Model):
    currency_name = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    quote = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Value'


class Cryptonews(models.Model):
    link = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateTimeField()
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cryptonews'


class CurrencyNews(models.Model):
    currency_name = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=500, blank=True, null=True)
    incontent = models.CharField(db_column='inContent', max_length=10)  # Field name made lowercase.
    intitle = models.CharField(db_column='inTitle', max_length=10)  # Field name made lowercase.
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'currency_news'


class DummyCryptonews(models.Model):
    link = models.CharField(max_length=500)
    content = models.TextField()
    date = models.DateTimeField()
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dummy_cryptonews'
