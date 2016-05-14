# coding=utf-8
from django.db import models

# Create your models here.

class VisitCount(models.Model):
    createdate = models.DateField(auto_now_add=True,primary_key=True)
    count = models.IntegerField(verbose_name='点击次数',default=0)

    class Meta:
        verbose_name = '网站点击'
        verbose_name_plural = '网站点击'
        ordering = ['-createdate']

class VisitCountHour(models.Model):
    create_time = models.DateTimeField()
    count = models.IntegerField(verbose_name='点击次数',default=0)

    class Meta:
        verbose_name = '网站点击(小时)'
        verbose_name_plural = '网站点击(小时)'
        ordering = ['-create_time']