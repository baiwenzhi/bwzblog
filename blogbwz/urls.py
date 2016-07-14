# -*- coding: utf-8 -*-
"""blogbwz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:

Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from base.models import Blog

sitemaps = {
    'blog': GenericSitemap({'queryset': Blog.objects.all(), 'date_field': 'create_time'}, priority=0.6),
    # 如果还要加其它的可以模仿上面的
}
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^cron_analysis_day/$', 'analysis.views.cron_analysis_day'),
    url(r'^cron_analysis_hour/$', 'analysis.views.cron_analysis_hour'),
    url(r'^', include('web.urls')),
    url(r'^', include('usercenter.usercenter_urls')),
    url(r'api/', include('api.urls')),
    url(r'^get_background/$', 'base.views.get_background'),
    url(r'^change_pwd/$', 'base.views.change_pwd'),
    url(r'^login/$', 'base.views.login'),
    url(r'^findpwd/$', 'base.views.findpwd'),
    url(r'^base/photo_upload/$', 'base.views.photo_upload'),
    url(r'^logout/$', 'base.views.logout'),
    url(r'^return$','base.views.return_comment'),
)
