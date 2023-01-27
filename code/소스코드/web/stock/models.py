# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


''' # accounts.models 로 이전
class Macroeconomicindicators(models.Model):
    data_time = models.DateField(blank=True, null=True)
    kospi = models.FloatField(blank=True, null=True)
    america_top_500 = models.FloatField(blank=True, null=True)
    gold = models.FloatField(blank=True, null=True)
    copper = models.FloatField(blank=True, null=True)
    k_gov3 = models.FloatField(blank=True, null=True)
    usd_k = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'macroeconomicindicators'


class Stockcode(models.Model):
    stock_code = models.CharField(primary_key=True, max_length=7)
    stock_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stockcode'


class Stockdata(models.Model):
    stock_code = models.ForeignKey(Stockcode, models.CASCADE, db_column='stock_code', blank=True, null=True)
    data_time = models.DateField(blank=True, null=True)
    start_open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    end_close = models.FloatField(blank=True, null=True)
    trading_volume = models.FloatField(blank=True, null=True)
    transaction_amount = models.FloatField(blank=True, null=True)
    end_rate_change = models.FloatField(blank=True, null=True)
    institutional_total = models.FloatField(blank=True, null=True)
    other_corporations = models.FloatField(blank=True, null=True)
    individual = models.FloatField(blank=True, null=True)
    foreigner_total = models.FloatField(blank=True, null=True)
    short_selling = models.FloatField(blank=True, null=True)
    short_buying = models.FloatField(blank=True, null=True)
    short_importance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stockdata'


class Userdata(models.Model):
    userid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    experience = models.CharField(max_length=20, blank=True, null=True)
    now_money = models.BigIntegerField(blank=True, null=True)
    total_money = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userdata'


class Userstock(models.Model):
    userid = models.ForeignKey(Userdata, models.CASCADE, db_column='userid', blank=True, null=True)
    stock_code = models.ForeignKey(Stockcode, models.CASCADE, db_column='stock_code', blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userstock'
'''