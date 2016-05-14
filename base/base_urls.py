# -*- coding: utf-8 -*-
from django.conf.urls import  url
from django.views.generic import TemplateView

urlpatterns = [
    #url(r'^robots\.txt$', TemplateView.as_view(template_name="../robots.txt",content_type='text/plain; charset=UTF-8')),
    url(r'^get_background/$', 'base.views.get_background'),
    url(r'^change_pwd/$', 'base.views.change_pwd'),
    url(r'^login/$', 'base.views.login'),
    url(r'^findpwd/$', 'base.views.findpwd'),
    url(r'^search/$', 'base.views.search'),
    url(r'^base/photo_upload/$', 'base.views.photo_upload'),
    url(r'^logout/$', 'base.views.logout'),
    url(r'^category/(?P<category_id>\d+)/$', 'base.views.category'),
    url(r'^edit/$', 'base.views.edit'),
    url(r'^blog/(?P<blog_name>[^/]+)$', 'base.views.blog'),
    url(r'^fav/$', 'base.views.fav'),
    url(r'^timeline/$', 'base.views.timeline'),
    url(r'^sub_comment/$', 'base.views.sub_comment'),
]