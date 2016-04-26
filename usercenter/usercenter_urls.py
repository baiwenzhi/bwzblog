# -*- coding: utf-8 -*-
from django.conf.urls import  patterns,url

urlpatterns = [
    url(r'^usercenter/usersetting/$', 'usercenter.views.usersetting'),
    url(r'^usercenter/categorys/$', 'usercenter.views.categorys'),
    url(r'^usercenter/blogs/$', 'usercenter.views.blogs'),
    url(r'^usercenter/write_blog/$', 'usercenter.views.write_blog'),
    url(r'^usercenter/add_category/$', 'usercenter.views.add_category'),
    url(r'^usercenter/del_category/$', 'usercenter.views.del_category'),
    url(r'^usercenter/delete_blog/$', 'usercenter.views.delete_blog'),
    url(r'^usercenter/user_list/$', 'usercenter.views.user_list'),
    url(r'^usercenter/delete_user/$', 'usercenter.views.delete_user'),
    url(r'^usercenter/comments/$', 'usercenter.views.comments'),
    url(r'^usercenter/del_comment/$', 'usercenter.views.del_comment'),
    url(r'^usercenter/save_logo/$', 'usercenter.views.save_logo'),
    url(r'^usercenter/save_blog_name/$', 'usercenter.views.save_blog_name'),
    url(r'^usercenter/visit/$', 'usercenter.views.visit'),
    url(r'^mycenter/$', 'usercenter.views.mycenter'),
    url(r'^fav_blog/$', 'usercenter.views.fav_blog'),
]
