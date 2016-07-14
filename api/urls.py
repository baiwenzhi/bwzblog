# -*- coding: utf-8 -*-
from django.conf.urls import  url
from django.views.generic import TemplateView
from api import views

urlpatterns = [
    url(r'blogs$', views.BlogsView.as_view(), name='blog-list'),
    url(r'categorys$', views.CategoryView.as_view(), name='category-list'),
    url(r'blog/(?P<blog_name>[^/]+)$',views.BlogView.as_view(),name='base.views.blog'),
    url(r'category/(?P<category_id>\d+)$',views.CategoryBlogView.as_view(),name='base.views.category'),
    url(r'fav$', views.FavView.as_view(), name='fav'),
    url(r'timeline$', views.TimeLine.as_view(), name='fav'),
    url(r'search', views.SearchView.as_view(), name='search'),
    url(r'tag/(?P<tag_id>\d+)$',views.TagBlogsView.as_view(),name='base.views.tag'),
]