# -*- coding: utf-8 -*-
from rest_framework import serializers
from base.models import Blog , Tag, Category ,User

class UserSerizalizers(serializers.ModelSerializer):

    class Meta:
        model = User

class CategorySerizalizers(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('create_time','update_time','is_delete')

class TagSerizalizers(serializers.ModelSerializer):

    class Meta:
        model = Tag


class BlogsSerizalizers(serializers.ModelSerializer):
    category = CategorySerizalizers(read_only=True)
    tag = TagSerizalizers(read_only=True,many=True)

    class Meta:
        model = Blog
        exclude = ('content','is_delete','fav')


class BlogSerizalizers(serializers.ModelSerializer):
    category = CategorySerizalizers(read_only=True)
    tag = TagSerizalizers(read_only=True,many=True)

    class Meta:
        model = Blog


class TimeLineSerizalizers(serializers.Serializer):
    name = serializers.CharField()
    title = serializers.CharField()
    create_time = serializers.DateTimeField()

