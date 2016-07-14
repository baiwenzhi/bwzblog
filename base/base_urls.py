# -*- coding: utf-8 -*-
from django.conf.urls import  url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', 'base.views.index'),
    url(r'^search/$', 'base.views.search'),
    url(r'^category/(?P<category_id>\d+)$', 'base.views.category'),
    url(r'^blog/(?P<blog_name>[^/]+)$', 'base.views.blog'),
    url(r'^fav/$', 'base.views.fav'),
    url(r'^timeline/$', 'base.views.timeline'),
    url(r'^sub_comment/$', 'base.views.sub_comment'),
    url(r'^tag/(?P<tag_id>\d+)$', 'base.views.tag'),
]