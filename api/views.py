# -*- coding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import Blog,Category,Tag
from api.serializers import BlogSerizalizers,BlogsSerizalizers, CategorySerizalizers ,TagSerizalizers ,TimeLineSerizalizers
from base.util import user_visit

class BlogsView(APIView,PageNumberPagination):

    def get(self,request):
        blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False).order_by('-create_time')
        serializer = BlogsSerizalizers(self.paginate_queryset(blogs,request,view=None),many=True)
        return self.get_paginated_response(serializer.data)

class CategoryView(APIView):

    def get(self,request):

        categorys = Category.objects.filter(is_delete=False)
        serializer = CategorySerizalizers(categorys,many=True)

        return Response(serializer.data)

class BlogView(APIView):

    def get(self,request,blog_name):
        blog_id = blog_name.split('-')[1].split('.')[0]
        blog=Blog.objects.prefetch_related('tag').select_related("category").get(id=blog_id,name=blog_name,is_delete=False)
        serializer = BlogSerizalizers(blog)
        user_visit(request,blog)
        return Response(serializer.data)

class CategoryBlogView(APIView,PageNumberPagination):

    def get(self,request,category_id):
        blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False,category_id=category_id).order_by('-create_time')
        serializer = BlogsSerizalizers(self.paginate_queryset(blogs,request,view=None),many=True)
        return self.get_paginated_response(serializer.data)

class FavView(APIView,PageNumberPagination):

    def get(self,request):
        blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False,fav=True).order_by('-create_time')
        serializer = BlogsSerizalizers(self.paginate_queryset(blogs,request,view=None),many=True)
        return self.get_paginated_response(serializer.data)

class TimeLine(APIView,PageNumberPagination):

    def get(self,request):
        blogs = Blog.objects.filter(is_delete = False).order_by('-create_time').values('name','title','create_time')
        serializer = TimeLineSerizalizers(blogs,many=True)
        return Response(serializer.data)

class SearchView(APIView,PageNumberPagination):

    def get(self,request):
        keywords = request.GET.get('keywords') or ''
        blogs = Blog.objects.prefetch_related('tag').select_related('category').filter(is_delete = False,title__contains=keywords).order_by('-create_time')
        serializer = BlogsSerizalizers(self.paginate_queryset(blogs,request,view=None),many=True)
        return self.get_paginated_response(serializer.data)

class TagBlogsView(APIView,PageNumberPagination):
    def get(self,request,tag_id):
        tag = Tag.objects.get(id = tag_id)
        blogs = tag.blog_set.prefetch_related('tag').select_related('category').all()
        serializer = BlogsSerizalizers(self.paginate_queryset(blogs,request,view=None),many=True)
        return self.get_paginated_response(serializer.data)
