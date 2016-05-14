# coding=utf-8
from django.contrib import admin
from analysis.models import  VisitCount


class vs_VisitCount(admin.ModelAdmin):
    list_display = ('createdate','count')

admin.site.register(VisitCount,vs_VisitCount)