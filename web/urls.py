# -*- coding: utf-8 -*-
from django.conf.urls import  url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', 'web.views.index'),
]