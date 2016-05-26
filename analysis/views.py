# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from analysis.models import VisitCount, VisitCountHour
import pylibmc as memcache
import datetime
from django.db.models import Sum

def cron_analysis_day(request):

    today = datetime.date.today()
    count = VisitCountHour.objects.filter(create_time__gt = today).aggregate(Sum('count'))
    vc = VisitCount.objects.filter(createdate=today)
    if vc:
        vc[0].count = count.get('count__sum') or 0
        vc[0].save()
    else:
        VisitCount.objects.create(count = count.get('count__sum') or 0)
    return HttpResponse('success %s'%count)

def cron_analysis_hour(request):

    mc = memcache.Client('127.0.0.1')
    count = mc.get('visit_count')
    now = datetime.datetime.now()
    dtstr = "%s-%s-%s %s:00:00"%(now.year,now.month,now.day,now.hour)
    add_time = datetime.datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")
    vc = VisitCountHour.objects.filter(create_time=add_time)
    if vc:
        vc[0].count = vc[0].count+count
        vc[0].save()
    else:
        VisitCountHour.objects.create(count = count,create_time = add_time)
    mc.set('visit_count',0)
    return HttpResponse('%s:success,%s'%(add_time,count))
